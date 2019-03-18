
class DetectionSequence:
    def __init__(self, sequence):
        """ Constructs a new DetectionSequence

	The given sequence is a list of keywords that should be matched in the same order
	by any given text.
	"""
        self.sequence = [s.lower() for s in sequence]

    def _clean_word(self, word):
        """ Removes any punctuation from the given word. """
        chars = []
        for c in word:
            if c.isalpha():
                chars.append(c)

        return ''.join(chars)

    def matches(self, text):
        """ Returns whether this DetecionSequence matches the given text.

	The matching process is agnostic of text capitalization.

	Example:

	sequence = ['on', 'light']
	text = 'Turn on the light.'

	This will produce a match since the words 'on' and 'light' occur in the same order
	in the given text. The sequence tokens do not need to be consecutive though.
	"""
        words = [self._clean_word(word.lower()) for word in text.strip().split()]

        seq_ptr = 0
        words_ptr = 0

        print(self.sequence, words)

        while seq_ptr < len(self.sequence) and words_ptr < len(words):
            if self.sequence[seq_ptr] == words[words_ptr]:
                seq_ptr += 1
            words_ptr += 1
            
        return seq_ptr == len(self.sequence)


class SpeechCommand:
    """ Speech command. """

    def __init__(self, devices, action, detection_sequences):
        self.devices = devices
        self.action = action
        self.detection_sequences = detection_sequences

    def matches(self, text):
        """ Returns whether the given speech text should activate this command. """
        matches = False
        for seq in self.detection_sequences:
            if seq.matches(text):
                matches = True
                break
            
        return matches

    def execute(self):
        for d in self.devices:
            self.action(d)


class Device:
    """ A device that can be controlled through commands. """

    def __init__(self):
        self.state = {}


class Action:
    """ Operations that are executed on given devices. """

    def execute(self, device):
        pass


class LightDevice extends Device:
    """ spaß """

    def turn_on(id):
        device_id = 0b0000001111
        command = 0b01
        paket =  device_id << 2 + command
        send_data(paket)

    def turn_off(id):
        device_id = 0b0000001111
        command = 0b10
        paket =  device_id << 2 + command
        send_data(paket)