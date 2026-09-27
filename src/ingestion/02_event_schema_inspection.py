import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

EVENTS_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "statsbomb"
    / "events"
)


EVENT_TYPES_TO_FIND = {
    "Pass",
    "Shot",
    "Carry",
    "Pressure",
    "Duel",
    "Interception",
}


def get_event_type(event):
    """Return the event type name."""

    return event.get("type", {}).get("name")


def inspect_event(event):
    """Print the structure of one selected event."""

    event_type = get_event_type(event)

    print("\n" + "=" * 60)
    print("EVENT TYPE:", event_type)
    print("=" * 60)

    print("\nTop-level fields:")

    for key in event.keys():
        print(" -", key)

    # StatsBomb usually stores event-specific information
    # under a key matching the event type.
    nested_key = event_type.lower()

    if nested_key in event:

        print(
            f"\nFields inside '{nested_key}':"
        )

        nested_data = event[nested_key]

        if isinstance(nested_data, dict):

            for key in nested_data.keys():
                print(" -", key)

        else:

            print("Not a dictionary")

    print("\nBasic example information:")

    print(
        "Player:",
        event.get("player", {}).get("name")
    )

    print(
        "Team:",
        event.get("team", {}).get("name")
    )

    print(
    "Position:",
    event.get("position", {}).get("name")
)

    print(
        "Location:",
        event.get("location")
    )


def main():

    found_events = {}

    event_files = sorted(
        EVENTS_DIR.glob("*.json")
    )

    print(
        "Searching through event files..."
    )

    for file_path in event_files:

        with file_path.open(
            "r",
            encoding="utf-8"
        ) as file:

            events = json.load(file)

        for event in events:

            event_type = get_event_type(event)

            if (
                event_type in EVENT_TYPES_TO_FIND
                and event_type not in found_events
            ):

                found_events[event_type] = event

            if (
                len(found_events)
                == len(EVENT_TYPES_TO_FIND)
            ):
                break

        if (
            len(found_events)
            == len(EVENT_TYPES_TO_FIND)
        ):
            break

    print("\nFound event types:")

    for event_type in sorted(found_events):

        print(" -", event_type)

    # Inspect each selected event
    for event_type in sorted(found_events):

        inspect_event(
            found_events[event_type]
        )


if __name__ == "__main__":
    main()