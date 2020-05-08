
import wordjam
from appium.webdriver.common.touch_action import TouchAction
import test_launcher
import csv
import time
from dateutil import parser
import action
import constants as const
import random

reload(wordjam)
reload(action)
udid = ["192.168.1.108:5555"]
port_number = ["4723"]

test_launcher.driver_config(udid, port_number, 0)
action = action.Action(test_launcher.driver)
word = wordjam.Game(test_launcher.driver)
action.load_game(word)
word.load_game(action)
game = wordjam
record_of_count = {}
universal_count = 1
level_completd_till_now = 26
SIZE_OF_MAP = 43
var_fixed = 0
count = -1
var_count = 0
exp_count = -1

class Test:
    def __init__(self,driver):
        self.driver = driver
        self.action = action
        self.game = word
        self.const = const
        self.screen_count = []
        self.check_list = ["openDictionary","showPurchase","openDailyPuzzle",'loginToFb']
        self.screen_coun = []
        self.already_in_stack = []
        self.already_in_stac = []
        self.exp =0
        self.var = 1

    def scratch(self, x, y):
        """
        To scratch the scratch card:
        params: x,y coordinate of the scratch card in the screen
        """
        play = TouchAction(self.driver)
        for x in range(0,4):
            play.press(x=x-400,y=y)
            play.move_to(x=x+700,y=y)
        play.release().perform()
        xx=self.game.string_button_pos("CONTINUE")
        try:
            if(len(xx)):
                self.game.tap(x=xx[0],y=xx[1])
        except:
            pass

    def clean(self):
        """
        not use
        """
        self.screen_count = []
        self.already_in_stack = []


    def initialize(self):
        """
        do the basic task to get start
        """
        global y
        # self.action.clear_data()
        self.game.update_experiment("linear_progression", 0)
        self.action.get_magic_logs()
        self.action.start_record("test18")
        y = self.game.get_experiment_name_and_variants()
        self.game.update_experiment("linear_progression", 0)
        # y = eval(y)
        self.start()

    def select_the_active(self):
        """
        To select the active level from the puz pack screen and country screen
        """
        self.game.tap_sprite("#white_arrow.png")

    def solve_purchase_screen(self,ql):
        """
        TODO :FIX the purchase screen
        """
        self.action.tap_element(ql)
        self.driver.implicitly_wait(5000)
        if self.game.current_screen == "purchase_confirmation_screen":
            self.driver.implicitly_wait(5000)
            self.action.tap(350,1450)
            self.driver.implicitly_wait(5000)

    def change_experiment(self):
        """
        To change the experiment after every puzzle
        """
        x = self.get_experiment_name()
        self.game.update_experiment(x[0], x[1])
        #time.sleep(5)


    def get_experiment_name(self):
        """
        Use the json file store in the global variable y to get the experiment name and experiment variant
        """
        global var_fixed
        global count
        global exp_count
        global var_count
        global y
        experiment_name = None
        experiment_variant = None
        try:
            if (var_fixed > var_count):
                experiment_name = y["arr"][exp_count]["expName"]
                experiment_variant = y["arr"][exp_count]["variant"][var_count]["name"]
            else:
                count += 1
                exp_count += 1
                var_count = 0
                experiment_name = y["arr"][exp_count]["expName"]
                experiment_variant = y["arr"][exp_count]["variant"][var_count]["name"]
                var_fixed = len(y["arr"][exp_count]["variant"][var_count])
            return [experiment_name,experiment_variant]

        except:
            count = 0
            var_fixed = 0
            self.get_experiment_name()

    def start(self):
        """
        Main function to run the script
        """
        f=open("transition_of_screen.txt", 'a')
        global record_of_count
        global universal_count
        global level_completd_till_now
        global var_count

        if self.game.current_screen == 'bonus_words':
            x = self.game.string_button_pos("Back to puzzle")
            self.action.tap(369, 1150)
        try:
            self.game.get_magic_logs()
        except:
            pass
        if self.game.current_screen == "loginToFb":
            self.action.fb_login_webview()

        if (universal_count%15 == 0  or universal_count%18 == 0) and self.game.current_screen == "puzzle":
            self.game.solve_puzzle()
            var_count += 1
            # self.change_experiment()
            return

        count = 0
        button = self.game.group_qa_logs()
        temp_buttons = button["BUTTONS"]
        stack = []
        Set = set()
        buttons=[]
        for x in range(0,len(temp_buttons)):
            y=temp_buttons[x]["name"]
            size=len(Set)
            Set.add(y)
            if(size < len(Set) and temp_buttons[x]["name"] not in self.check_list):
                buttons.append(temp_buttons[x])
        temp_stack = []

        for x in range(0,len(buttons),1):
            if buttons[x]["name"] not in record_of_count.keys():
                record_of_count[buttons[x]["name"]] = 1
            temp_stack.append((buttons[x],record_of_count[buttons[x]["name"]]))
        temp_stack.sort(key=lambda x : x[1],reverse=True)
        size = len(temp_stack)


        while(len(temp_stack)):
            if self.game.current_screen == "puzzle" and count >= 3:
                self.action.solve_puzzle()
                var_count += 1
                # self.change_experiment()
                return
            else:
                li = temp_stack.pop()
                count += 1
                prev_screen = self.game.current_screen
                universal_count += 1
                if li[0]["name"] in record_of_count.keys():
                    record_of_count[li[0]["name"]] += 1

                if li[0]["layerType"] == "scroll":
                    self.game.reset_scroll_view_to_top()

                if (li[0]["name"] == "showPickHintScreen"):
                    xx = self.game.get_letter_in_tiles()
                    self.action.tap_element(li[0])
                    try:
                        self.action.tap(xx[0][0], xx[0][1])
                    except:
                        pass

                elif self.game.current_screen == "puz_pack" or self.game.current_screen == "country":
                    self.select_the_active()


                elif self.game.current_screen == "showPurchase":
                    self.solve_purchase_screen(li[0])

                elif self.game.current_screen == "purchase_confirmation_screen":
                    self.action.tap(400,1380)
                    self.driver.implicitly_wait(5000)

                elif (li[0]["name"] == "showScratchCard"):
                    self.action.tap_element(li[0])
                    try:
                        xx = self.game.string_button_pos("Scratch")
                        print(xx)
                        self.scratch(self.game.width/2,xx[1]-150)
                    except:
                        pass

                elif li[0]["name"] == "loginToFb":
                    self.action.tap_element(li[0])
                    self.action.fb_login_webview()
                    self.start()
                    temp_stack = []

                else:
                    self.action.tap_element(li[0])
                    if prev_screen != self.game.current_screen:
                        f.write(prev_screen + " " + self.game.current_screen + "\n")
                        f.close()
                        temp_stack = []
                        self.start()



        return




a = Test(test_launcher.driver)
a.initialize()

i = 0
for x in range(0,500,1):
    a.start()
    a.clean()

    if word.is_target_app_open() == False and word.current_screen != "purchase_confirmation_screen":
        test_launcher.driver.launch_app()



print(word.qa_logs)





















