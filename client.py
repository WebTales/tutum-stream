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
    msg_as_JSON = json.loads(message)
    type = msg_as_JSON.get('type')
    action = msg_as_JSON.get('action')
    name = msg_as_JSON.get('name')
    state = msg_as_JSON.get('state')
    resource_uri = msg_as_JSON.get('resource_uri')
    if type:
        if type == 'container' and state == 'running':
            container_uuid = str(resource_uri).split('/')[-2]
            service = get_resource(parents[0])
            service_as_JSON = json.loads(service)
            image_name = service_as_JSON.get('image_name')
            image_name = service_as_JSON.get('image_name')
            if 'apache' in service.image_name or 'nginx' in service.image_name:
                print('New web container : ' + container_uuid + 'is running')

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
        #url = 'wss://stream.tutum.co/v1/container/' + uuid + '/exec/?auth={}'.format(TUTUM_AUTH)
        url = 'wss://stream.tutum.co/v1/events?auth={}'.format(TUTUM_AUTH)
    elif token and username:
        #url = 'wss://stream.tutum.co/v1/container/' + uuid + '/exec/?token={}&user={}'.format(token, username)
        url = url = 'wss://stream.tutum.co/v1/events?token={}&user={}'.format(token, username)
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
