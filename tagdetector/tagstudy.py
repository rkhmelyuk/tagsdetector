from tagdetector.tag import TagWord

class TagStudy:

    def __init__(self, storage, reader):
        self.storage = storage
        self.reader = reader

    def learn(self, tags, text):
        if not tags or not text:
            return False

        words = self.reader.read(text)

        for tag in tags:
            tagWords = self.storage.get_tag_words(tag)
            tagWords = self._merge_tag_words(tagWords, words)

            self._calculate_tag_words_part(tagWords)
            self.storage.save_tag_words(tag, tagWords)

    def _merge_tag_words(self, words1, words2):
        words1 = words1 or []
        words2 = words2 or []

        result = []

        self._merge_counts(result, words1, words2)
        self._add_new(result, words2, words1)

        return result

    def _merge_counts(self, result, words1, words2):
        for word1 in words1:
            word = word1.word
            count = word1.count
            for word2 in words2:
                if word2.word == word:
                    count += word2.count

            result.append(TagWord(word, count))

    def _add_new(self, result, words1, words2):
        for word1 in words1:
            word = word1.word
            found = False
            for word2 in words2:
                if word2.word == word:
                    found = True
                    break
            if not found:
                result.append(TagWord(word, word1.count))

    # -------------------------------------------------------------------

    def forget(self, tags, text):
        if not tags or not text:
            return False

        words = self.reader.read(text)

        for tag in tags:
            tagWords = self.storage.get_tag_words(tag)
            tagWords = self._revert_tag_words(tagWords, words)

            self._calculate_tag_words_part(tagWords)
            self.storage.save_tag_words(tag, tagWords)

    def _revert_tag_words(self, words1, words2):
        words1 = words1 or []
        words2 = words2 or []

        result = []

        self._revert_counts(result, words1, words2)

        return result

    def _revert_counts(self, result, words1, words2):
        for word1 in words1:
            word = word1.word
            count = word1.count
            for word2 in words2:
                if word2.word == word:
                    count -= word2.count

            if count > 0:
                result.append(TagWord(word, count))
                

    def _calculate_tag_words_part(self, words):
        totalCount = 0
        for word in words:
            totalCount += word.count

        if totalCount:
            for word in words:
                word.part = float(word.count) / totalCount
