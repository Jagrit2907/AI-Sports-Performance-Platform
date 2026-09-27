import json
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

EVENTS_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "statsbomb"
    / "events"
)


def main():

    pass_outcomes = Counter()
    dribble_outcomes = Counter()

    pass_fields = {
        "shot_assist": Counter(),
        "goal_assist": Counter(),
        "through_ball": Counter(),
        "cross": Counter(),
    }

    for path in EVENTS_DIR.glob("*.json"):

        with path.open(
            "r",
            encoding="utf-8"
        ) as file:

            events = json.load(file)

        for event in events:

            event_type = (
                event
                .get("type", {})
                .get("name")
            )

            # ---------------------------------------------
            # PASS
            # ---------------------------------------------

            if event_type == "Pass":

                data = event.get(
                    "pass",
                    {}
                )

                outcome = data.get(
                    "outcome"
                )

                if isinstance(outcome, dict):
                    outcome = outcome.get("name")

                pass_outcomes[outcome] += 1

                for field in pass_fields:

                    if field in data:

                        value = data[field]

                        if value is True:
                            pass_fields[field]["True"] += 1

                        elif value is False:
                            pass_fields[field]["False"] += 1

                        else:
                            pass_fields[field][str(value)] += 1

                    else:

                        pass_fields[field]["Not present"] += 1

            # ---------------------------------------------
            # DRIBBLE
            # ---------------------------------------------

            elif event_type == "Dribble":

                data = event.get(
                    "dribble",
                    {}
                )

                outcome = data.get(
                    "outcome"
                )

                if isinstance(outcome, dict):
                    outcome = outcome.get("name")

                dribble_outcomes[outcome] += 1

    # =====================================================
    # PRINT RESULTS
    # =====================================================

    print("\n" + "=" * 50)
    print("PASS OUTCOMES")
    print("=" * 50)

    for value, count in pass_outcomes.most_common():
        print(f"{value}: {count}")

    print("\n" + "=" * 50)
    print("DRIBBLE OUTCOMES")
    print("=" * 50)

    for value, count in dribble_outcomes.most_common():
        print(f"{value}: {count}")

    for field, counter in pass_fields.items():

        print("\n" + "=" * 50)
        print(field.upper())
        print("=" * 50)

        for value, count in counter.most_common():
            print(f"{value}: {count}")


if __name__ == "__main__":
    main()