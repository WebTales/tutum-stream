import os
import tutum

def on_message(event):
    if event.get("state", "") not in ["In progress", "Pending", "Terminating", "Starting", "Scaling", "Stopping"] and event.get("type", "").lower() in ["container", "service"]:
        msg = "Tutum event: %s %s is %s" % (event["type"], str(event.get("resource_uri", "")).split('/')[-2], event["state"].lower())
        print(msg)
 
if __name__ == "__main__":
    events = tutum.TutumEvents()
    events.on_message(on_message)
    events.run_forever()