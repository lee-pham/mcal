from datetime import datetime

import matplotlib.pyplot as plt
from adjustText import adjust_text

# Constants
GRAY = "#6c757d"
TIMELINE_WIDTH = .75
RED_TICK_SIZE = 15


def military_to_minutes(time_in_military: str) -> int:
    hours, minutes = time_in_military.split(":")
    return int(hours) * 60 + int(minutes)


def is_complete(event: dict) -> dict:
    current_time = datetime.now().strftime("%H:%M")
    if military_to_minutes(current_time) >= military_to_minutes(event["end"]):
        # complete
        return {
            "color": GRAY,
            "markerfacecolor": GRAY,
            "xy": .01
        }
    elif military_to_minutes(event["start"]) < military_to_minutes(current_time) and military_to_minutes(
            current_time) <= military_to_minutes(event["end"]):
        # in progress
        return {
            "color": "k",
            "markerfacecolor": "k",
            "xy": .01
        }
    else:
        # incomplete
        return {
            "color": "k",
            "markerfacecolor": "w",
            "xy": -.01
        }


class Timeline:
    event_list = [
        {"summary": "Dentist", "start": "08:00", "end": "09:00"},
        {"summary": "Work", "start": "08:30", "end": "09:00"},
        {"summary": "Lunch", "start": "12:00", "end": "13:00"},
        {"summary": "Coffee", "start": "12:15", "end": "12:30"},
        {"summary": "Pottery", "start": "18:00", "end": "21:00"},
        {"summary": "Lee", "start": "22:00", "end": "23:59"},
    ]

    # Create figure and plot a stem plot with the date
    # fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=False)
    current_time = datetime.now().strftime("%H:%M")

    # Black line for the entire timeline
    ax.plot([0, 24 * 60], [0, 0], "-", color="k", linewidth=TIMELINE_WIDTH)
    # Gray for time that has passed
    ax.plot([0, military_to_minutes(current_time)], [0, 0], "-", color=GRAY, linewidth=TIMELINE_WIDTH)

    # Red tick for current time
    ax.plot(military_to_minutes(current_time), 0, "|", color="r", markersize=RED_TICK_SIZE)

    texts = []
    for event in event_list:
        summary_with_time = f'{event["start"]} {event["summary"]}'

        ax.plot(
            military_to_minutes(event["start"]), 0,
            "o", color=is_complete(event)["color"], markerfacecolor=is_complete(event)["markerfacecolor"])

        texts.append(
            ax.text(s=summary_with_time,
                    x=military_to_minutes(event["start"]), y=is_complete(event)["xy"],
                    color=is_complete(event)["color"])
        )

    # remove x, y axis and spines
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right", "bottom"]].set_visible(False)
    ax.margins(y=0.1)

    adjust_text(texts, only_move={'points': 'y', 'text': 'y', 'objects': 'y'}, ha='left', va='bottom')
    # plt.show()
    fig.savefig("render/timeline.png", bbox_inches='tight', transparent=True)
