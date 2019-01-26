#!/usr/bin/python2.7

from subprocess import Popen, PIPE
import re
import paho.mqtt.client as mqtt

def run_cmd(cmd):
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def inotify(log_file):
    cmd = ['/usr/bin/inotifywait', '-e', 'modify', '--format', '%e', log_file]
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line.decode('utf-8')

def motion(log_file, cameras):
    (camera_data, _) = run_cmd(['/usr/bin/tail', '-n1', log_file])
    regex = '.*INFO\s\s\s\w+\[(?P<camera_id>\w+)\]\stype:(?P<type>\w+).*'
    match = re.match(regex, camera_data)
    if match:
        for cam_id, cam_name in cameras.items():
            if match.group('camera_id') == cam_id:
                return {'cam_name': cam_name, 'motion_type': str(match.group('type'))}

def mqtt_publish(mqtt_ip, topic, message):
    client = mqtt.Client('Cameras') #MQTT Client name, could be anything but needs to be unic
    client.connect(mqtt_ip)
    client.publish('camera/motion/{}'.format(topic), message)

def main():
    cameras = {
   #'camera id': 'given name for camera'
    'FCECDA1F1B84': 'livingroom',
    'FCECDA1F1E25': 'kitchen'
    }
    mqtt_ip = '192.168.1.100' # IP address of your MQTT Broker
    log_file = '/var/lib/unifi-video/logs/motion.log'
    while True:
        for event in inotify(log_file):
            cam = motion(log_file, cameras)
            mqtt_publish(cam['cam_name'], cam['motion_type'])


if __name__ == '__main__':
    main()
