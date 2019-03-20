import traceback
import logging
import datetime

from time import time
from nltools import misc
from nltools.pulserecorder import PulseRecorder
from nltools.vad import VAD, BUFFER_DURATION
from nltools.asr import ASR, ASR_ENGINE_NNET3
from optparse import OptionParser

from lib.command import LightDevice, SpeechCommand, DetectionSequence, Action
from lib.speech_command_handler import SpeechCommandHandler

PROC_TITLE                       = 'kaldi_live_demo'

WAKEUP_WORD                      = 'Computer'.lower()

DEFAULT_VOLUME                   = 150
DEFAULT_AGGRESSIVENESS           = 2

# DEFAULT_MODEL_DIR                = '/opt/kaldi/model/kaldi-generic-de-tdnn_250'
DEFAULT_MODEL_DIR                = '/opt/kaldi/model/kaldi-generic-en-tdnn_250'
DEFAULT_ACOUSTIC_SCALE           = 1.0
DEFAULT_BEAM                     = 7.0
DEFAULT_FRAME_SUBSAMPLING_FACTOR = 3

STREAM_ID                        = 'mic'

misc.init_app(PROC_TITLE)

logging.basicConfig(level=logging.INFO)

source         = 'USB Audio Device Analog'
volume         = DEFAULT_VOLUME
aggressiveness = DEFAULT_AGGRESSIVENESS
model_dir      = DEFAULT_MODEL_DIR

rec = PulseRecorder (source_name=source, volume=volume)

vad = VAD(aggressiveness=aggressiveness)

print("Loading model from %s ..." % model_dir)

asr = ASR(engine = ASR_ENGINE_NNET3, model_dir = model_dir,
          kaldi_beam = DEFAULT_BEAM, kaldi_acoustic_scale = DEFAULT_ACOUSTIC_SCALE,
          kaldi_frame_subsampling_factor = DEFAULT_FRAME_SUBSAMPLING_FACTOR)

rec.start_recording()


print("ava: we are live")

def find_cmd_start_index(utterance):
    index = utterance.find(WAKEUP_WORD)

    if index == -1:
        return index

    return index + len(WAKEUP_WORD)

def init_speech_command_handler():
    turn_light_on = DetectionSequence(sequence=['turn', 'light', 'on'])
    turn_on_light = DetectionSequence(sequence=['turn', 'on', 'light'])
    turn_on_lights = DetectionSequence(sequence=['turn', 'on', 'lights'])

    turn_light_off = DetectionSequence(sequence=['turn', 'light', 'off'])
    turn_off_light = DetectionSequence(sequence=['turn', 'off', 'light'])
    turn_off_lights = DetectionSequence(sequence=['turn', 'off', 'lights'])

    on_detection_sequences = [turn_light_on, turn_on_light, turn_on_lights]

    off_detection_sequences = [turn_light_off, turn_off_light, turn_off_lights]

    device = LightDevice()

    set_light_on = Action(lambda l: l.turn_on())
    set_light_off = Action(lambda l: l.turn_off())

    on_cmd = SpeechCommand([device], set_light_on, on_detection_sequences)
    off_cmd = SpeechCommand([device], set_light_off, off_detection_sequences)

    handler = SpeechCommandHandler()
    handler.add_command(on_cmd)
    handler.add_command(off_cmd)

    return handler

cmd_handler = init_speech_command_handler()

utterance_consumed = False

while True:
    samples = rec.get_samples()

    audio, finalize = vad.process_audio(samples)

    if not audio:
        continue

    logging.debug ('decoding audio len=%d finalize=%s audio=%s' % (len(audio), repr(finalize), audio[0].__class__))

    user_utt, confidence = asr.decode(audio, finalize, stream_id=STREAM_ID)

    print "\r%s                     " % user_utt,

    # Look for wakeup word and command before the utterance has been finalized
    cmd_index = find_cmd_start_index(user_utt)
    if cmd_index != -1:
        utterance_consumed = utterance_consumed or cmd_handler.process(user_utt, cmd_index)

    if finalize:
        utterance_consumed = False
        print
