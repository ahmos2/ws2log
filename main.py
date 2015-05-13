import json,syslog,argparse
from ws4py.client.threadedclient import WebSocketClient

class wslogclient(WebSocketClient):
    def opened(self):
        syslog.syslog(syslog.LOG_INFO, "Connection opened")
    def closed(self, code):
        syslog.syslog(syslog.LOG_EMERG, "Connection closed")
    def received_message(self, message):
        obj=json.loads(str(message))
        if obj["type"] == "error":
            syslog.syslog(syslog.LOG_EMERG, str(message))
        elif obj["type"] == "alive":
            syslog.syslog(syslog.LOG_INFO, str(message))
        else:
            print "Unknown type",str(message)

parser=argparse.ArgumentParser()
parser.add_argument('websocket',default='wss://128.39.165.228:8080/ws')
args=parser.parse_args()

client=wslogclient(args.websocket)
client.daemon=False
syslog.openlog('ws2log',syslog.LOG_PID|syslog.LOG_CONS|syslog.LOG_PERROR)

client.connect()
