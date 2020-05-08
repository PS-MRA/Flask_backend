'''import wordjam
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


test_launcher.driver_config(udid,port_number,0)
action=action.Action(test_launcher.driver)
word=wordjam.Game(test_launcher.driver)
action.load_game(word)
word.load_game(action)
game = wordjam

class Test:

    def __init__(self,driver):
        self.driver = driver
        self.action = action
        self.game = word
        self.const = const
        self.stack = []
        self.current_count = 0
        self.upto_screen = []
        self.cu_count = 0

    def test_1(self):
        self.action.clear_data()
        self.action.get_magic_logs()
        #self.action.start_record("test2")
        self.add_to_the_adj_list()

    def cmp(self, li1, li2):
        return li1["zindex"] < li2["zindex"]
    def add_to_the_adj_list(self):

        self.action.get_magic_logs()
        self.game.group_qa_logs()
        #elements = self.game.group_qa_logs()
        #list_to_be_add = elements["BUTTONS"]
        #dd = sorted(list_to_be_add,cmp = self.cmp)
        #list_to_be_add = []
        #list_to_be_add = dd
        #print(dd)

        #sorting tryings


        list_to_be_add = self.game.get_buttons_only(word.qa_logs)
        if self.game.current_screen not in self.upto_screen:
            random.shuffle(list_to_be_add)

            for x in range(0,len(list_to_be_add),1):
                self.stack.append(list_to_be_add[x])
            self.upto_screen.append(self.game.current_screen)
        print("Clickec items")
        print(word.clicked_elements)
        size = len(self.stack)

        for x in range (0, size , 1):
            self.cu_count += 1
            print("Len of stack")
            print(len(self.stack))
            if self.game.current_screen == "puzzle" and (self.current_count >= 14 or len(self.stack)==0):
                self.action.solve_puzzle()
                self.stack = []
                self.upto_screen = []
                print(len(self.stack))
                print("Clear")
                self.current_count = 1
                self.add_to_the_adj_list()
            elif word.current_screen == "bonus_words":
                self.action.back()
                print(list_to_be_add)

            elif(len(self.stack) > 0):

                li = self.stack.pop()
                prev_screen = word.current_screen
                if li["name"] == 'openDictionary' or li["name"] == "checkAndShowNativeMagicPopup":
                    continue
                else:
                    self.current_count += 1
                    print(li)
                    self.action.tap_element(li)
                    if prev_screen != word.current_screen:
                        self.stack = []
                        self.add_to_the_adj_list()
            if(len(self.stack) == 0):
                self.upto_screen = []
                self.add_to_the_adj_list()

        if(self.cu_count > 100):
            self.action.record_status = False
            return







a=Test(test_launcher.driver)
a.test_1()


'''

import wordjam
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
f = open("just.txt", 'a')

class Test:
    def __init__(self,driver):
        self.driver = driver
        self.action = action
        self.game = word
        self.const = const
        self.screen_count = []
        self.check_list = ['checkAndShowNativeMagicPopup',"showBonusScreen",'showQuestCenter',"openDictionary","showPurchase"]
        self.caller = "launcheer"
        self.screen_coun = []
        self.universal_count = 0
        self.already_in_stack = []

    def chhhh(self):
        self.screen_count = []
        self.already_in_stack = []
    def initilize(self):
        self.action.clear_data()

        self.action.get_magic_logs()
        self.action.start_record("test3")

        self.start()


    def start(self):
        if self.game.current_screen == "fblogin":
            self.action.fb_login_webview()
        if self.universal_count%8 == 0 and self.game.current_screen == "puzzle":
            self.game.solve_puzzle()
            self.chhhh()
            return -1
        print("NEWWwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwddwwwwwEWWwWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
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
        if len(buttons) <= 0:
            self.action.back()
        if self.game.current_screen not in self.screen_coun:
            random.shuffle(buttons)
            for x in range(0,len(buttons),1):
                if buttons[x]["name"] in self.already_in_stack:
                    continue
                else:
                    stack.append(buttons[x])
                    self.already_in_stack.append(buttons[x]["name"])
                    print(buttons[x])
            self.screen_count.append(self.game.current_screen)

        size = len(stack)
        print(
            "NEWWwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwddwwwwwEWWwWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
        print(size)

        for x in range(0, size, 1):
            if self.game.current_screen == "puzzle" and count >= 3 or len(buttons) == 0:
                self.action.solve_puzzle()
                self.chhhh()
                return -1
            else:
                li = stack.pop()
                count += 1
                prev_screen = self.game.current_screen
                self.universal_count += 1
                print(li)
                print(li["name"])
                self.action.tap_element(li)
                self.action.get_magic_logs()
                print("!**! "+ prev_screen+" "+self.game.current_screen)
                if prev_screen != self.game.current_screen:
                    for a in range(0,7):
                        print("\n")
                    print("!**! " + prev_screen + " " + self.game.current_screen)
                    print(prev_screen +" "+self.game.current_screen)
                    #if count == 1:
                    f.write(prev_screen +" "+self.game.current_screen+"\n")
                    d = self.start()
                    if( d == -1):
                        self.start()
                        break
        return 1



a = Test(test_launcher.driver)
a.initilize()
print("a.start is called")
a.start()
a.chhhh()
a.start()
a.chhhh()
a.start()
a.chhhh()
f.close()








