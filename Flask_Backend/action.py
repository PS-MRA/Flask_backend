import inspect
from threading import Thread
import constants as const
import time
import recorder
import sys
import json
import csv
import ast
import os
import numbers
reload(recorder)


class Action():
    def __init__(self, driver):
        self.driver = driver
        #self.step = 1
        self.step = -1
        #og
        self.game = None
        self.record = recorder.Record(driver)
        self.record_status = False
        self.driver_command = {}

    @staticmethod
    def build_params(params):
        """
        in built thread function takes the argument in forms of the tupple, so this function makes the raw argumnet in proper tuple form
        parm : params = the raw argumnet
        """

        args_option = None
        if params is not None:
            args_option = params[0],
            if len(params) > 1:
                for p in range(1, len(params)):
                    args_option += (params[p],)
            else:
                args_option = params[0],
        return args_option

    def build_params_playback(self, params):
        args_option = None
        if params is not None:
            if params[0] == "None":
                params[0] = None
            elif params[0] == "True":
                params[0] = True
            elif params[0] == "False":
                params[0] = False
            elif self.is_numeric(params[0]):
                if "." in params[0]:
                    params[0] = float(params[0])
                else:
                    params[0] = int(params[0])
            args_option = params[0],
            if len(params) > 1:
                for p in range(1, len(params)):
                    if params[p] == "None":
                        params[p] = None
                    elif params[p] == "True":
                        params[p] = True
                    elif params[p] == "False":
                        params[p] = False
                    elif self.is_numeric(params[p]):
                        if "." in params[p]:
                            params[p] = float(params[p])
                        else:
                            params[p] = int(params[p])
                    args_option += (params[p],)
            else:
                args_option = params[0],
        return args_option

    @staticmethod
    def is_numeric(obj):
        """
        used to check if the obj is number or not
        return true else false
        """
        if isinstance(obj, numbers.Number):
            return True
        elif isinstance(obj, str):
            try:
                nodes = list(ast.walk(ast.parse(obj)))[1:]
            except:
                return False
            if len(nodes) == 0:
                return False
            if not isinstance(nodes[0], ast.Expr):
                return False
            if not isinstance(nodes[-1], ast.Num):
                return False
            nodes = nodes[1:-1]
            for i in range(len(nodes)):
                # if used + or - in digit :
                if i % 2 == 0:
                    if not isinstance(nodes[i], ast.UnaryOp):
                        return False
                else:
                    if not isinstance(nodes[i], (ast.USub, ast.UAdd)):
                        return False
            return True
        else:
            return False

    def load_game(self, game_obj):
        """
        link the worjam.py in this file
        parms : game_obj = instance of the Game class
        """
        self.game = game_obj

    def execute(self, action_type,  params=None):
        """
        This function acts like a wrapper class and link the caller function to its desired state
        """
        #QUESTION : What is the use of run_name

        if self.game.run_name is not None:
            self.record_status = True
        if self.game.play_run_name is not None:
            self.record_status = True
        if self.game.run_name is None and self.game.play_run_name is None:
            print ("Warning", "Please enter Run name for recording/playback before execute")
            self.record_status = False

        launch_commands = ["launch_app", "clear_data"]
        #The below line is uded to find the name of the caller function name
        command = sys._getframe(1).f_code.co_name

        #Call the magic_logs() by providing the threshold time and launch_app status as True
        if self.step <= 0 and command not in launch_commands:
            self.game.get_magic_logs(5, True)

        driver = self.driver
        args = self.build_params(params)

        self.driver_command = {
            "launch_app" : driver.launch_app,
            "activate_app": driver.activate_app,
            "back": driver.back,
            "tap_sprite": self.action_tap_sprite,
            "tap_element" : self.game.tap_element,
            "reset_scroll_view_to_top": self.game.reset_scroll_view_to_top,
            "controlled_swipe_v": self.game.controlled_swipe_v,
            "tap":  self.game.tap,
            "start_record": self.game.record_run,
            "solve_puzzle": self.game.solve_puzzle,
            "solve_daily_puzzle" : self.game.solve_daily_puzzle,
            "kill_app" : driver.close_app,
            "get_pre_conditions" : self.record_pre_conditions,
            "assert_current_screen" : self.assert_current_screen_action_call,
            "solve_one_word" : self.game.solve_one_word,
            "fb_login_webview" : self.game.fb_login_webview,
            "solve_bonus_words" : self.game.solve_bonus_words,
            "background_app" : driver.background_app,
            "update_game_data" : self.game.update_game_data,
            "add_hours" : self.game.add_hours,
            "get_magic_logs" : self.game.get_magic_logs,
            "play_run" : self.game.play_run,
            "update_experiment" : self.game.update_experiment,
            "clear_data" : self.reset,
            "update_step_id" : self.stepid,
            "force_sync" : self.game.force_sync,
            "update_puzle_completed": self.game.update_puzle_completed,
            "get_results": self.export_results,
            "botplay": self.game.next_click
        }
        non_thread = ["solve_puzzle",
                      "solve_daily_puzzle",
                      "solve_one_word",
                      "fb_login_webview",
                      "solve_bonus_words",
                      "get_magic_logs"]
        wait_in_screen = {
            "outro": 3,
            "country_complete" : 5,
            "settings" : 2
        }
        if args is None:
            execute_command = Thread(target=self.driver_command[command])
        else:
            execute_command = Thread(target=self.driver_command[command], args=args)
        #print command, args
        execute_command.start()
        if command in non_thread:
            execute_command.join()

        if command not in launch_commands:
            try:
                time.sleep(wait_in_screen[self.game.current_screen])
            except:
                time.sleep(2)
                pass
            self.game.get_magic_logs(5)

        if self.record_status:
            return self._record(command, params, action_type)
        return True
        '''
        try:
            if args is None:
                execute_command = Thread(target=driver_command[command])
            else:
                execute_command = Thread(target=driver_command[command], args=args)
            execute_command.start()
            if command in non_thread:
                execute_command.join()
            self.step += 1
            self._record(command, params, action_type)
            return True
        except:
            print "error execute_command"
            return False

        '''
    def _record(self, command, params=None, action_type=None):
        """
        Use to write the log and save the screenshort in the proper file
        """

        if params is not None:
            if "fbLoginButton" in params:
                self.game.wait_for_element_by_class_name('android.widget.Image')
        skip_commands = ["start_record", "stop_record", "play_run", "stepid", "get_results"]
        if command in skip_commands:
            return None

        if action_type is None:
            print ("ERROR: ", "Action type is None")

        if const.RECORD_ACTIONS:
            self.step += 1
            data = [self.game.action.step, command, params, action_type, self.game.current_screen, time.time(), self.game.magic_json]
            self.record.action(data)
            #time.sleep(1)
            self.game.ss.save(str(self.step) + ".png")
            return data

            #print ("Record action " , command)
        else:
            print ("no record")
            return None

    def botplay(self, count):
        """
        Play the game
        parm:count=number of clicks it will perform
        It call the execute function and bind a thread for the next_click()
        """
        params = [count]
        return self.execute("action", params)

    def force_sync(self):
        return self.execute("action")

    def start_record(self, name):

        if name is not None:
            params = [name]
            self.record_status = True
            return self.execute("action", params)
        else:
            self.record_status = True
            return self.execute("action")

    def play_run(self, name):
        params = [name]
        self.record_status = False
        self.step = -1
        return self.execute("action", params)

    def clear_data(self):
        return self.execute("action")

    def get_magic_logs(self):
        return self.execute("action")

    def launch_app(self):
        return self.execute("action")

    def fb_login_webview(self, action_details=None):
        params = [action_details]
        return self.execute("action", params)

    def solve_one_word(self, word):
        params = [word]
        return self.execute("action", params)

    def activate_app(self, app_package=None):
        if app_package is None:
            app_package = str(self.driver.desired_capabilities["appPackage"])
        params = [app_package]
        record_data = self.execute("action", params)
        time.sleep(5)
        return record_data

    def update_puzle_completed(self, value):
        params = [value]
        return self.execute("action", params)

    def reset(self):
        self.driver.reset()
        time.sleep(15)

    def update_game_data(self, field, value):
        params = [field, value]
        return self.execute("action", params)

    def get_command_list(self):
        command_list = {}
        for k in self.driver_command:
            command_list[k] = k
        return json.dumps(command_list)

    def update_step_id(self, id):
        params = [id]
        return self.execute("action", params)

    def stepid(self, id):
        self.step = id

    def update_experiment(self, exp, var):
        params = [exp, var]
        return self.execute("update_experiment", params)

    def add_hours(self, hours):
        params = [hours]
        return self.execute("action", params)

    def assert_current_screen_action_call(self, current_screen, wait=20):
        start_time = time.time()
        end_time = start_time + wait
        while True:
            self.game.get_magic_logs(10)
            if current_screen == self.game.current_screen:
                return True
            else:
                if time.time() >= end_time:
                    return False
                continue

    def assert_current_screen(self, current_screen):
        params = [current_screen]
        return self.execute("action", params)

    def back(self):
        record_data = self.execute("action")
        time.sleep(2)
        return record_data

    def game_back(self):
        self.tap_sprite(const.GAME_BACK_SPRITE_NAME)
        time.sleep(2)

    def tap(self, x, y, take_snap=True, element_name=None, element_type=None):
        """
        Tap to specific location
        parm: x = x location
              y = y location

        """
        params = [x, y, take_snap, element_name, element_type]
        return self.execute("action", params)

    def tap_sprite(self, sprite_name, index=0):
        self.action_tap_sprite(sprite_name, index)

    def click_fb_login_button(self):
        self.tap_sprite("fbLoginButton")
        self.game.wait_for_element_by_class_name('android.widget.Image')

    def tap_element(self, qlg):
        element_data = self.game.get_element_position(qlg)
        if type(element_data) != bool:
            params = [qlg]
            return self.execute("action", params)
        return None

    def solve_puzzle(self, puzzle_number=None, speed="fast", answers=None):
        params = [puzzle_number, speed, answers]
        return self.execute("action", params)

    def solve_daily_puzzle(self, puzzle_date=None, speed="fast"):
        params = [puzzle_date, speed]
        return self.execute("action", params)

    def controlled_swipe_v(self, start, end):
        params = [start, end]
        return self.execute("action", params)

    def action_tap_sprite(self, sprite_name, index=0):
        """ Custom action tap sprites
        :param sprite_name: sprite name to tap from screen
        :return: Bool
        """
        #self.game.get_magic_logs(1)
        index_count = 0
        qa_logs = self.game.qa_logs
        #print(qa_logs)
        print(type(qa_logs))
        for qlg in qa_logs:
            try:
                name = qlg["name"]
            except:
                name = ""
            if name == sprite_name:
                print(name)
                print(sprite_name)
                if index_count == index:
                    #self.record_action("self.tap_sprite('" + sprite_name + "')", self.current_screen)
                    return self.game.tap_element(qlg)
                else:
                    index_count += 1
        return False

    def reset_scroll_view_to_top(self):
        return self.execute("action")

    def kill_app(self):
        return self.execute("action")

    def background_app(self):
        return self.execute("action")

    def get_pre_conditions(self):
        self.game.load_magic_logs_if_empty()
        data = self.game.magic_json
        params = [data]
        return self.execute("action")

    def record_pre_conditions(self, *argv):
        pass

    def start_playback(self, start_step=None, end_step=None):
        self.record_status = True
        failed = 0

        for p in self.game.play_run_data:
            step = int(p[0])
            if start_step is not None:
                if start_step != step:
                    continue

            action = p[1]
            action_type = p[3]
            landing_screen = p[4]
            if landing_screen == '':
                landing_screen = p[4]= None
            timestamp = p[5]
            if p[2] is not None and p[2] is not "":
                params = p[2].replace("'","").strip('][').split(', ')
                build_params = self.build_params_playback(params)
                command = ("self." + action + str(build_params))
            else:
                command = ("self." + action + '()' )
            r = eval(command)
            if r is not None and r is not False:
                if p[const.RECORD_LOG_POSITON.CURRENT_SCREEN] != r[const.RECORD_LOG_POSITON.CURRENT_SCREEN]:
                    failed += 1
                    print ("ERROR " + str(failed) + " : " + str(r[const.RECORD_LOG_POSITON.CURRENT_SCREEN]) +
                           " instead of '"+ str(p[const.RECORD_LOG_POSITON.CURRENT_SCREEN]) + "' for step " + str(step))
                else:
                    failed = 0
            else:
                failed += 1
            if failed >= const.MAX_FAILED_STEPS:
                print ("ERROR", "RUN FAILED - " + str(failed) + " steps failed continuously! Check record log for details.")
                return
            if end_step is not None:
                if end_step == int(p[0]):
                    return

    def get_results(self, playback_run_name):
        params = [playback_run_name]
        return self.execute("action", params)

    def export_results(self, playback_run_name):
        result = []
        screen_compare = {}
        try:
            base_run_name = playback_run_name.split("_",1)[1]
        except:
            print ("ERROR", "Please check the playback run folder name!")
        if  os.path.exists(base_run_name):
            base_screenshots_folder = base_run_name + "/screenshots"
            base_log = base_run_name + "/botlog.csv"
        else:
            print("ERROR: Given run name folder not found")
            return False
        playback_screenshots_folder = playback_run_name + "/screenshots"
        base_screenshots_arr = os.listdir(base_screenshots_folder)
        playback_screenshots_arr = os.listdir(playback_screenshots_folder)
        base_steps = self.game.load_play_run(base_run_name)
        playback_steps = self.game.load_playback_run(playback_run_name)

        for bs in range(0, len(base_screenshots_arr)):
            if ".png" not in base_screenshots_arr[bs]:
                continue
            base_screenshot_path = base_screenshots_folder + "/" + base_screenshots_arr[bs]
            playback_screenshot_path = playback_screenshots_folder + "/" + base_screenshots_arr[bs]
            if os.path.exists(playback_screenshot_path):
                error_value = str(self.game.util.is_similar(base_screenshot_path, playback_screenshot_path))
            else:
                error_value = "xxxxx"
            screen_compare[int(base_screenshots_arr[bs].split(".")[0])] = error_value
        for i in range(0, len(base_steps)):
            base_step_screen_name = base_steps[i][const.RECORD_LOG_POSITON.CURRENT_SCREEN]
            try:
                playback_step_screen_name = playback_steps[i][const.RECORD_LOG_POSITON.CURRENT_SCREEN]
            except:
                playback_step_screen_name = None
            step_id = base_steps[i][const.RECORD_LOG_POSITON.STEP_ID]
            if base_step_screen_name == playback_step_screen_name:
                result.append([base_steps[i][const.RECORD_LOG_POSITON.STEP_ID], "PASS", screen_compare[int(step_id)]])
            else:
                #print base_steps[i][const.RECORD_LOG_POSITON.STEP_ID] , "FAIL", screen_compare[int(step_id)] #, base_step_screen_name, playback_step_screen_name]
                result.append([base_steps[i][const.RECORD_LOG_POSITON.STEP_ID], "FAIL", screen_compare[int(step_id)], base_step_screen_name, playback_step_screen_name])

        with open(playback_run_name + "/result.csv", mode='a') as file:
            record_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, len(result)):
                record_writer.writerow(result[i])
        result = []

    def solve_bonus_words(self):
        return self.execute("action")









