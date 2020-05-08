import subprocess
import re
import time
from appium import webdriver
import urllib
import argparse
import json
import importlib
from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

'''
parser = argparse.ArgumentParser()
parser.add_argument('-p' , '--port', help ="port number" , required=True, type=str)
parser.add_argument('-os' , '--os', help ="OS" , required=True, type=int)
parser.add_argument('-u' , '--u', help ="UDID" , required=True, type=str)
parser.add_argument('-g' , '--g', help ="GAME" , required=True, type=str)
parser.add_argument('-s' , '--scenario', help ="ScenarioId" , required=False, type=str)
args = parser.parse_args()

port_number = args.port.split(",")
scenario_id = args.scenario
os = args.os
udid = args.u.split(",")
appium_os_type = os
driver = None
drivers = None
game = args.g
'''
port_number = ["4723"]
scenario_id = "test_runner"
os = 0
#og
udid = ["192.168.1.108:5555"]
appium_os_type = 0
driver = None
drivers = None
game = "wordtrip"
#game = 'wordjam'

desired_capabilities = {}

def config_action(udid, port_number):

    while 1:
            found = False
            if os == 0:
                output = subprocess.check_output(["adb", "devices"])
            elif os == 1:
                return True
                output = subprocess.check_output("/usr/bin/instruments -s devices | grep -Ev 'Simulator|PSG-LAP|Known Devices' | awk {'print $3'}", shell=True)
            output = re.split(r'[\n\t]+', output)
            avl_devices = []
            devices = []
            for o in output:
                if os == 0:
                    if not (o.isalpha() or not o.isalnum()):
                        avl_devices.append(o)
                if os == 1:
                    if o is not "":
                        o = o.replace("[", "")
                        o = o.replace("]", "")
                        avl_devices.append(o)
            print "Number of devices connected : " + str(len(avl_devices))
            #p = subprocess.Popen(["appium", "-U 30045d57d83c3100"], stdin=None, stdout=None, stderr=None)
            for d in avl_devices:
                if os == 0:
                    command = "adb -s " + str(d) + " shell getprop | grep -E 'product.model|product.brand'"
                elif os == 1:
                    break
                    command = "instruments -s devices | grep -E '"+str(d)+"' | awk {'print $3'}"
                #command = command.split()
                details = subprocess.check_output(command, shell=True)
                details = details.replace(" ", "")
                details = details.replace("\r\n", ":")
                details = details.replace("\n", ":")
                details = details.split(":")
                print details
                if os == 0:
                    devices.append([d,details[1], details[3]])
                if os == 1:
                    details[0] = details[0].replace("[","")
                    details[0] = details[0].replace("]", "")
                    details[0] = details[0].replace("\n", "")
                    devices.append([details[0]])
            #devices = [udid]

            print devices
            for d in devices:
                found = False
                start = []
                print d[0],udid
                print udid
                if d[0] == udid:
                    choice = ""
                    check_process = "ps | grep -E 'node' | grep -Ev 'grep' | awk {'print $7'}"
                    check_process_output = subprocess.check_output(check_process, shell=True)
                    check_process_output = check_process_output.splitlines()
                    if d[0] not in check_process_output:
                        statement = "Start appium server for device id : " + d[0]
                        if os == 0:
                            statement = statement + " device model : " + d[2] + " device brand : " + d[1] + ": (Y/N) : "
                        if os == 1:
                            statement = statement + ": (Y/N) : "
                        print statement
                        choice1 = str(raw_input())
                        if choice1 == "y" or choice1 == "Y":
                            command = "/usr/local/bin/appium -U " + d[0] + " -p " + str(port_number)
                            command = command.split()
                            devnull = open('/dev/null', 'w')
                            server_init = subprocess.Popen(command, stdout=devnull, stderr=None, stdin=devnull)
                            time.sleep(5)
                            if os == 0:
                                print "Initiated appium server for device id " +  d[0] + " device model : " + d[2] + " device brand : " + d[1]
                            if os == 1:
                                print "Initiated appium server for device id " + d[0]
                            found = True
                            return True
                        else:
                            found = True
                            return False
                    else:
                        found = True
                        print "Server is already running for device id : " + d[0] + " Restart : (Y/N) : "
                        choice2 = str(raw_input())
                        if choice2 == "y" or choice2 == "Y":
                            print "Killing and restarting the server..."
                            check_for_kill = subprocess.check_output("ps | grep -E 'node' | grep -Ev 'grep' | awk {'print $1'}", shell=True)
                            check_for_kill = check_for_kill.splitlines()
                            for i in range(0, len(check_process_output)):
                                if check_process_output[i] == d[0]:
                                    print "kill -9 " + str(check_for_kill[i])
                                    server_kill = subprocess.check_output("kill -9 " + str(check_for_kill[i]), shell=True)
                                    print "Killed successfully!!!"
                                    command = "/usr/local/bin/appium -U " + d[0] + " -p " + str(port_number)
                                    print d[0]
                                    command = command.split()
                                    devnull = open('/dev/null', 'w')
                                    server_init = subprocess.Popen(command, stdout=devnull, stderr=None)
                                    time.sleep(10)
                                    if os == 0:
                                        print "Initiated appium server for device id " + d[0] + " device model : " + d[2] + " device brand : " + d[1] + " on port number : " + str(port_number)
                                    if os == 1:
                                        print "Initiated appium server for device id " + d[0]
                                    found = True
                                    return True
                        else:
                            print "Tester decision : [END]"
                            found = True
                            return False
                            break
                        break
            if found != True:
                print "Device not connected!!!"
                return False
    return False
            #print "Invalid input!!!"


def driver_config(udid,port_number, appium_os_type):
    global driver, desired_capabilities
    start_driver = []
    drivers = {}
    for u in range(0, len(udid)):
        start_driver.append(True)
        #start_driver.append(config_action(udid[u], int(port_number[u])))
        if start_driver[u] == True:
            print "Appium driver running..."

        desired_capabilities = {}

        if appium_os_type == 1:
            # Ios
            desired_capabilities['platformVersion'] = '12.14'
            desired_capabilities['deviceName'] = str(udid)
            #desired_capabilities['xcodeConfigFile'] = '/usr/local/lib/node_modules/appium/node_modules/appium-xcuitest-driver/WebDriverAgent/Config.xcconfig'
            desired_capabilities['platformName'] = 'iOS'
            desired_capabilities['automationName'] = 'XCUITest'
            desired_capabilities['bundleId'] = 'in.playsimple.tripcross'
            desired_capabilities['newCommandTimeout'] = 10000
            desired_capabilities["xcodeOrgId"] = "JVW9JEZL9R"
            desired_capabilities["xcodeSigningId"] = "iPhone Developer"
            #desired_capabilities["wdaLocalPort"] = 8100
            #desired_capabilities["wdaBaseUrl"] = "http://127.0.0.1"
        elif appium_os_type == 0:
            ## Android
            desired_capabilities['platformName'] = 'Android'
            desired_capabilities["automationName"] = 'UiAutomator2'
            #desired_capabilities['app'] = '/Users/fazilmajeeth/Downloads/wordup_april6.apk'
            desired_capabilities['appActivity'] = 'org.cocos2dx.javascript.AppActivity'
            if game == "wordtrip":
                desired_capabilities['appPackage'] = 'in.playsimple.wordtrip'
            if game == "wordjam":
                desired_capabilities['appPackage'] = 'in.playsimple.tripcross'
            desired_capabilities['deviceName'] = str(udid)
            desired_capabilities['newCommandTimeout'] = 10000
            desired_capabilities['noReset'] = 'true'
            #desired_capabilities['automationName'] = "UiAutomator2"

        desired_capabilities['autoLaunch'] = 'false'
        #print start_driver
        if start_driver[u] == True:
            #print "Driver - " + str(start_driver[u])
            print "Connecting appium driver for device id : " + udid[u] + " on port number : " + port_number[u]
            drivers[u] = webdriver.Remote('http://127.0.0.1:' + port_number[u] + '/wd/hub', desired_capabilities)
            #webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities)
            time.sleep(30)

        if len(drivers) != 0:
            driver = drivers[0]
        else:
            print "ERROR in configuration!!!!!"
            exit()


def import_scenario(scenario_id):

    i = importlib.import_module(scenario_id)
    reload(i)
    run_test = i.Test(driver)
    return run_test

@app.route('/')
def hello():

    return render_template('index.html')

test = None;

@app.route('/start_appium')
def start_appium():
    global test
    driver_config(udid, port_number, appium_os_type)
    if scenario_id is not None:
        test = import_scenario(scenario_id)
    return json.dumps(True)

@app.route('/get_appium_status')
def get_appium_status():
    if test is None:
        return json.dumps(False)
    else:
        return json.dumps(True)

@app.route('/action/<command>', methods=['GET'])
def command(command):
    action_cmd = "test.action." + format(command)
    args = request.args
    print "ARGS:", args
    first_param = True
    action_cmd += "("
    for arg in args:
        print request.args.get(arg)
        if not first_param:
            action_cmd += ","
        action_cmd += request.args.get(arg)
        first_param = False
    action_cmd += ")"
    print "ACTION:" , action_cmd
    result = eval(action_cmd)
    return json.dumps(result)

@app.route('/refresh')
def refresh():
    global test
    test = import_scenario(scenario_id)
    return hello()

if __name__ == '__main__':
    app.run()
    #start_appium()


'''
if __name__ == "__main__":
    driver_config(udid,port_number,appium_os_type)
    if scenario_id is not None:
        test = import_scenario(scenario_id)
'''