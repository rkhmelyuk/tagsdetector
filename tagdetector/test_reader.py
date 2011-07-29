import unittest

from tagdetector.reader import TextReader

class TextReaderTests(unittest.TestCase):

    def setUp(self):
        self.reader = TextReader()

    def tearDown(self):
        self.reader = None

    def test_read_empty(self):
        text = ""
        words = self.reader.read(text)
        self.assertEquals(len(words), 0)

    def test_read_punctuation(self):
        text = "Hello, Ruslan!shard;orthopedics:consist-later"

        words = self.reader.read(text)

        onlyWords = [word.word for word in words]

        self.assertEquals(len(words), 6)
        self.check_contains_words(onlyWords)

    def check_contains_words(self, onlyWords):
        self.assertIn("hello", onlyWords)
        self.assertIn("ruslan", onlyWords)
        self.assertIn("shard", onlyWords)
        self.assertIn("consist", onlyWords)
        self.assertIn("later", onlyWords)
        self.assertIn("orthopedics", onlyWords)

    # -----------------------------------------------------------------

    def test_read_duplicates(self):
        text = "hello Hello HELLO hElLO master"

        words = self.reader.read(text)
        onlyWords = [word.word for word in words]

        self.check_count_duplicates(onlyWords, words)

    def check_count_duplicates(self, onlyWords, words):
        self.assert_word_count(words, "hello", 4)
        self.assertEquals(len(words), 2)
        self.assertIn("hello", onlyWords)
        self.assertIn("master", onlyWords)

    def assert_word_count(self, words, word, count):
        for each in words:
            if each.word == word:
                self.assertEqual(each.count, count)
                break
        else:
            self.fail("Word is not found")


if __name__ == "__main__":
    unittest.main()