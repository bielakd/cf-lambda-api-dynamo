from .builder import Container


class Processor:
    def __init__(self, container: Container):
        self.container = container

    def run(self, message_key):
        self.container.initiate()
        message = self.container.extract(message_key=message_key)
        return message
