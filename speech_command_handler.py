
class SpeechCommandHandler:

    def __init__(self):
        self.commands = []

    def add_command(self, cmd):
        self.commands.append(cmd)

    def process(self, speech, start_index=0):
        text = speech[start_index:]
        for c in self.commands:
            if c.matches(text):
                c.execute()
