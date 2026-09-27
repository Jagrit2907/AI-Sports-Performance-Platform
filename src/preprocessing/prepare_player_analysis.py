import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "player_stats.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "player_analysis.csv"
)

MIN_MINUTES = 300


def position_group(position):

    if position == "Goalkeeper":
        return "Goalkeeper"

    if position in [
        "Center Back",
        "Left Center Back",
        "Right Center Back"
    ]:
        return "Centre Back"

    if position in [
        "Left Back",
        "Right Back",
        "Left Wing Back",
        "Right Wing Back"
    ]:
        return "Full Back"

    if position in [
        "Center Defensive Midfield",
        "Left Defensive Midfield",
        "Right Defensive Midfield"
    ]:
        return "Defensive Midfielder"

    if position in [
        "Center Midfield",
        "Left Center Midfield",
        "Right Center Midfield",
        "Left Midfield",
        "Right Midfield"
    ]:
        return "Midfielder"

    if position in [
        "Center Attacking Midfield",
        "Left Attacking Midfield",
        "Right Attacking Midfield"
    ]:
        return "Attacking Midfielder"

    if position in [
        "Left Wing",
        "Right Wing"
    ]:
        return "Winger"

    if position in [
        "Center Forward",
        "Left Center Forward",
        "Right Center Forward",
        "Secondary Striker"
    ]:
        return "Forward"

    return "Unknown"


def main():

    df = pd.read_csv(INPUT_FILE)

    # Create broader position groups.
    df["position_group"] = (
        df["primary_position"]
        .apply(position_group)
    )

    # Players meeting our minimum sample requirement.
    df["eligible_for_analysis"] = (
        df["minutes_played"] >= MIN_MINUTES
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        "Player analysis dataset created."
    )

    print(
        "Total players:",
        len(df)
    )

    print(
        "Players with >= 300 minutes:",
        df["eligible_for_analysis"].sum()
    )

    print(
        "\nPosition groups:"
    )

    print(
        df["position_group"]
        .value_counts()
    )

    print(
        "\nSaved to:",
        OUTPUT_FILE
    )


if __name__ == "__main__":
    main()