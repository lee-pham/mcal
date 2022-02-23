import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime

event_list = [
    {"summary": "Dentist", "start": "08:00", "end": "09:00"},
    {"summary": "Work", "start": "08:30", "end": "09:00"},
    {"summary": "Lunch", "start": "12:00", "end": "13:00"},
    {"summary": "Pottery", "start": "18:00", "end": "21:00"},
    {"summary": "Lee", "start": "22:00", "end": "23:59"},
]


def military_to_minutes(time_in_military: str) -> int:
    hours, minutes = time_in_military.split(":")
    return int(hours) * 60 + int(minutes)


def is_complete(event: dict) -> dict:
    current_time = datetime.now().strftime("%H:%M")
    if military_to_minutes(current_time) >= military_to_minutes(event["end"]):
        # complete
        return {
            "color": "#6c757d",
            "markerfacecolor": "#6c757d",
            "xy": .005
        }
    else:
        # incomplete
        return {
            "color": "k",
            "markerfacecolor": "w",
            "xy": -.0075
        }


events = [f'{event["start"]} {event["summary"]}' for event in event_list]

# Create figure and plot a stem plot with the date
fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)

current_time = datetime.now().strftime("%H:%M")

# Black line for the entire timeline
ax.plot([0, 24 * 60], [0, 0], "-", color="k")
# Gray for time that has passed
ax.plot([0, military_to_minutes(current_time)], [0, 0], "-", color="#6c757d")

# Red tick for current time
ax.plot(military_to_minutes(current_time), 0, "|", color="r")

for event in event_list:
    ax.plot(military_to_minutes(event["start"]), 0, "o",
            color=is_complete(event)["color"], markerfacecolor=is_complete(event)["markerfacecolor"])
    ax.annotate(event["summary"], (military_to_minutes(event["start"]), is_complete(event)["xy"]))

# annotate lines
# for i, txt in enumerate(events):
#     ax.annotate(txt, ([military_to_minutes(event["start"]) for event in event_list][i], .005))

# remove x, y axis and spines
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.spines[["left", "top", "right", "bottom"]].set_visible(False)

ax.margins(y=0.1)
plt.show()
