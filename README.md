# Magic Calendar

# TODO:

## Bugs

- [x] if current day of multiday event is between the start and end day, event does not show up on timeline
- [ ] Fix ordering of multiday events in calendar view

## UI

### Calendar

- [x] year and time font need to be slightly smaller than the calendar day font
- [x] overflow in red, event in gray
- [x] long line for multi day events
- [x] multiday line in red
- [ ] increase width between columns
- [ ] noto serif
- [ ] roboto slab
- [ ] bitter (font)
- [ ] bullet point is all day event indicator for single day

### Timeline

- [x] thinner line for timeline line
- [x] filled black circle while event is going on
- [x] all day event as 00:00 event
- [x] all day multi day italics surrounded by bullet
- [x] all day single day is italics no bullet
- [ ] text start aligns with dot
- [ ] fix overlapping as it's not perfected yet

## Hardware Required

- [Raspberry Pi Zero WH](https://www.raspberrypi.org/blog/zero-wh/) - Header pins are needed to connect to the E-Ink
  display
- [Waveshare 12.48" Tri-color E-Ink Display](https://www.waveshare.com/product/12.48inch-e-paper-module-b.htm) -
  Unfortunately out of stock at the time this is published

## Some features of the calendar:

- Since I had the luxury of using red for the E-Ink display, I used it to highlight the current date, as well as
  recently added/updated events.
- Given limited space (oh why are large E-Ink screens still so expensive!) and resolution on the display, I could only
  show 3 events per day and an indicator (e.g. 4 more) for those not displayed
- The calendar always starts from the current week, and displays the next four (total 35 days). If the dates cross over
  to the new month, it's displayed in grey instead of black.

![MagInkCal Basics](https://user-images.githubusercontent.com/5581989/134775456-d6bacaca-03c7-4357-af28-7c06aa19ed90.png)

## Setting Up Raspberry Pi Zero

1. Start by flashing [Raspberrypi OS Lite](https://www.raspberrypi.org/software/operating-systems/) to a MicroSD Card.

2. After setting up the OS, run the following commmand in the RPi Terminal, and use
   the [raspi-config](https://www.raspberrypi.org/documentation/computers/configuration.html) interface to setup Wifi
   connection, enable SSH, I2C, SPI, and set the timezone to your location.

```bash
sudo raspi-config
```

3. Run the following commands in the RPi Terminal to setup the environment to run the Python scripts.

```shell
sudo apt install chromium????
```

6. Download the over the files in this repo to a folder in your PC first.

7. In order for you to access your Google Calendar events, it's necessary to first grant the access. Follow
   the [instructions here](https://developers.google.com/calendar/api/quickstart/python) on your PC to get the
   credentials.json file from your Google API. Don't worry, take your time. I'll be waiting here.

8. Once done, copy the credentials.json file to the "gcal" folder in this project. Run the following command on your PC.
   A web browser should appear, asking you to grant access to your calendar. Once done, you should see a "token.pickle"
   file in your "gcal" folder.

```bash
python3 quickstart.py
```

9. Copy all the files over to your RPi using your preferred means.

10. Run the following command in the RPi Terminal to open crontab.

```bash
crontab -e
```

11. Specifically, add the following command to crontab so that the MagInkCal Python script runs each time the RPi is
    booted up.

```bash
@reboot cd /location/to/your/maginkcal && python3 maginkcal.py
```

12. That's all! Your Magic Calendar should now be refreshed at the time interval that you specified in the PiSugar2 web
    interface!

PS: I'm aware that the instructions above may not be complete, especially when it comes to the Python libraries to be
installed, so feel free to ping me if you noticed anything missing and I'll add it to the steps above.

## Acknowledgements
- [MagInkCal](https://github.com/speedyg0nz/maginkcal): Built out the initial concept and is the backbone of this code
- [Quattrocento Font](https://fonts.google.com/specimen/Quattrocento): Font used for the calendar display
- [Bootstrap Calendar CSS](https://bootstrapious.com/p/bootstrap-calendar): Stylesheet that was adapted heavily for the
  calendar display
- [emagra](https://github.com/emagra): For adding in new features, such as 24hr display and multiple calendar selection.
- [/u/aceisace](https://www.reddit.com/user/aceisace/): For the tips on E-Ink development and
  the [InkyCal](https://github.com/aceisace/Inkycal) repo (worth checking out even though I didn't use it for this
  project).
