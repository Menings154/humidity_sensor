from dataclasses import dataclass
import typing
import datetime as dt

datalist = list[float]


@dataclass
class Data:
    filename: str
    date: list = None
    temperature: list = None
    humidity: list = None

    def read_data(self):
        """
        Reads the data in the file with the filename needed for creation of the class.

        The file should be a csv-file with lines with following structure:
        ["datetime","temperature","humidity"]
        """
        self.date = []
        self.temperature = []
        self.humidity = []
        with open(self.filename, "r") as file:
            for line in file:
                self.date.append(
                    dt.datetime.combine(
                        dt.date.fromisoformat(line[2:12]),
                        dt.time.fromisoformat(line[13:21]),
                    )
                )
                self.temperature.append(float(line.split(",")[1][1:-1]))
                self.humidity.append(float(line.split(",")[2][1:-3]))


test = Data(
    filename=r"C:\Users\Benja\Documents\Git\IOT\humidity_sensor\test\Test_how_t_and_h_changes\Bad_Fenster_Reminder2.csv"
)
print(test.temperature)
test.read_data()
print(test.temperature)
