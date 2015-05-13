import json,syslog,argparse,base64
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
parser.add_argument('--websocket',default='wss://128.39.165.228:8080/ws')
parser.add_argument('--syslogname',default="ws2log")
parser.add_argument('--username',default="ws2log")
parser.add_argument('--password',default="ws2log")
args=parser.parse_args()

if args.username:
    client=wslogclient(args.websocket, headers=[("Authorization: Basic ",base64.b64encode(args.username+":"+args.password))])
else:
    client=wslogclient(args.websocket)
client.daemon=False
syslog.openlog(args.syslogname,syslog.LOG_PID|syslog.LOG_CONS|syslog.LOG_PERROR)
client.connect()
