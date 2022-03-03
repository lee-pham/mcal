import datetime


def enumerate_multiday_event(event_list: list) -> list:
    enumerated_event_list = []
    for event in event_list:
        if event["isMultiday"]:
            duration = event["endDatetime"] +datetime.timedelta(microseconds=1)- event["startDatetime"]
            print("@@@@@",event["summary"], duration)

            enumerated_event = {
                "summary": event["summary"],
                "startDatetime": event["startDatetime"],
                "endDatetime": event["startDatetime"] + datetime.timedelta(1) - datetime.timedelta(microseconds=1),
                "isMultiday": True,
                "isUpdated": event["isUpdated"]}
            enumerated_event_list.append(enumerated_event)

            for date in [event["startDatetime"] + datetime.timedelta(i) for i in range(1, duration.days)]:
                enumerated_event = {
                    "summary": "&nbsp;",
                    "startDatetime": date,
                    "endDatetime": date + datetime.timedelta(1) - datetime.timedelta(microseconds=1),
                    "isMultiday": True,
                    "isUpdated": event["isUpdated"]}
                last_date = date
                enumerated_event_list.append(enumerated_event)
            
            if duration.seconds + duration.microseconds > 0:
                enumerated_event = {
                    "summary": "&nbsp;",
                    "startDatetime": last_date + datetime.timedelta(1),
                    "endDatetime": event["endDatetime"],
                    "isMultiday": True,
                    "isUpdated": event["isUpdated"]}
                enumerated_event_list.append(enumerated_event)

        else:
            enumerated_event_list.append(event)

    return enumerated_event_list


def calculate_number_of_days(event_list: list) -> list:
    for event in event_list:
        if event["isMultiday"]:
            days_spanned = event["endDatetime"] + datetime.timedelta(microseconds=1) - event["startDatetime"]
            days_spanned += 1 if days_spanned.seconds + days_spanned.microseconds > 0 else 0
            event["days_spanned"] = days_spanned


def assign_lanes(event_list: list) -> list:
    multiday_event_list = [event for event in event_list if event["isMultiday"]]
    multiday_event_list = sorted(multiday_event_list, key="days_spanned")
    longest_event = max(event["days_spanned"] for event in event_list)
    calendar = {}
    for i in range(longest_event, -1):
        same_length_events = [event for event in event_list if event["days_spanned"] == i]
        same_length_events = sorted(same_length_events, key="startDatetime")
        for event in same_length_events:
            for date in (event["startDatetime"].date + datetime.timedelta(n) for n in range(i)):
                if date in calendar:
                    calendar[date] += 1
                else:
                    calendar[date] = 0














def generate_all_day_event_for_today_if_today_falls_between_multiday_event(event_list: list) -> list:
    modified_event_list = []
    today = datetime.datetime.now().date()
    for event in event_list:
        if event["isMultiday"]:
            if event["startDatetime"].date() <= today <= event["endDatetime"].date():
                modified_event = event.copy()
                modified_event["startDatetime"] = datetime.datetime(today.year, today.month, today.day)
                modified_event["endDatetime"] = datetime.datetime(today.year, today.month, today.day, 23, 59, 59)
                modified_event["allday"] = True
                modified_event_list.append(modified_event)

        modified_event_list.append(event)

    return modified_event_list


today = datetime.datetime.now().date()
multiday_event = [
    {'summary': "Sleepover at Vicky's",
     'allday': False,
     'startDatetime': datetime.datetime(today.year - 1, 2, 24, 10, 0),
     'endDatetime': datetime.datetime(today.year + 1, 3, 1, 10, 30),
     'isUpdated': False,
     'isMultiday': True}
]


def test_should_return_same_input_if_no_multiday_event():
    event_list = [
        {'summary': "Sleepover at Vicky's",
         'allday': False,
         'startDatetime': datetime.datetime(2022, 2, 24, 10, 0),
         'endDatetime': datetime.datetime(2022, 2, 24, 10, 30),
         'isUpdated': False,
         'isMultiday': False}
    ]
    assert generate_all_day_event_for_today_if_today_falls_between_multiday_event(event_list) == event_list


def test_should_return_event_with_start_datetime_of_today():
    assert generate_all_day_event_for_today_if_today_falls_between_multiday_event(multiday_event)[0][
               "startDatetime"] == datetime.datetime(today.year, today.month, today.day)


def test_multiday_event_returns_two_events():
    assert len(generate_all_day_event_for_today_if_today_falls_between_multiday_event(multiday_event)) == 2
