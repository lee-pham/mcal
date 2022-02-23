import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime

# In case the above fails, e.g. because of missing internet connection
# use the following lists as fallback.
names = ["", "Dentist", "Lunch", "Pottery", "Lee", ""]

dates = [0, 800, 1200, 1800, 2200, 2400]

current_time = datetime.now().

# Convert date strings (e.g. 2014-10-18) to datetime
# dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
dates = [d for d in dates]

# Choose some nice levels
# levels = np.tile([1, 1, 1, 1, 1, 1],
#                  int(np.ceil(len(dates) / 6)))[:len(dates)]

# Create figure and plot a stem plot with the date
fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)

# ax.vlines(dates, 0, levels, color="tab:red")  # The vertical stems.
ax.plot(dates, np.zeros_like(dates), "-o",
        color="k", markerfacecolor="w")  # Baseline and markers on it.

# plt.xlim([0, 2400])

# annotate lines
for i, txt in enumerate(names):
    ax.annotate(txt, (dates[i], .005))

# format xaxis with 4 month intervals
# ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
# ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# remove y axis and spines
ax.yaxis.set_visible(False)
ax.spines[["left", "top", "right"]].set_visible(False)

ax.margins(y=0.1)
plt.show()
