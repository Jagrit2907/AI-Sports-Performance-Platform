import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

LINEUPS_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "statsbomb"
    / "lineups"
)

EVENTS_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "statsbomb"
    / "events"
)


def main():

    empty_position_players = 0
    empty_position_players_in_events = 0

    # Use one match first.
    lineup_file = next(
        LINEUPS_DIR.glob("*.json")
    )

    match_id = lineup_file.stem

    event_file = (
        EVENTS_DIR
        / f"{match_id}.json"
    )

    with lineup_file.open(
        "r",
        encoding="utf-8"
    ) as file:

        lineups = json.load(file)

    with event_file.open(
        "r",
        encoding="utf-8"
    ) as file:

        events = json.load(file)

    event_player_ids = set()

    for event in events:

        player = event.get("player")

        if player:

            event_player_ids.add(
                player["id"]
            )

    print("Match:", match_id)

    for team in lineups:

        for player in team["lineup"]:

            positions = player.get(
                "positions",
                []
            )

            if not positions:

                empty_position_players += 1

                player_id = player["player_id"]

                if player_id in event_player_ids:

                    empty_position_players_in_events += 1

                    print(
                        "Empty position BUT appears in events:",
                        player["player_name"]
                    )

    print(
        "\nPlayers with empty positions:",
        empty_position_players
    )

    print(
        "Empty-position players appearing in events:",
        empty_position_players_in_events
    )


if __name__ == "__main__":
    main()