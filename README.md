# Ava

Inspired by [Ex Machina](https://en.wikipedia.org/wiki/Ex_Machina_(film)), Ava is an Automated Speech Recognition (ASR) system used to control your home devices through voice (like Amazon Alexa).

The system is designed to be light on resources and can be executed on a Raspberry Pi 3.

Devices can be enabled or disabled by using RF power sockets. These sockets are controlled by an Arduino that in turn receives commands from the ASR running on the Raspberry Pi.

## Requirements

- Python 2.7
- [zamia-speech](https://github.com/gooofy/zamia-speech)

## Execution

```
python runner.py
# nohup python runner.py & if the task should permanently run in the background
```

This will listen to any speech commands that start with the `WAKEUP_WORD` that is specified in `runner.py`. Per default this will be `computer`.

## Add a custom command

A command consists of the device that should be controlled, an action that is executed on the device and a number of detection sequences to detect whether a given speech text should trigger the command.

```
# This will create a command to turn on a light source.

# The light source to active or deactivate
light = LightDevice(id=1)

# Any speech sequence containing 'turn', 'on', 'kitchen', 'light' in this order will trigger the command.
detection_seq = ['turn', 'on', 'kitchen', 'light']

# The action is to turn on the light.
action = Action(lambda l: l.turn_on())

# Constructs the command
cmd = SpeechCommand(devices=[light], action=action, detection_sequences=[detection_seq])

# Add the command to the SpeechHandler in runner.py
```
