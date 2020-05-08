import operator
#import cv2
import numpy as np
import requests
import time
import sys



class Util():
    def __init__(self, driver):
        self.driver = driver
        self.log_tags_to_print = {
                                    "debug": 1,
                                    "info": 0,
                                    "result": 0,
                                    "error": 0
                                  }

    def is_element_inside_box(self, parent, child):
        #return (child["xPos"] >= parent["start_point"][0] and child["yPos"] >= parent["start_point"][1]) and (child["xPos"] <= parent["end_point"][0] and child["yPos"] <= parent["end_point"][1])
        return (child["start_point"][0] >= parent["start_point"][0] and child["start_point"][1] >= parent["start_point"][1]) and (child["end_point"][0] <= parent["end_point"][0] and child["end_point"][1] <= parent["end_point"][1])

    def get_box_position(self, ql):
        '''
        ql["start_point"] = (0,0)
        ql["end_point"] = (0,0)
        return ql
        '''
        boundbox = ql["boundbox"]
        xPos, yPos, h, w = boundbox["x"], boundbox["y"], boundbox["height"], boundbox["width"]
        # TODO aanchor logic to be verified
        #
        '''
        new try and catch around the statement as it contains none
        '''
        ql["start_point"] = (xPos, yPos)
        ql["end_point"] = (xPos + w, yPos + h)

        #ql["start_point"] = (xPos - (w * ql["anchorX"]), yPos - (h * ql["anchorY"]))
        #ql["end_point"] = (xPos + (w * (1 - ql["anchorX"])), yPos + (h * (1 - ql["anchorY"])))
        return ql

    def get_device_clock_string(self):
        return self.driver.device_time

    @staticmethod
    def is_similar(image1path, image2path):
        print image1path, image2path
        image1 = cv2.imread(image1path, 0)
        image2 = cv2.imread(image2path, 0)
        # the 'Mean Squared Error' between the two images is the
        # sum of the squared difference between the two images;
        # NOTE: the two images must have the same dimension
        err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
        err /= float(image1.shape[0] * image2.shape[1])

        # return the MSE, the lower the error, the more "similar"
        # the two images are
        return err
        if err == 0.0:
            return True
        else:
            return False

    def new_fb_test_user(self):
        app_access_token = "465855800479707|jbD-Pb48ufENk_LexlpPwMHhlw4"
        r = requests.post("https://graph.facebook.com/v4.0/1778394085519552/accounts/test-users?access_token=" + str(
            app_access_token))
        return r.json()

    def wait_for_element_by_id(self, id, timeout=None):

        now = time.time()
        if timeout is None:
            timeout = now + 10
        else:
            timeout = now + timeout
        while True:
            try:
                elem = self.driver.find_element_by_id(id)
                if elem.is_displayed():
                    print("info", "Element is shown")
                    return True
                    break
                else:
                    log("info", "Element is not shown")
            except:
                if time.time() >= timeout:
                    print("info", "Element is not shown")
                    return False
                else:
                    print("info", "Waiting for element")
                    time.sleep(1)

    def charCount(self, word):
        #Count the Frequency of the char repeated in the word
        dict = {}
        for i in word:
            dict[i] = dict.get(i, 0) + 1
        return dict

    """new function"""
    def logger(self,tag,msg=None):
        command = sys._getframe(1).f_code.co_name
        if(self.log_tags_to_print[tag] == 1):
            if tag == "debug":
                print("Executing "+ str(command) +" function - " + msg)
            else:
                print (tag, msg)



    def possible_words(self, lwords, charSet):
        words_list = []
        for word in lwords:
            word = word.upper()
            flag = 1
            chars = self.charCount(word)
            for key in chars:
                if key not in charSet:
                    flag = 0
                else:
                    if charSet.count(key) != chars[key]:
                        flag = 0
            if flag == 1:
                words_list.append(word)
        return words_list

    def get_bonus_words(self, dictionary, charset):
        input = dictionary
        return self.possible_words(input, charset)


ops = {
    "eq": operator.eq,
    "gt": operator.gt,
    "lt": operator.lt,
    "ge": operator.ge,
    "le": operator.le,
    "ne": operator.ne
}