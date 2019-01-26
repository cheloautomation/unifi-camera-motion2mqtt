# Unifi Camera Motion

This is a python 2 script that will tail the logs file for the camera motion and will publish a mqtt topic "camera/motion/'camera name'" with payload of 'MOTION' or 'NO motion'.

This script needs to be running in the unifi video server as root or unifi-video user, in my case I put it in a cron job to start it after reboot. 

The logs this script is scrapping are "/var/lib/unifi-video/logs/motion.log"

## Script camera-motion.py configs

In the script, under the main function, you need to modify the cameras dictionary and the mqtt_ip for your own broker. The camera ID can be retrieve from the monito.log file:
```bash
1548533355.286 2019-01-26 15:09:15.286/EST: INFO   Camera[camera_id] type:start event:6831 clock:3115655514 (Kitchen) in ApplicationEvtBus-12
1548533396.094 2019-01-26 15:09:56.094/EST: INFO   Camera[camera_id] type:stop event:4994 clock:3115702948 (Living Room) in ApplicationEvtBus-19
```
This is how you need to structure the cameras dictionary:
```python
cameras = {
  "camera_id_1": "camera_name",
  "qwer12345": "livingroom",
  "qwer12346": "kitchen"
}
```

## Home Assistant configs
```python
sensor:
  - platform: mqtt
    name: "Kitchen Camera Motion"
    state_topic: 'camera/motion/kitchen'
    
  - platform: mqtt
    name: "Livingroom Camera Motion"
    state_topic: 'camera/motion/livingroom'
    
```

