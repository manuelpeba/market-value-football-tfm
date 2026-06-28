from pathlib import Path
import ast
import csv
import re
import time
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "reports" / "performance"
APP = ROOT / "app" / "streamlit_app.py"

DATA_DIRS = [
    ROOT / "data" / "processed",
    ROOT / "reports",
]

DATASET_PATTERNS = ["*.parquet", "*.csv"]

HOTSPOT_PATTERNS = {
    "read_parquet": r"\bread_parquet\s*\(",
    "read_csv": r"\bread_csv\s*\(",
    "merge": r"\.merge\s*\(|\bmerge\s*\(",
    "groupby": r"\.groupby\s*\(",
    "apply": r"\.apply\s*\(",
    "plotly": r"\bgo\.|plotly|px\.",
    "st_plotly_chart": r"st\.plotly_chart\s*\(",
    "st_dataframe": r"st\.dataframe\s*\(",
    "st_markdown_html": r"st\.markdown\s*\(.*unsafe_allow_html\s*=\s*True",
}

def safe_read(path: Path):
    t0 = time.perf_counter()
    if path.suffix.lower() == ".parquet":
        df = pd.read_parquet(path)
    elif path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        return None
    elapsed = time.perf_counter() - t0
    return {
        "path": str(path.relative_to(ROOT)),
        "suffix": path.suffix.lower(),
        "rows": len(df),
        "columns": len(df.columns),
        "read_seconds": round(elapsed, 6),
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 3),
    }

def audit_datasets():
    rows = []
    seen = set()

    for base in DATA_DIRS:
        if not base.exists():
            continue
        for pattern in DATASET_PATTERNS:
            for path in base.rglob(pattern):
                rel = str(path.relative_to(ROOT))
                if rel in seen:
                    continue
                seen.add(rel)
                try:
                    rows.append(safe_read(path))
                except Exception as e:
                    rows.append({
                        "path": rel,
                        "suffix": path.suffix.lower(),
                        "rows": None,
                        "columns": None,
                        "read_seconds": None,
                        "memory_mb": None,
                        "error": repr(e),
                    })

    rows = [r for r in rows if r]
    out = REPORTS / "tm86_dataset_read_times.csv"
    pd.DataFrame(rows).sort_values(
        ["read_seconds", "memory_mb"], ascending=False, na_position="last"
    ).to_csv(out, index=False)
    return rows

def decorators_for(node):
    values = []
    for d in node.decorator_list:
        try:
            values.append(ast.unparse(d))
        except Exception:
            values.append(str(d))
    return values

def audit_functions():
    source = APP.read_text(encoding="utf-8")
    tree = ast.parse(source)

    rows = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            decos = decorators_for(node)
            has_cache_data = any("st.cache_data" in d or "cache_data" in d for d in decos)
            has_cache_resource = any("st.cache_resource" in d or "cache_resource" in d for d in decos)
            rows.append({
                "function": node.name,
                "line": node.lineno,
                "end_line": getattr(node, "end_lineno", None),
                "n_lines": (getattr(node, "end_lineno", node.lineno) - node.lineno + 1),
                "decorators": " | ".join(decos),
                "has_cache_data": has_cache_data,
                "has_cache_resource": has_cache_resource,
                "has_any_cache": has_cache_data or has_cache_resource,
            })

    out = REPORTS / "tm86_streamlit_function_cache_audit.csv"
    pd.DataFrame(rows).sort_values(
        ["has_any_cache", "n_lines"], ascending=[True, False]
    ).to_csv(out, index=False)

    summary = {
        "total_functions": len(rows),
        "cached_functions": sum(1 for r in rows if r["has_any_cache"]),
        "cache_data_functions": sum(1 for r in rows if r["has_cache_data"]),
        "cache_resource_functions": sum(1 for r in rows if r["has_cache_resource"]),
        "uncached_functions": sum(1 for r in rows if not r["has_any_cache"]),
    }
    (REPORTS / "tm86_streamlit_cache_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return rows, summary

def audit_hotspots():
    source = APP.read_text(encoding="utf-8")
    lines = source.splitlines()
    rows = []

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        for name, pattern in HOTSPOT_PATTERNS.items():
            if re.search(pattern, stripped):
                rows.append({
                    "hotspot_type": name,
                    "line": i,
                    "code": stripped[:260],
                })

    out = REPORTS / "tm86_static_hotspots.csv"
    pd.DataFrame(rows).sort_values(["hotspot_type", "line"]).to_csv(out, index=False)
    return rows

def main():
    REPORTS.mkdir(parents=True, exist_ok=True)

    datasets = audit_datasets()
    functions, cache_summary = audit_functions()
    hotspots = audit_hotspots()

    console = {
        "datasets_audited": len(datasets),
        "slowest_datasets": sorted(
            [d for d in datasets if d.get("read_seconds") is not None],
            key=lambda x: x["read_seconds"],
            reverse=True,
        )[:10],
        "cache_summary": cache_summary,
        "hotspot_count": len(hotspots),
        "hotspot_breakdown": pd.DataFrame(hotspots)["hotspot_type"].value_counts().to_dict() if hotspots else {},
    }

    (REPORTS / "tm86_performance_audit_summary.json").write_text(
        json.dumps(console, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(console, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
