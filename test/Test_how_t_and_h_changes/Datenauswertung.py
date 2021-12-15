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

fig, [ax1, ax2] = plt.subplots(nrows=2)
ax1.set_yaxis('Temperature (°C)')
ax2.set_yaxis('Humidity (%)')
ax2.set_xaxis('Datetime')
ax1.plot(datetime_values, temperature, color='red')
ax2.plot(datetime_values, humidity, color='blue')
plt.show(block=True)
