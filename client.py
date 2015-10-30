import os
import tutum
 
def on_error(event):
    print error
 
def on_close(event):
    print "### closed ###"
 
def on_message(event):
    if event.get("state", "") not in ["In progress", "Pending", "Terminating", "Starting", "Scaling", "Stopping"] and event.get("type", "").lower() in ["container", "service"]:
        msg = "Tutum event: %s %s is %s" % (event["type"], parse_uuid_from_resource_uri(event.get("resource_uri", "")), event["state"].lower())
        print(msg)

def on_open(event):
    print "Connected"
 
if __name__ == "__main__":
    events = tutum.TutumEvents()
    events.on_open(on_open)
    events.on_close(on_close)
    events.on_message(on_message)
    events.run_forever()