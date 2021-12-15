import numpy as np
import datetime
import matplotlib.pyplot as plt


def read_data_from_line(line):
    "Read date, time, temperature and humidity from a line of the data file."
    datestemp = datetime.date.fromisoformat(line[2:12])
    timestemp = datetime.time.fromisoformat(line[13:21])
    temperature = float(line.split(",")[1][1:-1])
    humidity = float(line.split(",")[2][1:-3])
    datetimestemp = datetime.datetime.combine(datestemp, timestemp)
    return datetimestemp, temperature, humidity


datetime_values = []
temperature = []  # (°C)
humidity = []  # (%)

# read the date and time as well as temperature and humidity
with open(
    r"C:\Users\Benja\Documents\Git\IOT\humidity_sensor\test\Test_how_t_and_h_changes\Bad_Fenster_Reminder.csv",
    "r",
) as file:
    for line in file:
        d, t, h = read_data_from_line(line)
        datetime_values.append(d)
        temperature.append(t)
        humidity.append(h)

# create plot layout and plot data from file
fig, [ax1, ax2] = plt.subplots(nrows=2)
ax1.set_ylabel('Temperature (°C)')
ax2.set_ylabel('Humidity (%)')
ax2.set_xlabel('Datetime')
ax1.plot(datetime_values, temperature, color='red')
ax2.plot(datetime_values, humidity, color='blue')

# analog timestemps 
showerstart = datetime.datetime(year=2021, month=12, day=14, hour=20-1, minute=49)
shower_fenster_open = datetime.datetime(year=2021, month=12, day=14, hour=20-1, minute=58)
shower_fenster_closed = datetime.datetime(year=2021, month=12, day=14, hour=21-1, minute=29)

fenster_open = datetime.datetime(year=2021, month=12, day=15, hour=10-1, minute=0)
fenster_closed = datetime.datetime(year=2021, month=12, day=15, hour=10-1, minute=23)

# include analog data in plot
for value in [showerstart, shower_fenster_open, shower_fenster_closed,]:
    ax1.vlines(value, ymin=17, ymax=22, color='black')
    ax2.vlines(value, ymin=50, ymax=100, color='black')

for value in [fenster_open, fenster_closed]:
    ax1.vlines(value, ymin=17, ymax=22, color='black', linestyle='--')
    ax2.vlines(value, ymin=50, ymax=100, color='black', linestyle='--')



# Test, ob man in Ableitung mehr erkennen kann

fig_abl, [ax1_abl, ax2_abl] = plt.subplots(nrows=2)

ax1_abl.plot(datetime_values[:-1], np.diff(np.array(temperature)), color='red')
ax2_abl.plot(datetime_values[:-1], np.diff(np.array(humidity)), color='blue')

plt.show(block=True)