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

#
# cmdline, logging
#
"""
parser = OptionParser("usage: %prog [options]")

parser.add_option ("-a", "--aggressiveness", dest="aggressiveness", type = "int", default=DEFAULT_AGGRESSIVENESS,
                   help="VAD aggressiveness, default: %d" % DEFAULT_AGGRESSIVENESS)

parser.add_option ("-m", "--model-dir", dest="model_dir", type = "string", default=DEFAULT_MODEL_DIR,
                   help="kaldi model directory, default: %s" % DEFAULT_MODEL_DIR)

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")

parser.add_option ("-s", "--source", dest="source", type = "string", default=None,
                   help="pulseaudio source, default: auto-detect mic")

parser.add_option ("-V", "--volume", dest="volume", type = "int", default=DEFAULT_VOLUME,
                   help="broker port, default: %d" % DEFAULT_VOLUME)
"""

model_dir = DEFAULT_MODEL_DIR
aggressiveness = DEFAULT_AGGRESSIVENESS


(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

source         = options.source
volume         = options.volume
aggressiveness = options.aggressiveness
model_dir      = options.model_dir

rec = PulseRecorder (source_name=source, volume=volume)

vad = VAD(aggressiveness=aggressiveness)

print "Loading model from %s ..." % model_dir

asr = ASR(engine = ASR_ENGINE_NNET3, model_dir = model_dir,
          kaldi_beam = DEFAULT_BEAM, kaldi_acoustic_scale = DEFAULT_ACOUSTIC_SCALE,
          kaldi_frame_subsampling_factor = DEFAULT_FRAME_SUBSAMPLING_FACTOR)

rec.start_recording()

print "Please speak."

def main():
    while True:

        samples = rec.get_samples()

        audio, finalize = vad.process_audio(samples)

        if not audio:
            continue

        logging.debug ('decoding audio len=%d finalize=%s audio=%s' % (len(audio), repr(finalize), audio[0].__class__))

        user_utt, confidence = asr.decode(audio, finalize, stream_id=STREAM_ID)

        print "\r%s                     " % user_utt,

        if finalize:
            print

if __name__ == '__main__':
    main()
