"""
This project is designed for the WaveShare 12.48" eInk display. Modifications will be needed for other displays,
especially the display drivers and how the image is being rendered on the display. Also, this is the first project that
I posted on GitHub so please go easy on me. There are still many parts of the code (especially with timezone
conversions) that are not tested comprehensively, since my calendar/events are largely based on the timezone I'm in.
There will also be work needed to adjust the calendar rendering for different screen sizes, such as modifying of the
CSS stylesheets in the "render" folder.
"""
import datetime as dt
import json
import logging
import platform
import sys

from pytz import timezone

from gcal.gcal import GcalHelper
from render.render import RenderHelper
from utils.date_parse import enumerate_multiday_event


def main():
    # Only drive the EPD when running on Raspberry Pi
    is_rpi = platform.system() == "Linux"

    # Basic configuration settings (user replaceable)
    configFile = open('config.json')
    config = json.load(configFile)

    # list of timezones - print(pytz.all_timezones)
    displayTZ = timezone(config['displayTZ'])
    # considers events updated within last 12 hours as recently updated
    thresholdHours = config['thresholdHours']
    # limits number of events to display (remainder displayed as '+X more')
    maxEventsPerDay = config['maxEventsPerDay']
    # set to true when debugging rendering without displaying to screen
    isDisplayToScreen = config['isDisplayToScreen']
    # set to true to conserve power, false if in debugging mode
    isShutdownOnComplete = config['isShutdownOnComplete']
    # 0: do not show / 1: always show / 2: show when battery is low
    batteryDisplayMode = config['batteryDisplayMode']
    weekStartDay = config['weekStartDay']  # Monday = 0, Sunday = 6
    dayOfWeekText = config['dayOfWeekText']  # Monday as first item in list
    # Width of E-Ink display. Default is landscape. Need to rotate image to fit.
    screenWidth = config['screenWidth']
    # Height of E-Ink display. Default is landscape. Need to rotate image to fit.
    screenHeight = config['screenHeight']
    # Width of image to be generated for display.
    imageWidth = config['imageWidth']
    # Height of image to be generated for display.
    imageHeight = config['imageHeight']
    # If image is rendered in portrait orientation, angle to rotate to fit screen
    rotateAngle = config['rotateAngle']
    calendars = config['calendars']  # Google calendar ids
    is24hour = config['is24h']  # set 24 hour time
    weeks_to_display = config["weeks_to_display"]  # num of weeks to display after the previous sunday of the month

    # Create and configure logger
    logging.basicConfig(filename="logfile.log",
                        format='%(asctime)s %(levelname)s - %(message)s', filemode='a')
    logger = logging.getLogger('maginkcal')
    logger.addHandler(logging.StreamHandler(
        sys.stdout))  # print logger to stdout
    logger.setLevel(logging.INFO)
    logger.info("Starting daily calendar update")

    try:
        # Establish current date and time information
        # Note: For Python datetime.weekday() - Monday = 0, Sunday = 6
        # For this implementation, each week starts on a Sunday and the calendar begins on the nearest elapsed Sunday
        # The calendar will also display 5 weeks of events to cover the upcoming month, ending on a Saturday

        currDatetime = dt.datetime.now(displayTZ)
        current_time = currDatetime.strftime("%H:%M")
        logger.info("Time synchronised to {}".format(currDatetime))
        currDate = currDatetime.date()
        current_month_date = dt.datetime(currDate.year, currDate.month, 1).date()
        calStartDate = current_month_date - dt.timedelta(days=((current_month_date.weekday() + (7 - weekStartDay)) % 7))
        calEndDate = calStartDate + dt.timedelta(days=(weeks_to_display * 7 - 1))

        # Dates used for testing ##########################
        # calStartDate = dt.datetime(2022, 3, 27).date()  #
        # calEndDate = dt.datetime(2022, 4, 30).date()    #
        ###################################################
        calStartDatetime = displayTZ.localize(
            dt.datetime.combine(calStartDate, dt.datetime.min.time()))
        calEndDatetime = displayTZ.localize(
            dt.datetime.combine(calEndDate, dt.datetime.max.time()))

        # Using Google Calendar to retrieve all events within start and end date (inclusive)
        start = dt.datetime.now()
        gcalService = GcalHelper()
        eventList = gcalService.retrieve_events(
            calendars,
            calStartDatetime,
            calEndDatetime,
            displayTZ,
            thresholdHours)
        enumerated_event_list = enumerate_multiday_event(eventList)
        # enumerated_event_list = eventList
        logger.info("Calendar events retrieved in " +
                    str(dt.datetime.now() - start))

        # Populate dictionary with information to be rendered on e-ink display
        calDict = {'events': enumerated_event_list, 'calStartDate': calStartDate, 'calEndDate': calEndDate,
                   'today': currDate, 'lastRefresh': currDatetime,
                   'batteryDisplayMode': batteryDisplayMode,
                   'dayOfWeekText': dayOfWeekText, 'weekStartDay': weekStartDay, 'maxEventsPerDay': maxEventsPerDay,
                   'is24hour': is24hour, "current_time": current_time, "weeks_to_display": weeks_to_display}
        renderService = RenderHelper(imageWidth, imageHeight, rotateAngle)
        calBlackImage, calRedImage = renderService.process_inputs(calDict)

        if is_rpi:
            from display.display import DisplayHelper
            displayService = DisplayHelper(screenWidth, screenHeight)
            if currDate.weekday() == weekStartDay:
                # calibrate display once a week to prevent ghosting
                # to calibrate in production
                displayService.calibrate(cycles=0)
            displayService.update(calBlackImage, calRedImage)
            displayService.sleep()

    except Exception as e:
        logger.error(e, exc_info=True)

    logger.info("Completed daily calendar update")


if __name__ == "__main__":
    main()
