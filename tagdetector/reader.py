import re
from tagdetector.tag import TagWord

class TextReader:

    STOP_WORDS = ['a', 'the', 'where', 'why', 'by', 'for', 'then', 'than', 'has', 'of', 'and', 'or', 'in', 'out',
                  'would', 'will', 'have', 'is', 'are', 'that', 'this', 'there', 'here', 'when', 'while',
                  'an', 'into', 'other', 'we', 'i', 've', 'they', 'he', 'she', 'be', 'to', 'how', 'not',
                  'my', 'your', 'you', 'their', 'his', 'her', 'none']

    def __init__(self):
        pass

    def read(self, text):
        words = self.split(text)
        words = self.filter_empty(words)
        words = self.filter_stop_words(words)
        words = self.count_words(words)
        words.sort()
        words.reverse()
        
        return words

    def split(self, text):
        pattern = "[\s\.,;:!\[\]()\-_=+*&^%$#@!?`~/']"
        return re.split(pattern, text.lower(), flags=re.M)

    def filter_empty(self, words):
        return [word for word in words if len(word) != 0]

    def filter_stop_words(self, words):
        return [word for word in words if word not in TextReader.STOP_WORDS]

    def count_words(self, words):
        duplicates = []
        result = []
        for word in words:
            if word not in duplicates:
                count = self.count_word(words, word)
                result.append(TagWord(word, count))
                duplicates.append(word)

        return result

    def count_word(self, words, word):
        count = 0
        for each in words:
            if each == word:
                count += 1

        return count
