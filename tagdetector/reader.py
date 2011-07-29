import re
from tagdetector.tag import TagWord

class TextReader:

    STOP_WORDS = ('a', 'the', 'where', 'why', 'by', 'for', 'then', 'than', 'has', 'of', 'and', 'or', 'in', 'out',
                  'would', 'will', 'have', 'is', 'are', 'that', 'this', 'there', 'here', 'when', 'while',
                  'an', 'into', 'other', 'we', 've', 'they', 'he', 'she', 'be', 'to', 'how', 'not',
                  'my', 'your', 'you', 'their', 'his', 'her', 'none', 'so', 'it', 'on', 'have', 'me',
                  'much', 'more', 'less', 'up', 'with', 'without', 'can', 'most', 'long', 'same', 'new', 'old',
                  'should', 'just', 'only', 'not', 'one', 'two', 'unit', 'till', 'if', 'worth', 'either', 'rather',
                  'else', 'something', 'someone', 'sometime', 'somewhere', 'who', 'where', 'what', 'often', 'well',
                  'any', 'all', 'never', 'ever', '')

    def __init__(self):
        pass

    def read(self, text):
        words = self.split(text)
        words = self._filter_only_words(words)
        words = self._filter_stop_words(words)
        words = self._count_words(words)
        
        words.sort(reverse=True)
        
        return words

    def split(self, text):
        pattern = "[\s\.,;:!\[\]()\-_=+*&^%$#@!?`~/']"
        return re.split(pattern, text.lower(), flags=re.MULTILINE)

    def _filter_only_words(self, words):
        return [word for word in words if len(word) > 1]

    def _filter_stop_words(self, words):
        return [word for word in words if word not in TextReader.STOP_WORDS]

    def _count_words(self, words):
        result = []
        duplicates = []
        for word in words:
            if word not in duplicates:
                count = words.count(word)
                result.append(TagWord(word, count))
                duplicates.append(word)

        return result

