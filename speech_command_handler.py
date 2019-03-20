
class SpeechCommandHandler:

    def __init__(self):
        self.commands = []

    def add_command(cmd):
        self.commands.append(cmd)

    def process(speech, start_index=0):
        text = speech[start_index:]
        for c in commands:
            if c.matches(text):
                c.execute()
