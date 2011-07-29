import unittest
from tagdetector.calculator import TagCalculator
from tagdetector.reader import TextReader
from tagdetector.storage.mongo import MongoConnection
from tagdetector.storage.storage import Storage

class TagCalculatorTests(unittest.TestCase):
    def setUp(self):
        mongoConn = MongoConnection()
        self.storage = Storage(mongoConn)
        reader = TextReader()
        self.calculator = TagCalculator(self.storage, reader)

    def tearDown(self):
        self.calculator = None

    def test_new_tag(self):
        tags = ['tag1']
        text = 'Hello World!'
        self.calculator.calculate(tags, text)

        self.check_tag_words('tag1', {'hello': 1, 'world': 1})

    def test_few_tags(self):
        tags = ['tag1', 'tag2']
        text = 'Hello World!'
        self.calculator.calculate(tags, text)

        self.check_tag_words('tag1', {'hello': 1, 'world': 1})
        self.check_tag_words('tag2', {'hello': 1, 'world': 1})

    def test_merge_tags(self):
        tags = ['tag1']
        text = 'Hello World!'
        self.calculator.calculate(tags, text)

        self.check_tag_words('tag1', {'hello': 1, 'world': 1}, remove=False)

        text = 'Hello Ruslan!'
        self.calculator.calculate(tags, text)
        self.check_tag_words('tag1', {'hello': 2, 'world': 1, 'ruslan': 1})

    def test_tags_words_parts(self):
        tags = ['tag1']
        text = 'Hello World! World is nice, so it is a pleasure to say hello to the world'
        self.calculator.calculate(tags, text)

        words = self.storage.get_tag_words('tag1')

        try:
            foundHello = False
            foundWorld = False
            foundNice = False
            for word in words:
                if word.word == 'hello':
                    self.assertEqual(2, word.count)
                    self.assertEqual(float(2.0/5), word.part)
                    foundHello = True
                if word.word == 'world':
                    self.assertEqual(3, word.count)
                    self.assertEqual(3.0/5, word.part)
                    foundWorld = True
                if word.word == 'nice':
                    self.assertEqual(1, word.count)
                    self.assertEqual(0.0, word.part)
                    foundNice = True

            self.assertTrue(foundHello, 'Hello is not found')
            self.assertTrue(foundWorld, 'World is not found')
            self.assertTrue(foundNice, 'Nice is not found')
        finally:
            self.storage.remove_tag('tag1')


    def check_tag_words(self, tag, checkWords, remove = True):
        words = self.storage.get_tag_words(tag)
        for key, value in checkWords.items():
            self.assertWordInWithCount(words, key, value)

        if remove: self.storage.remove_tag(tag)

    def assertWordInWithCount(self, words, word, count):
        for each in words:
            if each.word == word:
                self.assertEqual(count, each.count, "Wrong count")
                return
        self.fail("Word is not found")



if __name__ == "__main__":
    unittest.main()
