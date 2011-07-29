from tagdetector.tag import TagWord
from tagdetector.utils import find

class Storage:

    def __init__(self, mongoConnection):
        self.db = mongoConnection.getDatabase()

    def save_tag_words(self, tag, words):
        words = [{'word': word.word, 'count': word.count, 'part': word.part} for word in words]
        self.db.tagwords.update({'_id': tag}, {'_id': tag, 'words': words}, True)

    def get_tag_words(self, tag):
        cursor = self.db.tagwords.find_one(tag)
        return self._read_tag_words(cursor)

    def get_tags_by_words(self, words):
        cursor = self.db.tagwords.find({'words.word': {"$in": words}})
        result = []
        for tag in cursor:
            part = self._calculate_tag_part(tag, words)
            result.append({
                'name': tag.get("_id"),
                'part': part
            })

        return result

    def _calculate_tag_part(self, tag, words):
        parts = 0
        for tagWord in self._read_tag_words(tag):
            for word in words:
                if tagWord.word == word:
                    parts += tagWord.part
        return parts


    def remove_tag(self, tag):
        self.db.tagwords.remove(tag)

    def _read_tag_words(self, row):
        if row is not None:
            try:
                words = row['words']
                return [self._read_tag_word(word) for word in words]
            except KeyError:
                pass

        return None

    def _read_tag_word(self, word):
        return TagWord(
            word.get('word'),
            word.get('count'),
            word.get('part'))