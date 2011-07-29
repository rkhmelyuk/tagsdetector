
import unittest
from tagdetector.storage.mongo import MongoConnection
from tagdetector.storage.storage import Storage
from tagdetector.tag import TagWord

class StorageTests(unittest.TestCase):

    def setUp(self):
        mongoConn = MongoConnection()
        self.storage = Storage(mongoConn)

    def tearDown(self):
        self.storage = None

    # ------------------------------------------------------------

    def test_save_tag_words(self):
        words = self.add_tag_words()
        self.assert_tag_words_found(words)
        self.remove_tag_with_words()

    def add_tag_words(self):
        words = [
            TagWord("mark", 1),
            TagWord("paul", 2),
            TagWord("john", 2)
        ]
        self.storage.save_tag_words("name", words)
        return words

    def assert_tag_words_found(self, words):
        found_words = self.storage.get_tag_words("name")
        self.assertIsNotNone(found_words, "no words")
        self.assertEqual(len(found_words), len(words))

    def remove_tag_with_words(self):
        self.storage.remove_tag("name")

    # ------------------------------------------------------------

    def test_remove_tag(self):
        self.add_tags()
        self.assert_tags_present()
        self.assert_one_tag_was_removed()
        self.assert_both_tags_were_removed()

    def add_tags(self):
        self.storage.save_tag_words("tag1", [])
        self.storage.save_tag_words("tag2", [])

    def assert_tags_present(self):
        self.assertIsNotNone(self.storage.get_tag_words("tag1"))
        self.assertIsNotNone(self.storage.get_tag_words("tag2"))

    def assert_one_tag_was_removed(self):
        self.storage.remove_tag("tag1")
        self.assertIsNone(self.storage.get_tag_words("tag1"))
        self.assertIsNotNone(self.storage.get_tag_words("tag2"))

    def assert_both_tags_were_removed(self):
        self.storage.remove_tag("tag2")
        self.assertIsNone(self.storage.get_tag_words("tag1"))
        self.assertIsNone(self.storage.get_tag_words("tag2"))

    # ----------------------------------------------------------------

    def test_get_tags_by_words(self):
        self.add_tags_words()
        self.check_found_tags_by_words()

    def add_tags_words(self):
        words1 = (TagWord("mark", 1, 1.0/5), TagWord("paul", 2, 2.0/5), TagWord("john", 2, 2.0/5))
        words2 = (TagWord("john", 1, 1.0/5), TagWord("ira", 2, 2.0/5), TagWord("natali", 2, 2.0/5))

        self.storage.save_tag_words("tag1", words1)
        self.storage.save_tag_words("tag2", words2)

    def check_found_tags_by_words(self):
        self.check_found_tags(('tag1', 'tag2'), (2.0/5, 1.0/5), 'john')
        self.check_found_tags((), (), 'mila')

    def check_found_tags(self, expectedTags, expectedParts, tag):
        tags = self.storage.get_tags_by_words([tag])

        tagsList = [tag.get('name') for tag in tags]
        tagParts = [tag.get('part') for tag in tags]
        
        self.assertEqual(expectedTags, tuple(tagsList), 'wrong list of tags for "john"')
        self.assertEqual(expectedParts, tuple(tagParts), 'wrong list of tags parts for "john"')

if __name__ == "__main__":
    unittest.main()
