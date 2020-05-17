class Container:
    def __init__(self, initiator, extractor):
        self.initiator = initiator
        self.extractor = extractor

    def initiate(self):
        self.initiator.insert()

    def extract(self, message_key: str) -> dict:
        return self.extractor.extract(message_key)
