import wordjam
import csv
import time
from dateutil import parser
import action
reload(wordjam)
reload(action)

game = wordjam
notif_sheet = ""

class Test:
    def __init__(self, driver):
        self.driver = driver
        self.game = game.Game(driver)
        self.action = action.Action(driver)
        self._link_game_action()
        #self.notif_csv_input = "/Users/fazilmajeeth/Downloads/notif_testing.csv"
        #self.test_notif_list = self.load_input_csv(self.notif_csv_input)

    def _link_game_action(self):
        self.game.action = self.action
        self.action.game = self.game

    def load_input_csv(self, file_path):
        notif_list = {}

        with open(file_path) as f_name:
            counter = 0
            reader = csv.DictReader(f_name, delimiter=',')
            for line in reader:
                notif_list[counter] = line
                counter += 1
        return notif_list

    def get_notif_for_day(self, day):
        notif_for_day = {}
        counter = 0
        for t in self.test_notif_list:
            check_notif = self.test_notif_list[t]
            if int(check_notif["days"]) == day:
                notif_for_day[counter] = check_notif
                counter += 1
        return notif_for_day

    def check_notif_for_current_day(self, start_time, end_time, notif_name, launch_app, app_launch_time):
        notif = []
        current_date = parser.parse(self.game.get_device_clock_string()).day
        while parser.parse(end_time).hour <= parser.parse(self.game.get_device_clock_string()).hour:
            self.game.add_hours(1)
            if parser.parse(self.game.get_device_clock_string()).day != current_date:
                current_date = parser.parse(self.game.get_device_clock_string()).day
                break

        while (parser.parse(self.game.get_device_clock_string()).day == current_date and parser.parse(self.game.get_device_clock_string()).hour <= parser.parse(end_time).hour):
            current_datetime = parser.parse(self.game.get_device_clock_string())
            # If time is between given lookup time range
            if current_datetime.hour >= parser.parse(start_time).hour and current_datetime.hour <= parser.parse(end_time).hour:
                self.game.open_notification_panel()
                self.game.add_minutes(20)
                # If notif is shown
                if self.game.is_jam_notif_shown():
                    if launch_app:
                        self.game.get_notifications_shown()
                        notif.append(self.game.click_on_jam_notif())
                        time.sleep(10)
                        self.driver.press_keycode(187)
                        time.sleep(2)
                        self.driver.press_keycode(67)
                        time.sleep(2)
                        self.driver.press_keycode(3)
                        self.game.open_notification_panel()
                time.sleep(3)
            # In time range outside lookup time
            else:
                self.game.add_hours(1)
                self.game.open_notification_panel()
                if self.game.is_jam_notif_shown():
                    notif.append(self.game.get_notifications_shown())
                time.sleep(1)
        print "result", notif

    def run_days(self):
        test_notif_list = self.test_notif_list
        current_day_number = 1
        for t in test_notif_list:
            print test_notif_list[t]
            day_number = test_notif_list[t]["days"]
            start_time = test_notif_list[t]["start_time"]
            end_time = test_notif_list[t]["end_time"]
            notif_name = test_notif_list[t]["notif_name"]
            launch_app = test_notif_list[t]["launch_app"]
            app_launch_time = test_notif_list[t]["app_launch_time"]
            self.check_notif_for_current_day(start_time, end_time,  notif_name, launch_app, app_launch_time)
            current_day_number += 1





