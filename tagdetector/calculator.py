from tagdetector.tag import TagWord

class TagCalculator:

    def __init__(self, storage, reader):
        self.storage = storage
        self.reader = reader

    def calculate(self, tags, text):
        if not tags:
            return False

        words = self.reader.read(text)

        for tag in tags:
            tagWords = self.storage.get_tag_words(tag)
            tagWords = self.merge_tag_words(tagWords, words)

            self.calculate_tag_words_part(tagWords)
            self.storage.save_tag_words(tag, tagWords)

    def merge_tag_words(self, words1, words2):
        words1 = words1 or []
        words2 = words2 or []

        result = []

        self.merge_counts(result, words1, words2)
        self.add_new(result, words2, words1)

        return result

    def merge_counts(self, result, words1, words2):
        for word1 in words1:
            word = word1.word
            count = word1.count
            for word2 in words2:
                if word2.word == word:
                    count += word2.count

            result.append(TagWord(word, count))

    def add_new(self, result, words1, words2):
        for word1 in words1:
            word = word1.word
            found = False
            for word2 in words2:
                if word2.word == word:
                    found = True
                    break
            if not found:
                result.append(TagWord(word, word1.count))

    def calculate_tag_words_part(self, words):
        totalCount = 0
        for word in words:
            if word.count > 1:
                totalCount += word.count

        for word in words:
            if word.count > 1:
                word.part = float(word.count) / totalCount
