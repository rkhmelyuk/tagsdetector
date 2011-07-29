from tagdetector.tag import TagPart

class TagDetector:

    def __init__(self, storage, reader):
        self.storage = storage
        self.reader = reader

    def detect(self, text, limit = 5, minPart = 0.1):
        if not text:
            return []

        tagWords = self.reader.read(text)
        if not tagWords:
            return []

        words = [word.word for word in tagWords]
        tags = self.storage.get_tags_by_words(words)
        tags = [TagPart(tag.get("name"), tag.get("part"))
                for tag in tags if tag.get("part") > minPart]

        tags.sort()
        tags.reverse()

        print [str(tag) for tag in tags]

        if limit < len(tags):
            tags = tags[0:limit]

        return tags