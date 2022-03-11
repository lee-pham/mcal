import datetime


def enumerate_multiday_event(event_list: list) -> list:
    enumerated_event_list = []
    for event in event_list:
        if event["isMultiday"]:
            if event["startDatetime"].tzinfo._tzname != event["endDatetime"].tzinfo._tzname:
                event["endDatetime"] += datetime.timedelta(hours=1)
            duration = event["endDatetime"] + datetime.timedelta(microseconds=1) - event["startDatetime"]
            print("@@@@@", event["summary"], duration)
            enumerated_event = {
                "summary": event["summary"],
                "startDatetime": event["startDatetime"],
                "endDatetime": event["startDatetime"] + datetime.timedelta(1) - datetime.timedelta(microseconds=1),
                "isMultiday": True,
                "isUpdated": event["isUpdated"],
                "allday": event["allday"]
            }
            enumerated_event_list.append(enumerated_event)
            for date in [event["startDatetime"] + datetime.timedelta(i) for i in range(1, duration.days)]:
                enumerated_event = {
                    "summary": event["summary"],
                    "startDatetime": date,
                    "endDatetime": date + datetime.timedelta(1) - datetime.timedelta(microseconds=1),
                    "isMultiday": True,
                    "isUpdated": event["isUpdated"],
                    "allday": event["allday"],
                    "hide": True
                }
                last_date = date
                enumerated_event_list.append(enumerated_event)

            if duration.seconds + duration.microseconds > 0:
                enumerated_event = {
                    "summary": event["summary"],
                    "startDatetime": last_date + datetime.timedelta(1),
                    "endDatetime": event["endDatetime"],
                    "isMultiday": True,
                    "isUpdated": event["isUpdated"],
                    "allday": event["allday"],
                    "hide": True
                }
                enumerated_event_list.append(enumerated_event)
        else:
            enumerated_event_list.append(event)

    return enumerated_event_list
