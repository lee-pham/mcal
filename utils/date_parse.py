import datetime


def enumerate_multiday_event(event_list: list) -> list:
    enumerated_event_list = []
    for event in event_list:
        if event["isMultiday"]:
            if event["startDatetime"].tzinfo._tzname != event["endDatetime"].tzinfo._tzname:
                if event["endDatetime"].tzinfo._tzname == "CDT":
                    event["endDatetime"] += datetime.timedelta(hours=1)
                else:
                    event["endDatetime"] -= datetime.timedelta(hours=1)

            duration = event["endDatetime"] + datetime.timedelta(microseconds=1) - event["startDatetime"]
            print("Multiday:", event, duration)
            enumerated_event = {
                "summary": event["summary"],
                "startDatetime": event["startDatetime"],
                "endDatetime": event["startDatetime"] + datetime.timedelta(1) - datetime.timedelta(microseconds=1),
                "isMultiday": True,
                "isUpdated": event["isUpdated"],
                "allday": event["allday"],
                "duration": duration,
                "main": True
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
                    "hide": "text",
                    "duration": duration
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
                    "hide": "text",
                    "duration": duration
                }
                enumerated_event_list.append(enumerated_event)
        else:
            event["duration"] = datetime.timedelta(0)
            enumerated_event_list.append(event)

    return enumerated_event_list


def test_account_for_dst_begin():
    # event_ends_after_dst = [
    #     {'summary': 'Ab', 'allday': True, 'startDatetime': datetime.datetime(2022, 3, 12, 0, 0, tzinfo= < DstTzInfo
    #      'America/Chicago' CST - 1 day, 18:00: 00
    # STD >), 'endDatetime': datetime.datetime(2022, 3, 13, 23, 59, 59, 999999, tzinfo= < DstTzInfo
    # 'America/Chicago'
    # CDT - 1
    # day, 19: 00:00
    # DST >), 'updatedDatetime': datetime.datetime(2022, 3, 10, 23, 6, 14, 575000, tzinfo= < DstTzInfo
    # 'America/Chicago'
    # CST - 1
    # day, 18: 00:00
    # STD >), 'isUpdated': False, 'isMultiday': True}
    # ]
    pass


def test_account_for_dst_end():
    pass
