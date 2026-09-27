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


def main():

    found_sub_on = False
    found_sub_off = False
    found_multi_position = False

    for file in LINEUPS_DIR.glob("*.json"):

        with file.open(
            "r",
            encoding="utf-8"
        ) as f:

            lineups = json.load(f)

        for team in lineups:

            for player in team["lineup"]:

                positions = player.get(
                    "positions",
                    []
                )

                # -----------------------------------------
                # Substitute on
                # -----------------------------------------

                for pos in positions:

                    start_reason = pos.get(
                        "start_reason"
                    )

                    end_reason = pos.get(
                        "end_reason"
                    )

                    if (
                        "Substitution" in str(start_reason)
                        and not found_sub_on
                    ):

                        print("\n" + "=" * 60)
                        print("EXAMPLE: SUBSTITUTE ON")
                        print("=" * 60)

                        print(
                            json.dumps(
                                player,
                                indent=2,
                                ensure_ascii=False
                            )
                        )

                        found_sub_on = True

                    # -------------------------------------
                    # Substitute off
                    # -------------------------------------

                    if (
                        "Substitution" in str(end_reason)
                        and not found_sub_off
                    ):

                        print("\n" + "=" * 60)
                        print("EXAMPLE: SUBSTITUTE OFF")
                        print("=" * 60)

                        print(
                            json.dumps(
                                player,
                                indent=2,
                                ensure_ascii=False
                            )
                        )

                        found_sub_off = True

                # -----------------------------------------
                # Multiple position intervals
                # -----------------------------------------

                if (
                    len(positions) > 1
                    and not found_multi_position
                ):

                    print("\n" + "=" * 60)
                    print("EXAMPLE: MULTIPLE POSITIONS")
                    print("=" * 60)

                    print(
                        json.dumps(
                            player,
                            indent=2,
                            ensure_ascii=False
                        )
                    )

                    found_multi_position = True

                # -----------------------------------------
                # Stop once all three examples are found
                # -----------------------------------------

                if (
                    found_sub_on
                    and found_sub_off
                    and found_multi_position
                ):
                    return

    print("\nInspection completed.")


if __name__ == "__main__":
    main()