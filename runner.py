import traceback
import logging
import datetime

from time import time
from nltools import misc
from nltools.pulserecorder import PulseRecorder
from nltools.vad import VAD, BUFFER_DURATION
from nltools.asr import ASR, ASR_ENGINE_NNET3
from optparse import OptionParser

PROC_TITLE                       = 'kaldi_live_demo'

DEFAULT_VOLUME                   = 150
DEFAULT_AGGRESSIVENESS           = 2

# DEFAULT_MODEL_DIR                = '/opt/kaldi/model/kaldi-generic-de-tdnn_250'
DEFAULT_MODEL_DIR                = '/opt/kaldi/model/kaldi-generic-en-tdnn_250'
DEFAULT_ACOUSTIC_SCALE           = 1.0
DEFAULT_BEAM                     = 7.0
DEFAULT_FRAME_SUBSAMPLING_FACTOR = 3

STREAM_ID                        = 'mic'

#
# init
#

misc.init_app(PROC_TITLE)

logging.basicConfig(level=logging.INFO)

source         = 'USB PnP Sound'
volume         = DEFAULT_VOLUME
aggressiveness = DEFAULT_AGGRESSIVENESS
model_dir      = DEFAULT_MODEL_DIR

rec = PulseRecorder (source_name=source, volume=volume)

vad = VAD(aggressiveness=aggressiveness)

print "Loading model from %s ..." % model_dir

asr = ASR(engine = ASR_ENGINE_NNET3, model_dir = model_dir,
          kaldi_beam = DEFAULT_BEAM, kaldi_acoustic_scale = DEFAULT_ACOUSTIC_SCALE,
          kaldi_frame_subsampling_factor = DEFAULT_FRAME_SUBSAMPLING_FACTOR)

rec.start_recording()

print "Please speak."


def handle(user_utt):


def has_trigger_word(string):
    words = user_utt.split()
    len_words = len(words)

    for k in range (0, len_words):
        if words[k] == "computer":
            print("NICE")
            return True

    return False


def main():
    light_device = Device()

    turn_light_on = DetectionSequence(sequence=['turn', 'light', 'on'])
    turn_on_light = DetectionSequence(sequence=['turn', 'on', 'light'])

    detection_sequences = [turn_light_on, turn_on_light]

    commands = []
    light_on_cmd = SpeechCommand()

    while True:

        samples = rec.get_samples()

        audio, finalize = vad.process_audio(samples)

        if not audio:
            continue

        logging.debug ('decoding audio len=%d finalize=%s audio=%s' % (len(audio), repr(finalize), audio[0].__class__))

        user_utt, confidence = asr.decode(audio, finalize, stream_id=STREAM_ID)

        print "\r%s                     " % user_utt,

        if finalize:
            if(has_trigger_word(user_utt)):
                handle(user_utt)
            print 'NEW:', user_utt, confidence

if __name__ == '__main__':
    main()
