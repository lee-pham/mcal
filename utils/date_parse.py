import datetime


def generate_all_day_event_for_today_if_today_falls_between_multiday_event(event: dict):
    if event["startDatetime"].date() <= datetime.datetime.now().date() <= event["endDatetime"].date():
        return True


def test_should_return_true():
    assert generate_all_day_event_for_today_if_today_falls_between_multiday_event(
        {'summary': "Sleepover at Vicky's", 'allday': False,
         'startDatetime': datetime.datetime(2022, 2, 24, 10, 0),
         'endDatetime': datetime.datetime(2022, 3, 1, 10, 30),
         'updatedDatetime': datetime.datetime(2022, 2, 27, 1, 41, 32, 87000),
         'isUpdated': False,
         'isMultiday': True}
    )
