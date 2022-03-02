import datetime


def generate_all_day_event_for_today_if_today_falls_between_multiday_event(event_list: list) -> list:
    modified_event_list = []
    today = datetime.datetime.now().date()
    for event in event_list:
        if event["isMultiday"]:
            if event["startDatetime"].date() <= today <= event["endDatetime"].date():
                modified_event = event.copy()
                modified_event["startDatetime"] = datetime.datetime(today.year, today.month, today.day)
                modified_event["endDatetime"] = datetime.datetime(today.year, today.month, today.day, 22, 00)
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
