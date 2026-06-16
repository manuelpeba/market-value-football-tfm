import asyncio
import aiohttp
from understat import Understat


async def main():

    async with aiohttp.ClientSession() as session:

        understat = Understat(session)

        players = await understat.get_league_players(
            "EPL",
            2024
        )

        print(f"Players retrieved: {len(players)}")

        if players:
            print("\nSample player:")
            print(players[0])


if __name__ == "__main__":
    asyncio.run(main())