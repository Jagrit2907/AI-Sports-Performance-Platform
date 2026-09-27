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


def get_name(value):
    if isinstance(value, dict):
        return value.get("name")
    return value


def main():

    counters = {
        "pass_type": Counter(),
        "pass_height": Counter(),
        "pass_body_part": Counter(),

        "duel_type": Counter(),
        "duel_outcome": Counter(),

        "interception_outcome": Counter(),

        "shot_outcome": Counter(),
        "shot_type": Counter(),
        "shot_technique": Counter(),
        "shot_body_part": Counter(),
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

            if event_type == "Pass":

                data = event.get(
                    "pass",
                    {}
                )

                counters["pass_type"][
                    get_name(data.get("type"))
                ] += 1

                counters["pass_height"][
                    get_name(data.get("height"))
                ] += 1

                counters["pass_body_part"][
                    get_name(data.get("body_part"))
                ] += 1

            elif event_type == "Duel":

                data = event.get(
                    "duel",
                    {}
                )

                counters["duel_type"][
                    get_name(data.get("type"))
                ] += 1

                counters["duel_outcome"][
                    get_name(data.get("outcome"))
                ] += 1

            elif event_type == "Interception":

                data = event.get(
                    "interception",
                    {}
                )

                counters["interception_outcome"][
                    get_name(data.get("outcome"))
                ] += 1

            elif event_type == "Shot":

                data = event.get(
                    "shot",
                    {}
                )

                counters["shot_outcome"][
                    get_name(data.get("outcome"))
                ] += 1

                counters["shot_type"][
                    get_name(data.get("type"))
                ] += 1

                counters["shot_technique"][
                    get_name(data.get("technique"))
                ] += 1

                counters["shot_body_part"][
                    get_name(data.get("body_part"))
                ] += 1

    for name, counter in counters.items():

        print("\n" + "=" * 50)
        print(name)
        print("=" * 50)

        for value, count in counter.most_common():

            print(
                f"{value}: {count}"
            )


if __name__ == "__main__":
    main()