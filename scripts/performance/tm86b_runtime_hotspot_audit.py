from pathlib import Path
import ast
import json
import re
import time
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "reports" / "performance"
APP = ROOT / "app" / "streamlit_app.py"

REPORTS.mkdir(parents=True, exist_ok=True)

TARGET_DATASETS = [
    ROOT / "data" / "processed" / "current_performance_snapshot.parquet",
    ROOT / "data" / "processed" / "transfermarkt_features_v13a.parquet",
    ROOT / "reports" / "strategy" / "transfer_portfolio_dataset.csv",
    ROOT / "reports" / "roles" / "player_role_dna.csv",
    ROOT / "reports" / "roles" / "player_role_labels.csv",
    ROOT / "data" / "processed" / "current_player_snapshot.csv",
]

HEAVY_PATTERNS = {
    "read_parquet": r"\bread_parquet\s*\(",
    "read_csv": r"\bread_csv\s*\(",
    "merge": r"\.merge\s*\(|\bmerge\s*\(",
    "groupby": r"\.groupby\s*\(",
    "dataframe_apply_axis1": r"\.apply\s*\([^)]*axis\s*=\s*1",
    "apply_generic": r"\.apply\s*\(",
    "plotly_figure": r"go\.Figure\s*\(|px\.",
    "st_plotly_chart": r"st\.plotly_chart\s*\(",
}

def read_dataset(path: Path):
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    raise ValueError(path)

def repeated_dataset_reads(n=5):
    rows = []

    for path in TARGET_DATASETS:
        if not path.exists():
            rows.append({
                "path": str(path.relative_to(ROOT)),
                "exists": False,
                "error": "missing",
            })
            continue

        timings = []
        shape = None
        memory_mb = None

        for i in range(n):
            t0 = time.perf_counter()
            df = read_dataset(path)
            elapsed = time.perf_counter() - t0

            if shape is None:
                shape = df.shape
                memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024

            timings.append(elapsed)

        timings_sorted = sorted(timings)
        rows.append({
            "path": str(path.relative_to(ROOT)),
            "exists": True,
            "rows": shape[0],
            "columns": shape[1],
            "memory_mb": round(memory_mb, 3),
            "cold_read_seconds": round(timings[0], 6),
            "median_read_seconds": round(timings_sorted[len(timings_sorted)//2], 6),
            "min_read_seconds": round(min(timings), 6),
            "max_read_seconds": round(max(timings), 6),
            "all_reads_seconds": json.dumps([round(x, 6) for x in timings]),
        })

    out = REPORTS / "tm86b_repeated_dataset_reads.csv"
    pd.DataFrame(rows).sort_values(
        ["median_read_seconds", "cold_read_seconds"],
        ascending=False,
        na_position="last",
    ).to_csv(out, index=False)

    return rows

def function_ranges(source: str):
    tree = ast.parse(source)
    funcs = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcs.append({
                "function": node.name,
                "line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno),
                "n_lines": getattr(node, "end_lineno", node.lineno) - node.lineno + 1,
                "decorators": [
                    ast.unparse(d) if hasattr(ast, "unparse") else str(d)
                    for d in node.decorator_list
                ],
            })

    funcs.sort(key=lambda x: x["line"])
    return funcs

def locate_function(funcs, line_no):
    lo, hi = None, None
    for f in funcs:
        if f["line"] <= line_no <= f["end_line"]:
            if lo is None or f["line"] >= lo["line"]:
                lo = f
    return lo

def static_hotspots_by_function():
    source = APP.read_text(encoding="utf-8")
    lines = source.splitlines()
    funcs = function_ranges(source)

    rows = []
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        for hotspot, pattern in HEAVY_PATTERNS.items():
            if re.search(pattern, stripped):
                func = locate_function(funcs, i)
                rows.append({
                    "hotspot_type": hotspot,
                    "line": i,
                    "function": func["function"] if func else "__module__",
                    "function_start": func["line"] if func else None,
                    "function_end": func["end_line"] if func else None,
                    "function_n_lines": func["n_lines"] if func else None,
                    "function_decorators": " | ".join(func["decorators"]) if func else "",
                    "code": stripped[:260],
                })

    df = pd.DataFrame(rows)
    df.to_csv(REPORTS / "tm86b_static_hotspots_by_function.csv", index=False)

    if len(df):
        grouped = (
            df.groupby(["function", "hotspot_type"])
            .size()
            .reset_index(name="count")
            .sort_values(["count", "function"], ascending=[False, True])
        )
    else:
        grouped = pd.DataFrame(columns=["function", "hotspot_type", "count"])

    grouped.to_csv(REPORTS / "tm86b_hotspot_function_summary.csv", index=False)

    priority = []
    if len(df):
        for func, g in df.groupby("function"):
            types = set(g["hotspot_type"])
            score = 0
            score += 5 * len(g[g["hotspot_type"].isin(["read_parquet", "read_csv"])])
            score += 4 * len(g[g["hotspot_type"].isin(["dataframe_apply_axis1"])])
            score += 3 * len(g[g["hotspot_type"].isin(["merge", "groupby"])])
            score += 2 * len(g[g["hotspot_type"].isin(["plotly_figure", "st_plotly_chart"])])
            score += 1 * len(g[g["hotspot_type"].isin(["apply_generic"])])
            func_meta = g.iloc[0]
            priority.append({
                "function": func,
                "priority_score": score,
                "hotspot_count": len(g),
                "hotspot_types": ", ".join(sorted(types)),
                "function_start": func_meta["function_start"],
                "function_end": func_meta["function_end"],
                "function_n_lines": func_meta["function_n_lines"],
                "cached": "cache" in str(func_meta["function_decorators"]).lower(),
            })

    priority_df = pd.DataFrame(priority).sort_values(
        ["priority_score", "hotspot_count"], ascending=False
    )
    priority_df.to_csv(REPORTS / "tm86b_candidate_optimization_functions.csv", index=False)

    return rows, grouped.to_dict("records"), priority

def main():
    read_rows = repeated_dataset_reads(n=5)
    hotspot_rows, grouped_rows, priority_rows = static_hotspots_by_function()

    summary = {
        "repeated_dataset_reads": len(read_rows),
        "hotspot_lines": len(hotspot_rows),
        "candidate_functions": len(priority_rows),
        "top_candidate_functions": sorted(
            priority_rows,
            key=lambda x: (x["priority_score"], x["hotspot_count"]),
            reverse=True,
        )[:20],
    }

    (REPORTS / "tm86b_runtime_hotspot_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
