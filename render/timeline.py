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
    if military_to_minutes(current_time) >= military_to_minutes(event["endDatetime"].strftime("%H:%M")):
        # complete
        return {
            "color": GRAY,
            "markerfacecolor": GRAY,
            "xy": .01
        }
    elif military_to_minutes(event["startDatetime"].strftime("%H:%M")) < military_to_minutes(
            current_time) and military_to_minutes(
            current_time) <= military_to_minutes(event["endDatetime"].strftime("%H:%M")):
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
    def __init__(self, event_list):
        self.event_list = event_list
        # self.event_list = [
        #     {"summary": "Dentist", "startDatetime": "08:00", "endDatetime": "09:00"},
        #     {"summary": "Work", "startDatetime": "08:30", "endDatetime": "09:00"},
        #     {"summary": "Lunch", "startDatetime": "12:00", "endDatetime": "13:00"},
        #     {"summary": "Coffee", "startDatetime": "12:15", "endDatetime": "12:30"},
        #     {"summary": "Pottery", "startDatetime": "18:00", "endDatetime": "21:00"},
        #     {"summary": "Lee", "startDatetime": "22:00", "endDatetime": "23:59"},
        # ]
        self.current_datetime = datetime.now()
        self.current_time = self.current_datetime.strftime("%H:%M")
        self.current_day = self.current_datetime.today()

    def render(self):
        # Create figure and plot a stem plot with the date
        # fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
        fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=False)

        # Black line for the entire timeline
        ax.plot([0, 24 * 60], [0, 0], "-", color="k", linewidth=TIMELINE_WIDTH)
        # Gray for time that has passed
        ax.plot([0, military_to_minutes(self.current_time)], [0, 0],
                "-", color=GRAY, linewidth=TIMELINE_WIDTH)

        # Red tick for current time
        ax.plot(military_to_minutes(self.current_time), 0,
                "|", color="r", markersize=RED_TICK_SIZE)

        texts = []
        for event in self.event_list:
            summary_with_time = f'{event["startDatetime"].strftime("%H:%M")} ' * (
                not event["allday"]) + f'{event["summary"]}'

            ax.plot(
                military_to_minutes(event["startDatetime"].strftime("%H:%M")), 0,
                "o", color=is_complete(event)["color"], markerfacecolor=is_complete(event)["markerfacecolor"])

            texts.append(
                ax.text(s=summary_with_time,
                        x=military_to_minutes(event["startDatetime"].strftime("%H:%M")), y=is_complete(event)["xy"],
                        color=is_complete(event)["color"])
            )

        # remove x, y axis and spines
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.spines[["left", "top", "right", "bottom"]].set_visible(False)
        ax.margins(y=0.1)

        adjust_text(texts, only_move={
                    'points': 'y', 'text': 'y', 'objects': 'y'}, ha='left', va='bottom')
        # plt.show()
        fig.savefig("render/timeline.png", bbox_inches='tight', transparent=True)
