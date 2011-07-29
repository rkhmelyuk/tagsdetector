import unittest
from tagdetector.calculator import TagCalculator
from tagdetector.detector import TagDetector
from tagdetector.reader import TextReader
from tagdetector.storage.mongo import MongoConnection
from tagdetector.storage.storage import Storage

class TagDetectorTests(unittest.TestCase):

    def setUp(self):
        mongoConn = MongoConnection()
        self.storage = Storage(mongoConn)
        reader = TextReader()

        self.calculator = TagCalculator(self.storage, reader)
        self.detector = TagDetector(self.storage, reader)

    def tearDown(self):
        self.detector = None

    def test_no_text(self):
        tags = self.detector.detect("")
        self.assertEqual([], tags, 'Should be empty')

    def test_simple_text_single_tag(self):
        try:
            tags = ['tag1']
            text = 'Hello my World'
            self.calculator.calculate(tags, text)

            foundTags = self.detector.detect("Hello wonderful world!")
            foundTagsNames = [tag.get('name') for tag in foundTags]

            self.assertEqual(tags, foundTagsNames)
        finally:
            self.storage.remove_tag("tag1")

    def test_simple_text_two_tags(self):
        try:
            tags = ['tag1', 'tag2']
            text = 'Hello my World'
            self.calculator.calculate(tags, text)

            foundTags = self.detector.detect("Hello wonderful world!")
            foundTagsNames = [tag.get('name') for tag in foundTags]

            self.assertEqual(tags, foundTagsNames)
        finally:
            self.storage.remove_tag("tag1")
            self.storage.remove_tag("tag2")

if __name__ == "__main__":
    unittest.main()