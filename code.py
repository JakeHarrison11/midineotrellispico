import time
import random
import usb_midi
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend
from board import GP1, GP0
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis

# create the i2c object for the trellis
i2c_bus = busio.I2C(GP1, GP0)

# create the trellis
trellis = NeoTrellis(i2c_bus)

# create midi usb interface 
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# mappings for button --> note on trellis
notes = [60, 61, 62, 63, 56, 57, 58, 59, 52, 53, 54, 55, 48, 49, 50, 51]

OFF = (0,0,0)

# this will be called when button events are received
def blink(event):
    # turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        print(event.number)
        # send a MIDI note on command
        midi.send(NoteOn(notes[event.number], 120))
        trellis.pixels[event.number] = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
    # turn the LED off when a rising edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        trellis.pixels[event.number] = OFF
        # send a MIDI note off command
        midi.send(NoteOff(notes[event.number], 120))


for i in range(16):
    # activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    # activate falling edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    # set all keys to trigger the blink callback
    trellis.callbacks[i] = blink

    # cycle the LEDs on startup
    trellis.pixels[i] = (random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255))
    time.sleep(0.05)

for i in range(16):
    trellis.pixels[i] = OFF
    time.sleep(0.05)

while True:
    # call the sync function call any triggered callbacks
    trellis.sync()
    # the trellis can only be read every 17 millisecons or so
    time.sleep(0.02)
