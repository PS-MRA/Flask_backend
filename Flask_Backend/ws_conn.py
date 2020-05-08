from websocket import create_connection
import json
#"ws://192.168.0.44:7681"
class ws():

    def __init__(self, url, timeout=5):
        try:
            self.ws = create_connection(url, timeout)
            print("Connected")
        except:
            print "Warning! - Problem in creating socket connection. Start connection manually"

    def send(self, command):
        data = json.dumps(command)
        try:
            self.ws.send(data)
        except:
            print "Connection error"
            return False
        try:
            result = self.ws.recv()
            return result
        except:
            print "Connection error"
            return False

    def close(self):
        self.ws.close()