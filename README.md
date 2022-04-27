# Magic Calendar

![Magic Calendar](mcal.png)

## Hardware Required

- [Raspberry Pi](https://www.raspberrypi.org) - Header pins are needed to connect to the E-Ink
  display
- [Waveshare 12.48" Tri-color E-Ink Display](https://www.waveshare.com/product/12.48inch-e-paper-module-b.htm) -
  Unfortunately out of stock at the time this is published, so I adapted the code to work with the [7.5" Display](https://www.waveshare.com/7.5inch-e-paper-hat-b.htm)

## Some features of the calendar:

- Since I had the luxury of using red for the E-Ink display, I used it to highlight the current date, as well as
  recently added/updated events.
- Given limited space (oh why are large E-Ink screens still so expensive!) and resolution on the display, I could only
  show 3 events per day and an indicator (e.g. 4 more) for those not displayed
- The calendar always starts from the current week, and displays the next four (total 35 days). If the dates cross over
  to the new month, it's displayed in grey instead of black.
- Timeline added to the bottom to closely honor the [original concept](https://www.youtube.com/watch?v=2KDkFgOHZ5I)


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
sudo apt install chromium
```

4. Download the over the files in this repo to a folder in your PC first.

5. In order for you to access your Google Calendar events, it's necessary to first grant the access. Follow
   the [instructions here](https://developers.google.com/calendar/api/quickstart/python) on your PC to get the
   credentials.json file from your Google API. Don't worry, take your time. I'll be waiting here.

6. Once done, copy the credentials.json file to the "gcal" folder in this project. Run the following command on your PC.
   A web browser should appear, asking you to grant access to your calendar. Once done, you should see a "token.pickle"
   file in your "gcal" folder.

```bash
python3 quickstart.py
```

7. Copy all the files over to your RPi using your preferred means.

9. In the repository, run
```bash
pip install -r requirements.txt
```

9. Run the following command in the RPi Terminal to open crontab.

```bash
crontab -e
```

10. Specifically, add the following command to crontab so that the MagInkCal Python script runs each time the RPi is
    booted up.

```bash
@reboot cd /location/to/your/maginkcal && python3 maginkcal.py
```

11. That's it!

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
