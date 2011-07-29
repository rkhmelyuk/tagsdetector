
class TagDetector:

    def __init__(self, storage, reader):
        self.storage = storage
        self.reader = reader

    def detect(self, text, limit = 5):
        if not text:
            return []

        tagWords = self.reader.read(text)
        if not tagWords:
            return []

        words = [word.word for word in tagWords]
        tags = self.storage.get_tags_by_words(words)
        tags.sort()

        if limit < len(tags):
            return tags[0:limit]
        
        return tags