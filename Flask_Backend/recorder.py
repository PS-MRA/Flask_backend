import constants as const
import csv
reload(const)

class Record():
    def __init__(self, driver):
        self.driver  = driver
        self.batch_data = []

    def action(self, data):
        #self.record_batch.append((self.step, element, "click", screen, str(self.game_obj), timestamp))
        self.batch_data.append(data)
        if len(self.batch_data) >= const.BATCH_UPDATE_LENGTH:
            print "Write file path : " + const.BOT_LOG_FILE_PATH;
            with open(const.BOT_LOG_FILE_PATH, mode='a') as file:
                record_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in range(0, len(self.batch_data)):
                    #print self.batch_data[i]
                    record_writer.writerow(self.batch_data[i])
            self.batch_data = []


