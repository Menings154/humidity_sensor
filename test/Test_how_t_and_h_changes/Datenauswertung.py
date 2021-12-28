import numpy as np
import datetime
import matplotlib.pyplot as plt
import math


def read_data_from_line(line):
    "Read date, time, temperature and humidity from a line of the data file."
    datestemp = datetime.date.fromisoformat(line[2:12])
    timestemp = datetime.time.fromisoformat(line[13:21])
    temperature = float(line.split(",")[1][1:-1])
    humidity = float(line.split(",")[2][1:-3])
    datetimestemp = datetime.datetime.combine(datestemp, timestemp)
    return datetimestemp, temperature, humidity

def window_status(list_d:list, list_t:list, list_h:list, t_percentage:float, h_percentage:float, time_after_h:float):
    """
    Prototpye for later logic to detect if window is open or not.
    
    Plan:
        Go through all datapoints, make sliding average with an hour width
        if humidity rising, look for temperature sinking, then window open because of shower.
        if temperature diff is larger than a defined percent value without humidity rising, window open only for smell.
    """
    delta_time = (list_d[1]-list_d[0]).total_seconds()  # time between two measurement points

    temp_t = []
    temp_h = []

    window_opened_d = []
    window_opened_t = []
    window_opened_h = []
    
    shower_d = []
    shower_t = []
    shower_h = []

    for count, value in enumerate(list_d):
        if len(temp_t) >= 60:
            temp_t.pop(0)
            temp_h.pop(0)
        
        temp_t.append(list_t[count])
        temp_h.append(list_h[count])
        if list_h[count] >= np.mean(temp_h)*h_percentage:  # is humidity rising (indication of showering)
            for i in range(math.ceil(time_after_h/delta_time)):
                if list_t[count+i] < np.mean(temp_t)*t_percentage:
                    shower_d.append(list_d[count+i])
                    shower_t.append(list_t[count+i])
                    shower_h.append(list_h[count+i])
                else:
                    pass

        else:
            if list_t[count] < np.mean(temp_t)*t_percentage:
                if list_d[count] not in shower_d:
                    window_opened_d.append(value)
                    window_opened_t.append(list_t[count])
                    window_opened_h.append(list_h[count])

    return shower_d, shower_t, shower_h, window_opened_d, window_opened_t, window_opened_h

    

datetime_values = []
temperature = []  # (°C)
humidity = []  # (%)

# read the date and time as well as temperature and humidity
try:
    with open(
        r"C:\Users\Benja\Documents\Git\IOT\humidity_sensor\test\Test_how_t_and_h_changes\Bad_Fenster_Reminder.csv",
        "r",
    ) as file:
        for line in file:
            d, t, h = read_data_from_line(line)
            datetime_values.append(d)
            temperature.append(t)
            humidity.append(h)

except FileNotFoundError:
    with open(
        r"/home/menings/Documents/Git/humidity_sensor/test/Test_how_t_and_h_changes/Bad_Fenster_Reminder.csv",
        "r"
    ) as file:
        for line in file:
            d, t, h = read_data_from_line(line)
            datetime_values.append(d)
            temperature.append(t)
            humidity.append(h)

# create plot layout and plot data from file
plt.close('all')
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


shower_d, shower_t, shower_h, window_d, window_t, window_h = window_status(datetime_values, temperature, humidity, 0.9, 1.1, 6000)

ax1.scatter(shower_d, shower_t, color='yellow')
ax1.scatter(window_d, window_t, color='pink')

ax1.hlines(np.mean(temperature), xmin=datetime_values[0], xmax=datetime_values[-1], color='black')
ax2.hlines(np.mean(humidity), xmin=datetime_values[0], xmax=datetime_values[-1], color='black')
plt.show(block=True)

