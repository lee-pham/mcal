import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime

event_list = [
    {"summary": "Dentist", "start": "08:00"},
    {"summary": "Work", "start": "08:30"},
    {"summary": "Lunch", "start": "12:00"},
    {"summary": "Pottery", "start": "18:00"},
    {"summary": "Lee", "start": "22:00"},
]


def military_to_minutes(time_in_military: str) -> int:
    hours, minutes = time_in_military.split(":")
    return int(hours) * 60 + int(minutes)


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
ax.plot([military_to_minutes(event["start"]) for event in event_list], np.zeros_like(events), "-o",
        color="k", markerfacecolor="w")  # Baseline and markers on it.

# annotate lines
for i, txt in enumerate(events):
    ax.annotate(txt, ([military_to_minutes(event["start"]) for event in event_list][i], .005))

# remove x, y axis and spines
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.spines[["left", "top", "right", "bottom"]].set_visible(False)

ax.margins(y=0.1)
plt.show()
