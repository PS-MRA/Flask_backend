import json
from appium.webdriver.common.touch_action import TouchAction
import time
import requests
import random
from dateutil import parser
import subprocess
from datetime import timedelta
import csv
import unicodedata
import util
import screenshot
import os
import copy
from threading import Thread
import constants as const
import ws_conn
tt=0
#import googlesheets
reload(util)
reload(screenshot)
reload(const)
reload(ws_conn)
#reload(googlesheets)

input_csv = "screen_condition.csv"

class Game():
    def __init__(self, driver):
        self.driver = driver
        self.util = util.Util(driver)
        screen_size = self.driver.get_window_size()
        self.height = float(screen_size["height"])
        self.width = float(screen_size["width"])
        self.magic_json = None
        self.puzzle_completed = None
        self.current_screen = None
        self.core_element_map = {}
        self.game_obj = None
        self.user_obj = None
        self.runtime_config = None
        self.experiments = None
        self.qa_logs = None
        self.qa_logs_grouped = None
        self.last_updated = 0
        self.to_remove = []
        #self.core, self.core_element_map = self.import_test_csv()
        #self.csvrow = self.import_test_csv()
        self.sprite_elements = ["button", "icon", "image", "toggle"]
        self.string_elements = ["text", "number"]
        self.qa_logs_header = {"index", "xPos", "yPos", "visible", "spriteName", "string", "fontType", "fontName", "zOrder", "screen"}
        self.type_button = ["Button"]
        self.type_text = ["LabelBMFont", "LabelTTF"]
        self.type_image = ["Sprite", "Scale9Sprite"]
        self.separator = "--"
        self.clicked_elements = {}
        #self.googlesheets = googlesheets
        self.step = 1
        self.skip = 1
        self.record_batch_length = 10
        self.record_batch = []
        self.record_batch_back1 = []
        self.action = None
        self.const = const
        self.ws = ws_conn.ws(const.WS_URL, 3)

        # Load main puzzle json
        with open(const.PUZZLE_JSON_MAIN) as f:
            self.puzzle_json_data = json.load(f)
        # Load daily puzzle json
        with open(const.DAILY_PUZZLE_JSON) as f:
            self.daily_puzzle_json_data = json.load(f)

        with open(const.DICTIONARY_FILE, "r") as f:
            filetext = f.read()
            self.dictionary = filetext.split(",")

        self.update_log_location = "local"

        self.run_name = None
        self.play_run_name = None
        self.play_run_data = []
        self.playback_run_data = []
        self.is_ftue_shown = False

        #Record variables init
        self.screenshots_path = None
        self.ss = None
        self.bot_log = None


    def load_game(self, game_obj):
        """
         Used to bind the action.py to the game from the terminal
        :param game_obj: instance of the action.py
        :return: Binds the instance of the action.py to self.action
        """
        self.action = game_obj

    def scratch(self, x, y):
        """
        Used to perform the scratch action on in purchase screen
        :param x: x-coordinate of the scratch card -generally it is the middle point of the scratch card
        :param y: y-coordinate of the scratch card
        :return: no return
        """
        for x in range(0,4):
            play = TouchAction(self.driver)
            play.press(x=x-200,y=y)
            play.move_to(x=x+400,y=y)
            play.release().perform()

    def load_magic_logs_if_empty(self):
        """
        get_magic_logs() if logs is empty
        """
        if self.magic_json is None:
            self.get_magic_logs()

    def record_run(self, name=None):
        """
        Use to start the recording.
        Basically it makes a file in the current dir and inside it two files i.e screenshort and botlog.csv
        and record all the action which is performed once the connection is established till the connection is broken.
        :param name: if none the ask for new file name:
                    ELSE the file name in string format eg s="xyz"
        """
        if name is None:
            self.run_name = raw_input("Enter run name: ")
        else:
            self.run_name = name
        if not os.path.exists(self.run_name):
            os.makedirs(self.run_name + "/" + const.SCREENSHOTS_PATH)
        self.screenshots_path = self.run_name + "/" + const.SCREENSHOTS_PATH
        self.bot_log = self.run_name + "/" + const.BOT_LOG_FILE_NAME
        const.BOT_LOG_FILE_PATH = self.bot_log
        print "check here faz " + const.BOT_LOG_FILE_PATH
        self.ss = screenshot.Screenshot(self.driver, self.screenshots_path)

    def play_run(self, runname=None):
        """
        play the recorded steps in botlog.csv
        param runname : if None then ask for the filename
                        else the name of the file in string form eg s="xyz"
        """

        run_list = [name for name in os.listdir(".") if os.path.isdir(name)]
        if runname is None:
            self.play_run_name = raw_input("Enter run name to play: ")
        else:
            self.play_run_name = runname

        print self.play_run_name

        if self.play_run_name not in run_list:
            print ("Please choose a run name from below list to start playing")
            print run_list
            self.play_run()
        else:
            self.load_play_run(self.play_run_name)
            self.play_run_name = str(int(time.time())) + "_" + self.play_run_name
            if not os.path.exists(self.play_run_name):
                os.makedirs(self.play_run_name + "/" + const.SCREENSHOTS_PATH)
            self.screenshots_path = self.play_run_name + "/" + const.SCREENSHOTS_PATH
            self.bot_log = self.play_run_name + "/" + const.BOT_LOG_FILE_NAME
            const.BOT_LOG_FILE_PATH = self.bot_log
            self.ss = screenshot.Screenshot(self.driver, self.screenshots_path)


    def load_play_run(self, play_run_name):
        """
        return : the basic recorded steps to Action.export_results()
        parm  play_run_name : file name from where to take the recorded steps
        """

        self.play_run_data = []
        bot_file_path = play_run_name + "/" + "botlog.csv"
        with open(bot_file_path, mode='r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                self.play_run_data.append(row)
        return self.play_run_data

    def load_playback_run(self, playback_run_name):

        self.playback_run_data = []
        bot_file_path = playback_run_name + "/" + "botlog.csv"
        with open(bot_file_path, mode='r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                self.playback_run_data.append(row)
        return self.playback_run_data


    def qa_log_readable(self):
        """
        Prints readable qalogs.

        Print all visible objects in current screen.
        """
        self.load_magic_logs_if_empty()
        if self.qa_logs is None:
            print "error", "No qa_logs available for current screen"
            return False
        for log in self.qa_logs:
            for k, v in log.items():
                if k in self.qa_logs_header:
                    self.log(k, v)
        return True

    def get_current_screen(self, reload=True):
        """Returns current screen name

        :param reload: It True, reloads updated magic logs
        :return: Current screen name string
        """
        if reload:
            self.get_magic_logs()
        else:
            self.load_magic_logs_if_empty()
        return self.current_screen

    @staticmethod
    def import_test_csv():

        """Imports test steps from google sheets

        Not used now
        TODO: Fix sheetname and format to rerun botlogs
        """
        rows = googlesheets.main()
        headers = ["type", "screen", "element", "images", "labels"]
        csv_data = []

        for r in rows:
            if len(r) == 0:
                break
            row_map = {}
            for i in range(0, len(headers)):
                try:
                    row_map[headers[i]]  = r[i]
                except:
                    row_map[headers[i]] = ""
                    pass
            csv_data.append(row_map)

        return csv_data

    def tap(self, x, y, take_snap=True, element_name=None, element_type=None):

        """
        Performs tap action on given x, y
        Saves screenshot if take_snap is True
        :param x: X cordinate
        :param y: Y cordinates
        :param take_snap: if True, save screenshot after tap
        :return: bool
        parameter style : X=10&Y=10
        """
        try:
            # TODO: make notch height as generic
            self.driver.tap([(x, y+60)])
        except:
            os.system("adb shell input tap " + str(x) + " " + str(y))

    def log(self, tag, message):
        """
        Saves logs in required format

        TODO: Save it to logs file. Change the format and use it instead of all print statement
        :param tag: log type tag name
        :param message: log message
        """
        print tag, " : ", message

    def is_fb_login_shown(self, wait):
        """
        Check if fb login webview is visible currently
        :param wait: Wait time if any error occurs while looking for fb login view
        :return: bool
        """
        wait_time = time.time() + wait
        while True:
            try:
                login_form = self.driver.find_elements_by_xpath(const.FB_LOGIN_WEBVIEW_ANDROID)
                #print(login_form)
                if len(login_form) > 0:
                    return True
                return False
            except:
                if time.time() >= wait_time:
                    return False
                continue

    def group_qa_logs(self):
        """
        Group qa_logs into three categories.
        BUTTONS, IMAGES, LABELS

        BUTTONS - Buttons list along with text and images positioned inside the button
        IMAGES - Images list along with text positioned inside the sprite image
        LABELS - Labels list which are not part of above two category
        :return: Grouped elements list with keyword BUTTONS, IMAGES, LABELS
        """
        self.load_magic_logs_if_empty()
        if self.qa_logs is None:
            self.log("ERROR", "No magic logs available")
            return False
        button_list = []
        text_list = []
        text_list_removed = []
        image_list = []
        image_list_removed = []
        # Segregating button type, image type and text type
        self.is_ftue_shown = False
        for ql in self.qa_logs:
            #print("in group qa_logs")
            #print(ql)
            try:
                ql_el_type = ql["elementType"]
            except:
                continue
            try:
                if "ftue" in ql["name"]:
                    self.is_ftue_shown = True
            except:
                pass
            if ql["elementType"] in self.type_button and const.SCREEN_NAMES[ql["screen"]] == self.current_screen and ql["visible"]:
                ql = self.util.get_box_position(ql)
                button_list.append(ql)
            elif ql["elementType"] in self.type_image and const.SCREEN_NAMES[ql["screen"]] == self.current_screen and ql["visible"]:
                '''new if condition to fix the none problem'''
                if ql["boundbox"]["x"] is not None:
                    ql = self.util.get_box_position(ql)
                    image_list.append(ql)
            elif ql["elementType"]in self.type_text and const.SCREEN_NAMES[ql["screen"]] == self.current_screen and ql["visible"]:
                ql = self.util.get_box_position(ql)
                text_list.append(ql)
        # For every button element, checking if any image or text position is inside button bounding box

        for bl in button_list:
            string_in_button = []
            image_in_button = []
            # Checking every text element one by one, whether it is positioned inside the button box
            for tl in text_list:
                if self.util.is_element_inside_box(bl, tl) and tl["screen"] == bl["screen"] and bl["layerType"] == tl["layerType"]:
                    string_in_button.append(tl)
                    text_list_removed.append(tl)
            bl["strings"] = string_in_button

            # Removing already mapped text
            for tlr in text_list_removed:
                try:
                    text_list.remove(tlr)
                except:
                    pass

            # Checkin every Images element one by one, whether it is positioned inside the button box
            for il in image_list:
                if self.util.is_element_inside_box(bl, il) and il["screen"] == bl["screen"] and bl["layerType"] == il["layerType"]:
                    image_in_button.append(il)
                    image_list_removed.append(il)
            bl["images"] = image_in_button

            # Removing already mapped images
            for ilr in image_list_removed:
                try:
                    image_list.remove(ilr)
                except:
                    pass

        # For every image, checking if any text is positioned inside the image box
        for il in image_list:
            text_in_image = []
            for tl in text_list:
                if self.util.is_element_inside_box(il, tl) and tl["screen"] == il["screen"] and il["layerType"] == tl["layerType"]:
                    text_in_image.append(tl)
                    text_list_removed.append(tl)
            il["strings"] = text_in_image

            # Removing alreday mapped text
            for tlr in text_list_removed:
                try:
                    text_list.remove(tlr)
                except:
                    pass

        grouped_el_list = {
            "BUTTONS" : button_list,
            "LABELS" : text_list,
            "IMAGES" : image_list
        }
        # return button_list + text_list + image_list
        return grouped_el_list

    def print_test_cases(self):
        """
        Print all the informations which are present on the current device screen!
        """
        grouped_el_list = self.group_qa_logs()
        buttons = grouped_el_list["BUTTONS"]
        images = grouped_el_list["IMAGES"]
        labels = grouped_el_list["LABELS"]
        separator = "--"
        for b in buttons:
            image_arr = ""
            string_arr = ""
            for b_image in b["images"]:
                image_arr += str(b_image["name"]) + separator

            for b_string in b["strings"]:
                string_arr += str(b_string["name"]) + separator

            print (b["elementType"], "," , const.SCREEN_NAMES[b["screen"]], ",", b["name"], ",", image_arr, ",",string_arr)

        for i in images:
            string_arr = ""
            for i_string in i["strings"]:
                string_arr += str(i_string["name"]) + separator
            print (i["elementType"], ",", const.SCREEN_NAMES[i["screen"]], ",",i["name"], ",", "", ",", string_arr)

        for l in labels:
            print (l["elementType"], ",", const.SCREEN_NAMES[l["screen"]], ",", l["name"], ",", "", ",", "")

    def get_string_details_only(self, string_elements):
        """
        To be removed
        :param string_elements: 
        :return: 
        """
        if len(string_elements) == 0:
            return None
        string_details = []
        for el in string_elements:
            string_details.append(el["font_name"],el["name"])
        return string_details

    def get_image_details_only(self, string_elements):
        """
        To be removed
        :param string_elements:
        :return:
        """
        if len(string_elements) == 0:
            return None
        image_details = []
        for el in string_elements:
            image_details.append(el["spriteName"])
        return image_details
        return image_details

    def is_target_app_open(self):
        """
        Verify if the target app is open or not
        Check for different scenario of the screen which can be present on the screen
        """
        # Handle google app store buy screen
        if "billing" in self.driver.current_activity:
            print("Billing is active")
            print(self.current_screen)
            self.current_screen = "purchase_confirmation_screen"
            return False
        # Checks if app activity is running active on device
        if self.driver.current_activity != self.driver.desired_capabilities["appActivity"]:
            print("Contra")
            # Check if native share activity is running
            if self.driver.current_activity == "com.android.internal.app.ChooserActivity":
                print("android_native_share")
                self.current_screen = "android_native_share"
                return False
            # Check if FB login webview is shown
            if self.is_fb_login_shown(7):
                print("fb_login_shown")
                self.current_screen = "fblogin"
                self.log("info", "FB login page is being shown")
                return False
            # If above conditions fails, then app is not open at the moment
            print ("info:", "Game is not open at the moment. App running on top is ", self.driver.current_package)
            self.current_screen = "device_home"
            return False
        return True

    def get_magic_logs_old_v1(self, wait=30, launch_target_app=False):
        """
        Read updated magic logs from native view on app

        Performs click on the magic button to get updated logs populated to native view's description value.
        :param wait: Time required to get the updated magic logs after tapping on magic button
        :return: Current screen name string and bool for result
        """
        log_text = None
        target_app_state = self.is_target_app_open()
        if (not target_app_state):
            if launch_target_app:
                #print launch_target_app, target_app_state
                if self.driver.current_package != self.driver.desired_capabilities["appPackage"]:
                    self.log("info", "Target App is not open")
                    self.log("info", "Appium launching app : " + self.driver.desired_capabilities["appPackage"])
                    self.driver.activate_app(self.driver.desired_capabilities["appPackage"])
                    time.sleep(5)
            return self.current_screen, False

        wait_time = time.time() + wait
        log_shown = False
        while time.time() <= wait_time:
            self.tap(self.width / 2, 2, False)
            self.tap(self.width / 2, 2, False)
            self.tap(self.width / 2, 2, False)
            #unicodedata.normalize('NFKD', title).encode('ascii','ignore')
            try:
                log_unicode_string = self.driver.find_element_by_id("android:id/content").get_attribute("content-desc")
            except:
                print "unknown screen"
                self.current_screen = "unknown"
                return self.current_screen, False

            if log_unicode_string != None:
                log_text = unicodedata.normalize('NFKD', log_unicode_string).encode('ascii', 'ignore')
            if log_text is None or log_text == "":
                self.last_updated = 0
                continue
            try:
                self.magic_json = json.loads(log_text)
            except:
                print log_text
                print "Check above log to debug"
                continue

            last_updated_json = self.magic_json["updateOn"]
            if last_updated_json <= self.last_updated:
                continue
            else:
                log_shown = True
                break
        if not log_shown:
            self.log("Fail", "Magic logs not updated after " +str(wait)+" seconds wait")
            return self.current_screen, False

        # updates button names from code file


        self.current_screen = self.magic_json["screen"]




        self.last_updated = self.magic_json["updateOn"]
        self.game_obj = self.magic_json["gameObj"]

        self.user_obj = self.magic_json["userObj"]

        self.magic_json["runtimeConfig"] = "" #empty runtimeconfig for now
        self.runtime_config = self.magic_json["runtimeConfig"]
        self.experiments = self.magic_json["experiments"]
        self.qa_logs = copy.deepcopy(self.magic_json["qaLogs"])
        self.puzzle_completed = self.game_obj["puzCompleted"]
        self.qa_logs_zindex_filter()

        self.qa_logs_grouped = self.group_qa_logs()

        if self.current_screen == "puzzle":
            if self.is_string_shown("DAILY"):
                self.current_screen = "daily_puzzle"
            elif self.is_string_contains("Bonus Words"):
                self.current_screen = "bonus_words"
        return self.current_screen, True


    def get_magic_logs(self, wait=30, launch_target_app=False):
        #logs

        """
        Read updated magic logs from native view on app

        Performs click on the magic button to get updated logs populated to native view's description value.
        :param wait: Time required to get the updated magic logs after tapping on magic button
                launch_target_app : if true launch the app and get the logs and everything and then perform the required actions!
        :return: Current screen name string and bool for result
        """
        # self.util.logger("debug","fun")
        log_text = None
        target_app_state = self.is_target_app_open()
        if (not target_app_state):
            # self.util.logger('debug',"first if condition to check if the target is open")
            if launch_target_app:
                #print launch_target_app, target_app_state
                if self.driver.current_package != self.driver.desired_capabilities["appPackage"]:
                    self.log("info", "Target App is not open")
                    self.log("info", "Appium launching app : " + self.driver.desired_capabilities["appPackage"])
                    self.driver.activate_app(self.driver.desired_capabilities["appPackage"])
                    time.sleep(10)
            return self.current_screen, False

        wait_time = time.time() + wait
        log_shown = False
        while time.time() <= wait_time:

            """new try"""
            try:
                print("The current screen is " + self.current_screen)
            except:
                print("The current screen is none")
            try:
                self.util.logger("debug","try block in while loop")
                sever_connection = self.ws.ws.connected
            except:

                self.util.logger("debug","except block in while loop")
                self.ws = ws_conn.ws(const.WS_URL, 3)
                time.sleep(1)
                continue

            if not sever_connection:
                self.util.logger("debug","If not server_connection")
                self.ws = ws_conn.ws(const.WS_URL, 3)
            #self.tap(self.width / 2, 2, False)
            #self.tap(self.width / 2, 2, False)
            #self.tap(self.width / 2, 2, False)
            #unicodedata.normalize('NFKD', title).encode('ascii','ignore')
            try:
                self.util.logger("debug","2 try block")
                log_unicode_string = self.ws.send({"command": "magicLogs"})
                # print(log_unicode_string)
                #log_unicode_string = self.driver.find_element_by_id("android:id/content").get_attribute("content-desc")
            except:
                self.util.logger(("2 nd except block"))
                print "unknown screen"
                self.current_screen = "unknown"
                return self.current_screen, False
            '''
            if log_unicode_string != None:
                log_text = unicodedata.normalize('NFKD', log_unicode_string).encode('ascii', 'ignore')
            '''
            log_text = log_unicode_string
            if log_text is None or log_text == "":
                self.util.logger("debug","if log_text is None or log_text == ")
                self.last_updated = 0
                continue
            try:
                self.util.logger("debug", "3rd try block")
                self.magic_json = json.loads(log_text)
            except:
                self.util.logger("debug","3 rd except block")
                print log_text
                print "Check above log to debug"
                continue

            last_updated_json = self.magic_json["updateOn"]
            print(last_updated_json)
            print(self.last_updated);
            if last_updated_json <= self.last_updated:
                self.util.logger("debug","last_updated_json <= self.last_updated")
                print("******* last updated json")
                print(last_updated_json)
                print("\n******** self.last_updated")
                print(self.last_updated);
                continue
            else:
                log_shown = True
                break
        if not log_shown:
            self.log("Fail", "Magic logs not updated after " + str(wait)+" seconds wait")
            return self.current_screen, False

        # updates button names from code file
        #self.update_button_names()

        self.current_screen = self.magic_json["screen"]



        print("The last self.last_updated = "+str(self.last_updated));
        self.last_updated = self.magic_json["updateOn"]
        print("The new self.last_updated  = "+str(self.last_updated));
        self.game_obj = self.magic_json["gameObj"]
        self.user_obj = self.magic_json["userObj"]
        self.runtime_config = self.magic_json["runtimeConfig"]
        self.experiments = self.magic_json["experiments"]
        self.qa_logs = copy.deepcopy(self.magic_json["qaLogs"])

        self.puzzle_completed = self.game_obj["puzCompleted"]
        #self.qa_logs_zindex_filter()

        self.qa_logs_grouped = self.group_qa_logs()

        if self.current_screen == "puzzle":
            if self.is_string_shown("DAILY"):
                self.current_screen = "daily_puzzle"
            elif self.is_string_contains("Bonus Words"):
                self.current_screen = "bonus_words"

        return self.current_screen, True


    def update_experiment(self, exp, var):
        """
        Use to change the exp and var of the game
        param : exp = experiment no and
                var = Variant number.

        """
        self.ws.send({"command": "assignVariantForExperiment", "params": {"experimentName": exp, "variantName": int(var)}})

    def is_string_shown(self, search_string):
        """
        to check if the given string is shown on the screen or not
        parm : search_string = the required string to be searched!
        """
        #To check the string in the present screen
        for qlg in self.qa_logs:
            try:
                if qlg["name"] == search_string:
                    return True
            except:
                continue
        return False

    """
    new function to return the xPos and yPos if is_string_contains() return true
    """
    def string_button_pos(self,search_string):
        """
        Check if the search string is present and it is present on the button element type or not on the screen
        :parm : The string to be searched
        :return : the x and y pos of the string
        """
        xx = []
        for qlg in self.qa_logs:
            try:
                if search_string in qlg["name"]:
                    xx=qlg["end_point"]
                    if 'Button' in qlg["elementType"]:
                        xx = qlg["end_point"]
                    return xx
            except:
                continue
        return xx



    def is_string_contains(self, search_string):
        """
        To check if the substring is available on the current screen

        parm : search_string = for which the action to be performed!
        """
        for qlg in self.qa_logs:
            try:
                if search_string in qlg["name"]:
                    return True
            except:
                continue
        return False


    def get_fullscreen_element(self):
        """
            Get fullscreen elements
        """
        if self.current_screen != "puzzle":
            return 0
        for i in self.qa_logs:
            #TODO: get 1920 value or device height from appium function
            if i["boundbox"]["height"] >= 1920:
                return i
        return 0

    def qa_logs_zindex_filter(self):
        """
        Zindex filter
        """
        zindex = 0
        full_screen_element = self.get_fullscreen_element()
        if full_screen_element != 0:
            zindex = full_screen_element["zindex"]
        self.to_remove = []
        for ql in self.qa_logs:
            if ql["zindex"] < zindex:
                self.to_remove.append(ql)
        for t in self.to_remove:
            self.qa_logs.remove(t)





    def update_button_names(self):
        """
        No use
        """
        root = "/Users/fazilmajeeth/gitlab/word_jam/word_treat/frameworks/runtime-src/proj.android-studio/app/"
        for m in self.magic_json["qaLogs"]:
            if m["elementType"] == "Button":# and "@" in m["name"]:
                file = root + m["name"].split("@")[0]
                line_number = int(m["name"].split("@")[1])
                with open(file, 'r') as fp:
                    content = fp.read()
                content = content.split("\n")
                button_line = content[line_number-1]
                button_name_split = button_line.split("=")
                if len(button_name_split) > 1:
                    button_name = button_name_split[0].strip()
                    button_name = button_name.split(" ")
                    for b in button_name:
                        if b == "var":
                            button_name.remove(b)
                        if b == "":
                            button_name.remove(b)
                    button_name = button_name[0]
                    #m["name"] = button_name + "_" + str(m["xPos"]) + "_" + str(m["yPos"])
                    m["name"] = button_name


    def get_sprites(self, reload=False):
        """
        NO use
        """
        if reload:
            self.get_magic_logs()
        elif self.qa_logs is None:
            self.get_magic_logs()

        sprites = []
        for ql in self.qa_logs:
            try:
                print(ql.keys())
                print(ql["name"])
                if "spriteName" in ql.keys():
                    sprites.append(ql)
            except:
                pass
        return sprites

    def get_strings(self, reload=False):
        """
        No use
        """
        if reload:
            self.get_magic_logs()
        elif self.qa_logs is None:
            self.get_magic_logs()

        strings = []
        for ql in self.qa_logs:
            print(ql.keys())
            try:
                #og
                #if "strings" in ql.keys():
                if "string" in ql.keys():
                    strings.append(ql)
            except:
                pass
        return strings

    def click_sprite(self, sprite_name, reload=False, index=0):
        """
        No use
        """
        if reload:
            self.get_magic_logs()
        elif self.qa_logs is None:
            self.get_magic_logs()

        sprites = []
        for s in self.get_sprites():
            print(s["spriteName"])
            if s["spriteName"] == sprite_name:

                sprites.append(s)
        self.tap(sprites[index]["xPos"], sprites[index]["yPos"])

    def get_sprites_with_visibility(self, reload=False, visible_value=[True, None, False]):
        """
        No use
        """
        if reload:
            self.get_magic_logs()
        elif self.qa_logs is None:
            self.get_magic_logs()
        sprites = []
        for s in self.get_sprites():
            if s["visible"] in visible_value:
                sprites.append(s)
        return sprites


    def click_string(self, string_name, reload=False, index=0):
        """
        No use
        """
        if reload:
            self.get_magic_logs()
        elif self.qa_logs is None:
            self.get_magic_logs()

        strings = []

        for s in self.get_strings():
            #og
            #if s["strings"] == string_name:
            if s['string'] == "u\'"+string_name:
                strings.append(s)

        print(strings)
        self.tap(strings[index]["xPos"], strings[index]["yPos"])

    def get_core_element_type(self, element_index):
        """
        Use for BOT
        """
        if self.core[element_index]["Type"] in self.sprite_elements:
            return "spriteName"
        if self.core[element_index]["Type"] in self.string_elements:
            return "string"
        return self.core[element_index]["Type"]

    def is_core_element_visible(self, element_index):
        """
        use for BOT
        """
        element_type = self.get_core_element_type(element_index)
        elements_list = None
        if element_type == "string":
            return self.string_match(element_index, element_type)

        elif element_type == "spriteName":
            return self.sprite_match(element_index, element_type)

        elif element_type == "action":
            return [], True

        self.log("fail", "Element not shown")
        return [], False

    def get_bounding_box_for_el(self, element_name):
        """
        No use
        """
        print self.core_element_map
        el_index = self.core_element_map[element_name]
        el_details = self.core[el_index]
        qa_sprites_list = self.get_sprites()





    def string_match(self, element_index, element_type):
        """
        No use
        """
        elements_list = self.get_strings()

        for ql in elements_list:
            if "%#" == self.core[element_index][element_type]:
                #value_type_match = str(ql[element_type]).isdigit() and ql["fontName"] == self.core[element_index]["fontName"]
                if self.core[element_index]["action_details"] != "":
                    action_json = json.loads(self.core[element_index]["action_details"])
                    if str(self.run_action(action_json)) == str(ql[element_type]):
                        value_match = True
                    else:
                        continue
                    print "String match:", self.run_action(action_json), ql[element_type]
            else:
                value_match = str(ql[element_type]).encode('ascii') == self.core[element_index][element_type]
            if value_match and ql["fontName"] == self.core[element_index]["fontName"]:
                return ql, True
        return [], False


    def get_string_in_sprite(self, spritename, bounding=(10, 10), index=0):
        """
        NO use
        """

        self.get_magic_logs()
        screen_name = self.current_screen
        screen_id = self.screen_id(screen_name)
        magic_data = self.qa_logs
        sprite_list = self.get_sprites()

        sprite_item = self.get_magic_data_loaded_v2("spriteName", spritename, magic_data)
        if sprite_item:
            sprite_x_pos, sprite_y_pos = sprite_item[index]["xPos"],  sprite_item[index]["yPos"]
        else:
            print "Sprite " + spritename + " is not shown"
            return False
        string_item = self.get_magic_data_loaded_v2("string", None, magic_data)
        for st in string_item:
            start_point = (sprite_x_pos - bounding[0], sprite_y_pos - bounding[1])
            end_point = (sprite_x_pos + bounding[0], sprite_y_pos + bounding[1])
            if (st["xPos"] >= start_point[0] and st["yPos"] >= start_point[1]) and (st["xPos"] <= end_point[0] and st["yPos"] <= end_point[1]) and st["screen"] == screen_id:
                print "String in sprite" , st["string"]
                print st

    def sprite_match(self, element_index, element_type):
        """
        NO use
        """
        elements_list = self.get_sprites()
        for ql in elements_list:
            if str(ql[element_type]).encode('ascii').lower() == self.core[element_index][element_type].lower():
                return ql, True
        return [], False

    def update_core(self):
        """
        NO USE
        """
        self.get_magic_logs()
        cs = self.current_screen
        csvrow = self.csvrow
        grouped_logs = self.group_qa_logs()

        for c, cval in core.items():
            visible_condition = json.loads(cval["Visible_Condition"])
            if cval["Current_Screen"] == cs and self.check_condition_match(visible_condition):
                core_element_details_in_screen  = self.is_core_element_visible(c)
                cval["status"] = core_element_details_in_screen[1]
                cval["qlog"] = core_element_details_in_screen[0]
                print cval["Elements"], " = ", core_element_details_in_screen[1]
            else:
                cval["status"] = 0

    def check_condition_match(self, visible_condition):
        """
        NO USE
        """
        if self.current_screen == "fblogin":
            return True
        game_obj = self.magic_json["gameObj"]
        result = []
        for v in range(0, len(visible_condition)):
            op_func = util.ops[visible_condition[v]["condition"]]
            if visible_condition[v]["name"] == "visibility":
                result.append(visible_condition[v]["value"])
            else:
                result.append(op_func(game_obj[visible_condition[v]["name"]], visible_condition[v]["value"]))
        if False in result:
            return False
        return True
    '''
    def get_actions(self):
        csvdata = self.csvrow
        actions = []
        for c, cval in csvdata.items():
            click_condition = json.loads(cval["Clickable_Condition"])
            if cval["status"] and self.check_condition_click(click_condition):
                actions.append(c)
        return actions

    def next_step(self):
        actions = self.get_actions()
        for a in actions:
            element_type = self.get_core_element_type(a)
            if self.core[a]["click_count"] == 0:
                if element_type in ["string", "spriteName"]:
                    self.log("info", "Click " + self.core[a]["Elements"])
                    self.core[a]["click_count"] += 1
                    return self.tap(self.core[a]["qlog"]["xPos"], self.core[a]["qlog"]["yPos"])
                elif self.get_core_element_type(a) == "action":
                    action_details = json.loads(self.core[a]["action_details"])
                    self.core[a]["click_count"] += 1
                    self.run_action(action_details)
    '''
    def next_step(self):
        """
        No use
        """
        csvrow = self.csvrow

    def reset_scroll_view_to_top(self):
        """
        No Use
        """
        #og
        #self.driver.swipe(560, 1200, 560, 1600, 300)
        self.driver.swipe(560, 900, 560, 1350, 300)
        time.sleep(2)
        #og
        #self.driver.swipe(560, 1200, 560, 1600, 300)
        self.driver.swipe(560, 900, 560, 1350, 300)

        time.sleep(3)


    def get_ele_info(self, ele):
        """
        No use
        """
        grouped_log = self.qa_logs_grouped
        element_type = ele["type"]
        if element_type in self.type_button:
            images = [i for i in ele["images"].split(self.separator) if i]
            labels = [i for i in ele["labels"].split(self.separator) if i]
            element_type = "BUTTONS"
        elif element_type in self.type_image:
            labels = [i for i in ele["labels"].split(self.separator) if i]
            element_type = "IMAGES"
        elif element_type in self.type_text:
            element_type = "LABELS"

        for gl in grouped_log[element_type]:
            if ele["element"] == gl["name"]:
                return gl

    def check_click_count_condition(self,screen, click_count):

        """
        For BOT
        Parm : Current screen as Input and check if the prticular element is clickable or not
        """
        qa_logs_grouped = self.qa_logs
        buttons_count = len(self.qa_logs_grouped["BUTTONS"])
        element_type_for_action = ["Button"]
        if buttons_count == 0:
            element_type_for_action = ["Sprite", "Scale9Sprite"]

        for qlg in qa_logs_grouped:
            elementType = qlg["elementType"]
            if elementType in element_type_for_action:
                if qlg["name"] == self.const.MAGIC_BUTTON_NAME:
                    continue
                try:
                    if qlg["screen"] == screen and self.clicked_elements[qlg["name"]] < click_count:
                        return False
                except:
                    return False
        return True

    def record_click(self, element, screen):
        """
        Not use upto now
        To play the recorded logs
        """
        print "RECORD: ", element
        self.get_magic_logs()
        self.step += 1
        timestamp = time.time()
        if len(self.record_batch) <= 0:
            self.record_batch.append((self.step, element, "click", screen, str(self.game_obj), timestamp))
            self.update_batch()


    def launch_game(self):
        """
        Use to launch the game
        """
        p1 = Thread(target=self.ss.save)
        p2 = Thread(target=self.driver.launch_app)
        p1.start() # launch app
        p2.start() # launch app
        max_attempt = 6
        attempt = 0
        p1.join()
        while attempt<=max_attempt:
            err_index, image2 = self.ss.compare_previous_screenshot()
            if err_index > 10:
                print "err index more than 10 - " +  str(err_index)
                save_image2 = screenshot.AsyncWrite(image2, self.screenshots_path+"splash.png")
                _, logs = self.get_magic_logs(1)
                if logs:
                    break
                else:
                    save_image2.start()
                break
            attempt += 1

    def record_action(self, action_function, screen):
        """
        Record all the actions
        """
        print "RECORD: ", action_function
        self.get_magic_logs()
        self.step += 1
        timestamp = time.time()
        if len(self.record_batch) <= 0:
            self.record_batch.append((self.step, action_function, "action", screen, str(self.game_obj), timestamp))
            self.update_batch()


    def update_batch(self):
        if self.update_log_location == "googlesheets":
            for i in self.record_batch:
                self.googlesheets.append(i)
            self.record_batch_back1 = copy.deepcopy(self.record_batch)
            self.record_batch = []
        elif self.update_log_location == "local":

            writer = csv.writer(open(self.bot_log, 'a'))
            for i in range(0, len(self.record_batch)):
                writer.writerow(self.record_batch[i])
            self.record_batch_back1 = copy.deepcopy(self.record_batch)
            self.record_batch = []

    def tap_game_back_button(self):
        """
        Use to tap the back button
        """
        return self.tap_sprite("#back_new.png")

    def tap_sprite(self, sprite_name, index=0):
        """
        Use to tap the specific sprite
        parm : sprite_name = name of the sprite to tap on 
                index = if more than one sprite with same name are present on the screen the index will help to reach to specific sprite

        """
        index_count = 0
        self.get_magic_logs()
        qa_logs = self.qa_logs

        for qlg in qa_logs:
            try:
                name = qlg["name"]
                print(name)
            except:
                name = ""
            if name == sprite_name:
                print("Yes")
                if index_count == index:
                    print("YEEEEE")
                    self.record_action("self.tap_sprite('" + sprite_name + "')", self.current_screen)
                    return self.tap_element(qlg)
                else:
                    index_count += 1
                    continue
        return False

    def tap_hints_button(self):
        """
        Click on the hints icon
        """
        return self.tap_sprite("#hint_new.png")

    def choose_next_click(self, qa_logs_grouped):
        """
        click on the next clickable icon and increment the click counter
        """
        #s1 = input("Going in to load_magic_logs_if_empty")
        self.load_magic_logs_if_empty()
        buttons_count = len(self.qa_logs_grouped["BUTTONS"])
        #s1 = input("Printing the buttons details")
        #print(buttons_count)
        element_type_for_action = ["Button"]
        if buttons_count == 0:
            element_type_for_action = ["Sprite", "Scale9Sprite"]
        #print(element_type_for_action)
        for qlg in qa_logs_grouped:

            xPos = qlg["xPos"]
            yPos = qlg["yPos"]
            screen = qlg["screen"]
            #name = qlg["name"]
            #print(xPos)
            #print(yPos)
            #print(screen)

            elementType = qlg["elementType"]
            #print(elementType)
            layerType = qlg["layerType"]
            '''
            try:
                print("the name is"+str(qlg["name"]))
            except:
                print ("No name")
            print(layerType)'''
            if elementType in element_type_for_action:# or elementType == "Sprite" or elementType == "Scale9Sprite":
                if qlg["name"] == self.const.MAGIC_BUTTON_NAME:
                    continue
                try:
                    #print("i am in try ")
                    item_name = const.SCREEN_NAMES[screen] + "_" + qlg["name"] + "_" + str(int(xPos)) + "_" + str(int(yPos))
                except:
                    print "ERROR" , qlg

                    continue
                if (xPos < 0) or (yPos < 0):
                    continue
                '''
                if (yPos < 3000):
                    continue
                '''
                try:
                    #print("i am in clicked "+ self.clicked_elements[qlg["name"]])
                    click_count = self.clicked_elements[qlg["name"]]
                except:
                    click_count = self.clicked_elements[qlg["name"]] = 1
                    #print("except "+ str(click_count))
                    #print("layer type "+str(layerType))
                    if layerType == "scroll":
                        self.action.reset_scroll_view_to_top()

                    self.action.tap_element(qlg)
                    #print("printing true")
                    #self.action.tap_element(qlg)
                    #time.sleep(2)
                    #self.record_click(qlg["name"], self.current_screen)
                    return
                if self.check_click_count_condition(screen, self.clicked_elements[qlg["name"]]):

                    self.clicked_elements[qlg["name"]] += 1
                    if layerType == "scroll":
                        self.action.reset_scroll_view_to_top()
                    if qlg["name"] == self.const.MAGIC_BUTTON_NAME:
                        continue
                    self.action.tap_element(qlg)
                    #self.action.tap_element(qlg)
                    #time.sleep(2)
                    #self.record_click(qlg["name"], self.current_screen)
                    return
                else:
                    # self.record_click(qlg["name"])

                    continue




    def x_controlled_swipe_v(self, start, end):

        """
        x swipe
        """
        swipe_height = int(end[1])
        device_height = self.height
        full_swipe_height = device_height - 500
        print "full_swipe_height", full_swipe_height
        last_swipe = swipe_height % full_swipe_height
        print last_swipe
        swipe_count = int(swipe_height / full_swipe_height)
        print swipe_count
        for sc in range(0 ,swipe_count):
            print "Attempt", sc
            play = TouchAction(self.driver)
            play.press(x=start[0], y=start[1]).wait(1000)
            play.move_to(x=end[0], y=start[1] + full_swipe_height).wait(1000)
            play.release().perform()
            time.sleep(1)
        if last_swipe > 0:
            play = TouchAction(self.driver)
            play.press(x=start[0], y=start[1]).wait(1000)
            play.move_to(x=end[0], y=start[1] + last_swipe).wait(1000)
            play.release().perform()
            time.sleep(1)

    def controlled_swipe_v(self, start_y, end_y):
        """
        vertical swipe
        """
        play = TouchAction(self.driver)
        x = self.width / 2
        '''
        new +200
        '''
        play.press(x=x, y=start_y+200).wait(1000)
        play.move_to(x=x, y=end_y).wait(1000)
        play.release().perform()
        time.sleep(1)


    def tap_element(self, qlg):
        """
        DOUBT
        """
        xPos = qlg["xPos"]
        yPos = qlg["yPos"]
        element_name = str(qlg["name"])
        element_type = str(qlg["elementType"])
        take_snap = True

        centerX = self.width / 2
        max_swipe_height = 800
        height_segment = self.height / 10
        height_2_8 = (height_segment * 2, height_segment* 8)
        if qlg["layerType"] == "normal":
            self.action.tap(xPos, yPos, take_snap, element_name, element_type)
            #print qlg["name"]
            return True
        visibleContainerHeight = qlg["visibleContainerHeight"]
        if yPos <= visibleContainerHeight:
            self.action.tap(xPos, yPos, take_snap, element_name, element_type)
            #print qlg["name"]
            return True
        totalContainerheight = qlg["totalContainerheight"]
        extra_height = yPos - (self.height - 1)
        print "Extra height : ", extra_height
        swiped_height = 0
        bottom_segment = 200
        while extra_height > (self.height - 1):
            extra_height = yPos - (self.height - 1)
            self.action.controlled_swipe_v(self.height - bottom_segment, self.height - bottom_segment - max_swipe_height)
            yPos -= max_swipe_height

        while yPos > (self.height - 1):
            extra_height = yPos - (self.height - 1)
            if extra_height < max_swipe_height:
                self.action.controlled_swipe_v(self.height - bottom_segment, self.height - bottom_segment - extra_height)
                yPos -= extra_height
                print yPos, extra_height
            else:
                self.action.controlled_swipe_v(self.height - bottom_segment, self.height - bottom_segment - max_swipe_height)
                yPos -= max_swipe_height
                print yPos, max_swipe_height
        #print xPos, yPos - bottom_segment
        self.action.tap(xPos, yPos - bottom_segment, take_snap, element_name, element_type)
        #print qlg["name"]
        '''
        swipe_count = int(yPos/visibleContainerHeight)
        while (swipe_count > 1):
            total_swipe_height = visibleContainerHeight
            swiped_height = 0
            while swiped_height < total_swipe_height:
                self.controlled_swipe_v((centerX, height_2_8[1]), (centerX, height_2_8[0]))
                swiped_height += height_2_8[1] - height_2_8[0]
                yPos -= swiped_height
            swipe_count -= 1
        total_swipe_height = yPos - visibleContainerHeight
        swiped_height = 0
        while swiped_height < total_swipe_height:
            self.controlled_swipe_v((centerX, height_2_8[1]), (centerX, height_2_8[1] - total_swipe_height))
            swiped_height += height_2_8[1] - height_2_8[0]
            yPos -= swiped_height
        self.tap(xPos, visibleContainerHeight)
        '''
        """new"""
        self.action.get_magic_logs()
    def get_element_position(self, qlg):

        """
        to get the position of the element
        """
        xPos = qlg["xPos"]
        yPos = qlg["yPos"]
        element_name = str(qlg["name"])
        element_type = str(qlg["elementType"])
        take_snap = True

        centerX = self.width / 2
        max_swipe_height = 700
        height_segment = self.height / 10
        height_2_8 = (height_segment * 2, height_segment* 8)
        if qlg["layerType"] == "normal":
            self.action.tap(xPos, yPos, take_snap, element_name, element_type)
            #print qlg["name"]
            return True
        visibleContainerHeight = qlg["visibleContainerHeight"]
        if yPos <= visibleContainerHeight:
            self.action.tap(xPos, yPos, take_snap, element_name, element_type)
            #print qlg["name"]
            return True
        totalContainerheight = qlg["totalContainerheight"]
        extra_height = yPos - (self.height - 1)
        swiped_height = 0
        bottom_segment = 300
        while extra_height > (self.height - 1):
            extra_height = yPos - (self.height - 1)
            self.action.controlled_swipe_v(self.height - bottom_segment, self.height - bottom_segment - max_swipe_height)
            yPos -= max_swipe_height

        while yPos > (self.height - 1):
            extra_height = yPos - (self.height - 1)
            if extra_height < max_swipe_height:
                self.action.controlled_swipe_v(self.height - bottom_segment, self.height - bottom_segment - extra_height)
                yPos -= extra_height
                print yPos, extra_height
            else:
                self.action.controlled_swipe_v(self.height - bottom_segment, self.height - bottom_segment - max_swipe_height)
                yPos -= max_swipe_height
                print yPos, max_swipe_height
        #print xPos, yPos - bottom_segment
        return xPos, yPos - bottom_segment, qlg["name"], qlg["elementType"]
        #print qlg["name"]


    def next_click(self, count):
        """
        it acts like selection panel
        eg it will open the first screen oin the game and try to click each button available on the screen and increase it counter by 1
        """
        '''while self.run_name is None:
            self.record_run()'''

        i = 0

        if self.action.step == -1:
            self.action.get_pre_conditions()
        while (i < count):
            i += 1
            print "click count ", i
            screen, result = self.get_magic_logs()
            print(screen)
            if screen == "fblogin":
                self.action.fb_login_webview()

            if screen == "device_home":
                self.action.activate_app()
                screen, result = self.get_magic_logs()

            if screen == "dailyCalendar" or screen == "store" or screen == "spinner" or screen == "unknown" or screen == "device_home" or screen == "android_native_share" or screen == "purchase_confirmation_screen" or screen == "free_coins":

                self.action.back()
                screen, result = self.get_magic_logs()
                print "Skipped screen"
                continue
            if screen == "support" or screen == "quest_center":
                self.action.game_back()
                screen, result = self.get_magic_logs()
                print "Skipped screen"
                continue


            self.choose_next_click(self.qa_logs)
            try:
                actions = const.ACTIONS_IN_SCREEN[self.current_screen]
            except:
                actions = False

            if i % 5 == 0:
                if actions:
                    action_name = "self.action." + actions[0] + "()"
                    eval(action_name)

            if i % 7 == 0:
                if actions:
                    action_name = "self.action." + actions[1] + "()"
                    eval(action_name)

            '''if i % 10 == 0:
                if actions:
                    action_name = "self.action." + "kill_app()"
                    self.add_hours(7)
                    eval(action_name)'''


    def run_action(self, action_details):
        """
        use for BOT
        """

        action_name = action_details["name"]
        return eval("self."+action_name+"(" + json.dumps(action_details) + ")")

    def wait_for_element_by_class_name(self, classname, timeout_seconds=None):
        """
        Try to find the value by class
        parm : classname = name of the class to be searched on the native view
               timeout_seconds = number of seconds to be halt before terminationg the search
        """

        now = time.time()
        if timeout_seconds is None:
            timeout = now + 10
        else:
            timeout = now + timeout_seconds
        while True:
            print(classname)
            try:
                elem = self.driver.find_element_by_class_name(classname)
                if elem.is_displayed():
                    print("info", "Element is shown")
                    return True
                    break
                else:
                    print("info", "Element is not shown")
            except:
                if (time.time() >= timeout):
                    print("info", "Element is not shown")
                    return False
                else:
                    #print("info", "Waiting for element")
                    time.sleep(1)

    def fb_login_webview(self, action_details=None):
        """
        To check  if the fb page is active or not
        if yes  then perform the login

        """

        if action_details is None:
            action_details = self.util.new_fb_test_user()
        username = action_details["email"]
        password = action_details["password"]

        #if self.wait_for_element_by_class_name('android.widget.Image', 20):
        #if self.wait_for_element_by_class_name("android.view.View", 20):
        if self.is_fb_login_shown(5):
            email_field = self.driver.find_elements_by_class_name('android.widget.EditText')[0]
            password_field = self.driver.find_elements_by_class_name('android.widget.EditText')[1]
            email_field.send_keys(username)
            password_field.send_keys(password)
            login_button = self.driver.find_element_by_class_name('android.widget.Button')
            login_button.click()
            time.sleep(2)
        else:
            print("fail", "Unknown error, unable to complete login")
        self.confirm_login_fb()

    def confirm_login_fb(self):
        """
        Confirm if the login is valid
        """

        self.wait_for_fb_login_webview('android.widget.Button')
        login_button = self.driver.find_elements_by_class_name('android.widget.Button')[1]
        time.sleep(5)
        login_button.click()
        time.sleep(5)

    def assert_current_screen(self, screen_name):
        """
        Asserts if current screen show is expected screen
        :param screen_name: expeected screen name
        :return: bool
        """

        current_screen = self.current_screen
        if screen_name == current_screen:
            print "PASS: Current screen name : " + current_screen
            return True
        else:
            print "FAIL: Current screen name is : "+ current_screen + " and NOT : " + screen_name
            return False

    def assert_text_equals(self, actual, expected):
        """
        :param actual: text
        :param expected: text
        :return: bool
        """

        if expected == actual:
            print("pass", "Expected text " + actual + " is shown")
        else:
            print("fail", actual + " is shown instead of " + expected)

    def wait_for_element_by_id(self, id, timeout=None):
        """
        wait for element by id
        :param id:
        :param timeout:
        :return: bool
        """

        now = time.time()
        if timeout is None:
            timeout = now + 10
        else:
            timeout = now + timeout
        while True:
            try:
                elem = self.driver.find_element_by_id(id)
                if elem.is_displayed():
                    self.log("info", "Element is shown")
                    return True
                    break
                else:
                    log("info", "Element is not shown")
            except:
                if time.time() >= timeout:
                    self.log("info", "Element is not shown")
                    return False
                else:
                    self.log("info", "Waiting for element")
                    time.sleep(1)

    def wait_for_element_by_class(self, id, timeout=None):

        now = time.time()
        if timeout is None:
            timeout = now + 10
        else:
            timeout = now + timeout
        while True:
            try:
                elem = self.driver.find_element_by_class_name(id)
                if elem.is_displayed():
                    self.log("info", "Element is shown")
                    return True
                    break
                else:
                    log("info", "Element is not shown")
            except:
                if time.time() >= timeout:
                    self.log("info", "Element is not shown")
                    return False
                else:
                    self.log("info", "Waiting for element")
                    time.sleep(1)

    def wait_for_fb_login_webview(self, id, timeout=None):

        now = time.time()
        if timeout == None:
            timeout = now + 10
        else:
            timeout = now + timeout
        while True:
            try:
                elem = self.driver.find_elements_by_class_name(id)
                if len(elem) == 2:
                    self.log("info", "Element is shown")
                    return True
                    break
                else:
                    log("info", "Element is not shown")
            except:
                if time.time() >= timeout:
                    self.log("info", "Element is not shown")
                    return False
                else:
                    self.log("info", "Waiting for element")
                    time.sleep(1)

    def check_condition_click(self, click_condition):

        if self.current_screen == "fblogin":
            return True
        game_obj = self.magic_json["gameObj"]
        result = []
        for v in range(0, len(click_condition)):
            op_func = util.ops[click_condition[v]["condition"]]
            if click_condition[v]["name"] == "click":
                result.append(click_condition[v]["value"])
            else:
                result.append(op_func(game_obj[click_condition[v]["name"]], click_condition[v]["value"]))
        if False in result:
            return False
        return True

    def get_device_clock_string(self):
        """
        get_the device time in string format
        """
        return self.driver.device_time

    def is_jam_notif_shown(self):
        """
        Check if any notification related to the game is active in notification bar or not
        """
        try:
            notif = self.driver.find_element_by_xpath("//*[@package='in.playsimple.tripcross']")
            return True
        except:
            return False

    def is_notification_panel_shown(self):
        """
        Check if the notification is active or not
        return true: if shown
        return fasle: if not shown
        """

        notification_header = self.driver.find_elements_by_id("android:id/notification_header")
        if len(notification_header):
            return True
        else:
            return False

    def open_notification_panel(self):
        """
        drag the notification bar if not active  else do nothing
        """

        if self.is_notification_panel_shown():
            return False
            #print("info", "notification panel is shown")
        else:
            return self.driver.open_notifications()

    def add_days(self, count):
        """
        Add days to the current date of the device
        parm: count = number of days to be added
        """

        end_datetime = parser.parse(self.get_device_clock_string()) + timedelta(days=count)
        command = end_datetime.strftime("%m%d%H%M%Y.%S")
        subprocess.check_output(['adb', '-s', self.driver.desired_capabilities['deviceName'], 'shell', 'su', '-c', 'date ' + command])

    def add_hours(self, count):
        """
        Add hours to the current time of the devices
        parm : count = number of hours to be added
        """

        end_datetime = parser.parse(self.get_device_clock_string()) + timedelta(hours=count)
        command = end_datetime.strftime("%m%d%H%M%Y.%S")
        subprocess.check_output(['adb', '-s', self.driver.desired_capabilities['deviceName'], 'shell', 'su', '-c', 'date ' + command])

    def add_minutes(self, count):
        """
        Add minutes to the current time of the devices
        parm : count = number of minutes to be added
        """

        end_datetime = parser.parse(self.get_device_clock_string()) + timedelta(minutes=count)
        command = end_datetime.strftime("%m%d%H%M%Y.%S")
        subprocess.check_output(['adb', '-s', self.driver.desired_capabilities['deviceName'], 'shell', 'su', '-c', 'date ' + command])

    def get_notifications_shown(self):

        """
        Drag the notification bar if not active and read all the notification which are currently present on the notification bar
        """

        self.open_notification_panel()
        notif_list = self.driver.find_elements_by_id("android:id/status_bar_latest_event_content")
        notifs = {}
        item = 0
        for n in notif_list:
            app_name = self.get_notif_details(n, "android:id/app_name_text")

            notif_title = self.get_notif_details(n, "android:id/title")

            notif_desc = self.get_notif_details(n, "android:id/text")
            #notif_mini_icon =self.get_notif_details((" android:id/icon")
            notifs[item] = [app_name, notif_title, notif_desc]
            item = item + 1

        #self.driver.back()

        return notifs

    def click_on_jam_notif(self):
        """
        Darg the notification bar if not active and
        click on the wordjam related notification
        """

        self.open_notification_panel()
        notif_list = self.driver.find_elements_by_id("android:id/status_bar_latest_event_content")
        notifs = {}
        item = 0
        for n in notif_list:
            app_name = self.get_notif_details(n, "android:id/app_name_text")

            notif_title = self.get_notif_details(n, "android:id/title")

            notif_desc = self.get_notif_details(n, "android:id/text")
            # notif_mini_icon =self.get_notif_details((" android:id/icon")
            if app_name[0] == "CrossWord Jam":
                notif_desc[1].click()
                return [app_name[0], notif_title[0], notif_desc[0]]

            notifs[item] = [app_name[0], notif_title[0], notif_desc[0]]
            item = item + 1

        # self.driver.back()

        return notifs

    def get_notif_details(self,n, id):
        """
        Get the details of the current notifications
        """

        try:
            return n.find_element_by_id(id).text,  n.find_element_by_id(id)
        except:
            return "", ""

    def play_recorded_steps(self):
        """
        Not use currently
        """

        play_steps = self.googlesheets.read_data_for_range("record")
        print play_steps
        for p in range(0, len(play_steps)):
            screen, result = self.get_magic_logs()
            if not result:
                if screen == "device_home" or screen == "purchase_confirmation_screen" or screen == "fblogin":
                    self.self.go_back()
                    time.sleep(2)
                    screen, result = self.get_magic_logs()

            if play_steps[p]["screen"] == self.current_screen:
                if play_steps[p]["action"] == "click":
                    self.tap(play_steps[p]["x"], play_steps[p]["y"])
                elif play_steps[p]["action"] == "action":
                    eval("self." + play_steps[p]["element_type"])
                print p
                time.sleep(2)
            else:
                print "ERROR - Incorrect screen name", self.current_screen, "instead of ", play_steps[p]["screen"]

    def force_sync(self):
        """
        Syn if lost
        """

        try:
            sever_connection = self.ws.ws.connected
        except:
            self.get_magic_logs()
        self.ws.send({"command": "forceSync"})


    def go_back(self):
        """
        Go back from the current screen
        and store the record
        """

        self.get_magic_logs()
        self.driver.back()
        self.record_action("self.go_back()", self.current_screen)

    def assert_game_obj(self, keys):
        """
        For validating the result
        """

        for k in keys["keys"]:
            expected_value = self.game_obj[k]
            break
        return expected_value


    def get_experiment_name_and_variants(self):
        """
        Use to get the list of all the exoeriments and variants in JSON file
        :parm =NONE
        :return: return the Json of all the experiments and variants
        """
        y=self.ws.send({"command":"experiments"})
        #self.ws.send({"command": "setPuzCompleted", "params": {"val": value}})
        return y


    def get_letter_in_tiles(self):

        """
        Use for UserPickhint when a empty tiles need to be selected inorder to reveal the Alphabet
        :parms : NONE
        :return: return the list of all the vacant tiles which are currently available in the puzzle
        """
        self.get_magic_logs()
        qa_log = copy.deepcopy(self.magic_json["qaLogs"])
        letters_in_tiles_info = []
        letters_in_tiles = []
        letters =[]
        letters_order ={}
        order = 0

        for q in qa_log:
            if q["elementType"] in self.type_image:
                #font_changed = "res/fonts/ArialBold140.fnt"
                if q["name"] == '#bg_tile_white.png' or q["name"] == '#bg_tile_black.png':
                    letters.append((float(q["xPos"]),float(q["yPos"])))
                    order += 1
        return letters


    def get_letters_in_plate(self):

        """
        To identify the letter present on the plate
        """
        self.get_magic_logs()
        qa_log = copy.deepcopy(self.magic_json["qaLogs"])
        letters_in_plate_info = []
        letters_in_plate = []
        letters = {}
        letters_order = {}
        order = 0

        for q in qa_log:
            if q["elementType"] in self.type_text:
                font_changed = "res/fonts/Arial_250.fnt"        #font for the trip game
                font_before = "res/fonts/SFCompactDisplayMedium200.fnt"
                # font_changed = 'res/fonts/ArialBold140.fnt'        #font for wordjam
                # font_changed = "res/fonts/SFCompactDisplayMedium200.fnt"
                if q["font_name"] == font_changed and q["name"] != "" and q["yPos"] > self.height/2:
                    print "letters ", q
                    letters_in_plate_info.append(q)
                    letters_in_plate.append(q["name"])
                    letters_order[order] = q['name']
                    letters[order] = (float(q["xPos"]), float(q["yPos"]))
                    order += 1

        return letters_in_plate_info, letters_in_plate, letters_order, letters

    def kill_app(self):
        """
        Shut down the app
        """

        self.driver.close_app()
        #self.record_action("self.kill_app()", self.current_screen)

    def solve_one_word(self, answer):
        """
        solve one word
        parm: word to be solved
        format for parm : <any variable>='Any word'
        """

        self.solve_puzzle(None, None, answer)

    def get_answers_from_json(self, letters_in_plate):
        """
        Get answer from json
        Param: letter in the plate i =n format (["A","B","C")]
        """


        #mod
        answers_from_json = []
        for p in self.puzzle_json_data:
            letter_from_json = p["l"].split(":")
            if sorted(letter_from_json) == sorted(letters_in_plate):
                #og
                #answers_from_json = []
                for w_details in p["wp"]:
                    w = w_details.split(":")[3]
                    answers_from_json.append(w)
                break
        return letter_from_json, answers_from_json

    def solve_bonus_words(self):
        """
        Use to solve the bonus word if any exists in the current round
        """

        letters_in_plate_info, letters_in_plate, letters_order, letters = self.get_letters_in_plate()
        letter_from_json, answers_from_json = self.get_answers_from_json(letters_in_plate)
        possible_words = self.util.get_bonus_words(self.dictionary, letters_in_plate)
        bonuswords = []
        for p in possible_words:
            if p in answers_from_json:
                continue
            if len(p) >= 3:
                bonuswords.append(p)
        self.solve_puzzle(None, "fast", bonuswords)
        self.get_magic_logs()

    def solve_puzzle(self, puzzle_number=None, speed="fast", answer=None):
        """
        To solve the puzzle using the channing methods
        """

        answers_from_json = []
        if self.is_ftue_shown:
            speed = "slow"
        hints_freq = 4
        current_screen = self.current_screen
        action_name = "solve_puzzle"
        self.get_magic_logs()
        if puzzle_number is None:
            puzzle_number = self.puzzle_completed
        else:
            puzzle_number -= 1
        letters_in_plate_info, letters_in_plate,letters_order, letters = self.get_letters_in_plate()
        if answer is not None:
            if isinstance(answer, list):
                answers_from_json = answer
            elif isinstance(answer, str):
                answers_from_json.append(answer)
        else:
            letter_from_json, answers_from_json = self.get_answers_from_json(letters_in_plate)

            if sorted(letters_in_plate) != sorted(letter_from_json):
                print letter_from_json, letters_in_plate
                print "FAIL : Wrong letters in place"
                return False
            else:
                pass
                #print "PASS : JSON and letters in tile are matching"
        answers_from_json = sorted(answers_from_json, key=len)
        for a in answers_from_json:

            self.get_magic_logs()
            """new 2 line
            if Dictionary FTUE popups
            """
            if self.is_string_contains("Tap"):
                self.tap(x=509,y=406)
            if self.current_screen != "puzzle":
                return False
            #print a
            play = TouchAction(self.driver)
            first_letter = True
            letters_order_temp = letters_order.copy()
            # print letters_order, "Check this"
            for l in a:
                #print l
                #print l, first_letter
                #print letters_order_temp, "Temp"
                if first_letter:
                    for key_order, value_letter in letters_order_temp.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                        if value_letter == l:
                            letter_position = key_order
                            del letters_order_temp[key_order]
                            #print letters_order_temp, "Temp"
                            break
                    #TODO: Add generic function for notch device
                    play.press(x=letters[letter_position][0], y=letters[letter_position][1]+60)
                    first_letter = False
                    #time.sleep(0.1)
                else:
                    for key_order, value_letter in letters_order_temp.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                        if value_letter == l:
                            letter_position = key_order
                            del letters_order_temp[key_order]
                            #print letters_order_temp, "Temp"
                            break
                    # TODO: Add generic function for notch device
                    play.move_to(x=letters[letter_position][0], y=letters[letter_position][1]+60)
                    #time.sleep(0.1)
            play.release().perform()

            if speed == "fast":
                time.sleep(0.5)
            if speed == "slow":
                time.sleep(3)
        time.sleep(5)
        #self.record_action("solve_puzzle(" + puzzle_number + ", '" + speed + "')", current_screen)
        return True


    def solve_daily_puzzle(self, puzzle_date=None, speed="fast"):
        """
        Solve the Daily puzzle
        Parm : puzzle_data = if none then take the time from the device

        """

        self.get_magic_logs()
        if "ftue" in self.game_obj["dailyPuzzlePlayedId"]:
            puzzle_date = "00000000"
        if puzzle_date is None:
            puzzle_date_string = parser.parse(self.util.get_device_clock_string())
            puzzle_date = int(puzzle_date_string.strftime("%Y%m%d"))
        print puzzle_date
        puzzle_number = 0
        if puzzle_number is None:
            self.puzzle_completed = int(self.get_magic_data_loaded("game_data")["puzCompleted"])
        else:
            self.puzzle_completed = puzzle_number - 1

        letters_in_plate_info, letters_in_plate, letters_order, letters = self.get_letters_in_plate()

        for p in self.daily_puzzle_json_data:
            if p["i"] == str(puzzle_date):
                answers_from_json = []
                sort_populatiry = []
                answers_from_json_list = p["wp"]
                for a in answers_from_json_list:
                    answers_from_json.append(a.split(":")[3])
                    sort_populatiry.append(a.split(":")[4])
                print answers_from_json
                print "Daily Puzzle date: ", str(puzzle_date)
                letter_from_json = p["l"].split(":")
                print sorted(letter_from_json) , sorted(letters_in_plate)
                if sorted(letter_from_json) == sorted(letters_in_plate):
                    #answers_from_json = p["wp"].split(":")
                    random_sorted_answers = []
                    answers_popularity = {}
                    #random_sort = p["rs"].split(":")

                    answer_index = 0
                    for s in sort_populatiry:
                        answers_popularity[s] = answers_from_json[answer_index]
                        answer_index = answer_index + 1
                    sort_populatiry_sorted = sorted(sort_populatiry, reverse = True)
                    for s in sort_populatiry_sorted:
                        random_sorted_answers.append(answers_popularity[s])
                    '''
                    for i in sort_populatiry:
                        random_sorted_answers.append(answers_from_json[int(i)])
                    '''

                    #print random_sort
                    print random_sorted_answers
                    print sort_populatiry
                    print "PASS : JSON and letters in tile are matching"
                    break
                else:
                    print "FAIL", "Incorrect letters in plate and Json"
                    return False
            else:
                print "No puzzle for given puzzle date"

        answers_from_json = sorted(answers_from_json, key=len)
        print random_sorted_answers
        if not answers_from_json:
            print "No Daily puzzle found in Json for given puzzle date"

        for a in random_sorted_answers:
            self.get_magic_logs()
            if self.current_screen != "daily_puzzle" or self.is_ftue_shown:
                return False
            #print a
            play = TouchAction(self.driver)
            first_letter = True
            letters_order_temp = letters_order.copy()
            #print letters_order, "Check this"
            for l in a:
                #print l, first_letter
                #print letters_order_temp, "Temp"
                if first_letter:
                    for key_order, value_letter in letters_order_temp.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                        if value_letter == l:
                            letter_position = key_order
                            del letters_order_temp[key_order]
                            #print letters_order_temp, "Temp"
                            break
                    play.press(x=letters[letter_position][0], y=letters[letter_position][1])
                    first_letter = False
                    time.sleep(0.1)
                else:
                    for key_order, value_letter in letters_order_temp.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                        if value_letter == l:
                            letter_position = key_order
                            del letters_order_temp[key_order]
                            #print letters_order_temp, "Temp"
                            break
                    play.move_to(x=letters[letter_position][0], y=letters[letter_position][1])
                    time.sleep(0.1)
            play.release().perform()
            if speed == "fast":
                time.sleep(1)
            if speed == "slow":
                time.sleep(3)
        time.sleep(5)
        return True

    def update_puzle_completed(self, value):
        
        """
        Use to move to the x round without solving it
        parm : value = the number of rounds to be updated
        """

        try:
            sever_connection = self.ws.ws.connected
        except:
            self.get_magic_logs()
        self.ws.send({"command": "setPuzCompleted", "params": {"val": value}})



    def update_game_data(self,field, value):
        """
        Use in same way as update_puzzle_completed()
        """

        refid = self.user_obj["refId"]
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        game_data_list = {}
        payload = {
            'type': 'staging',
            'refid': refid,
            'game': 'jam',
            'change': '{"' + field + '":[' + "0" + ',' + str(value) + ']}'  # remember me
        }
        post_uri = "https://www.little-engine.com/api-gunicorn/gamedata/updateGame"
        result = requests.post(post_uri, data=payload, headers=headers)
        return result.status_code

    '''
    def get_random_action_index(self, possible_actions_index=None):
        if possible_actions_index is None:
            possible_actions_index = self.get_possible_actions_index()
        if len(possible_actions_index) > 0:
            random_index = random.randint(0,len(possible_actions_index))
            element_index = possible_actions_index[random_index]
            return element_index
        else:
            self.log("info", "No clickable element defined in this screen")
            return False

    def add_status_count(self, element_index):
        self.core[element_index]["status"] += 1

    def is_element_visible(self, element_index):
        for ql in self.qa_logs:
            if "spriteName" in ql.keys():
                if ql["spriteName"] == self.core[element_index]["Sprite_Name"]:
                    return ql, True
            elif "string" in ql.keys():
                if ql["string"] == self.core[element_index]["String"]:
                    return ql, True
            else:
                self.log("fail", "Incorrect element type")
        self.log("fail", "Element not shown")
        return [], False

    def get_random_clickable(self, possible_actions_index=None):
        if possible_actions_index is None:
            possible_actions_index = self.get_possible_actions_index()

        clickable_element_index = self.get_random_action_index(possible_actions_index)
        clickable_element = self.core[clickable_element_index]
        game_element, result = self.is_element_visible(clickable_element_index)
        if result:
            self.tap(game_element["xPos"], game_element["yPos"])
            self.log("info", "Tapping on below element")
            self.log("info", clickable_element)
            self.log("info", game_element)
            self.add_status_count(clickable_element_index)

    def get_possible_actions_index(self):
        possible_actions_index = []
        current_screen = self.get_current_screen()
        for key, c in self.core.items():
            if c["Current_Screen"] == current_screen and c["Clickable_Condition"] == "TRUE":
                possible_actions_index.append(key)
        return possible_actions_index

    '''