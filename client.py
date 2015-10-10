import os
import websocket
import json
import urllib

from integrations.utilities import get_resource
 
def on_error(ws, error):
    print error
 
def on_close(ws):
    print "### closed ###"
 
def on_message(ws, message):
    print(message)

def on_open(ws):
    print "Connected"
 
if __name__ == "__main__":
    websocket.enableTrace(False)
    token = os.environ.get('TUTUM_TOKEN')
    username = os.environ.get('TUTUM_USERNAME')
    uuid = os.environ.get('CONTAINER_UUID')
    command = os.environ.get('COMMAND')
    TUTUM_AUTH = os.environ.get('TUTUM_AUTH')

    if TUTUM_AUTH:
        TUTUM_AUTH = TUTUM_AUTH.replace(' ', '%20')
        url = 'wss://stream.tutum.co/v1/container/' + uuid + '/exec/?auth={}'.format(TUTUM_AUTH)
    elif token and username:
        url = 'wss://stream.tutum.co/v1/container/' + uuid + '/exec/?token={}&user={}'.format(token, username)
    else:
        raise Exception("Please provide authentication credentials")
    encodedCommand = urllib.urlencode({'command' : command})
    url = url + "&" + encodedCommand
    ws = websocket.WebSocketApp(url, 
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
                                on_open = on_open)
 
    try:
        ws.run_forever()
    except KeyboardInterrupt:
        pass
