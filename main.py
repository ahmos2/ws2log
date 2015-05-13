import json
import syslog
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

client=wslogclient('wss://128.39.165.228:8080/ws')
client.daemon=False
syslog.openlog('ws2log',syslog.LOG_PID|syslog.LOG_CONS|syslog.LOG_PERROR)

client.connect()
