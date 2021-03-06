from unittest import TestCase
from mockredis.sortedset import SortedSet


class TestSortedSet(TestCase):

    def setUp(self):
        self.zset = SortedSet()

    def test_initially_empty(self):
        """
        Sorted set is created empty.
        """
        self.assertEqual(0, len(self.zset))

    def test_insert(self):
        """
        Insertion maintains order and uniqueness.
        """
        # insert two values
        self.assertTrue(self.zset.insert("one", 1.0))
        self.assertTrue(self.zset.insert("two", 2.0))

        # validate insertion
        self.assertEquals(2, len(self.zset))
        self.assertTrue("one" in self.zset)
        self.assertTrue("two" in self.zset)
        self.assertFalse(1.0 in self.zset)
        self.assertFalse(2.0 in self.zset)
        self.assertEquals(1.0, self.zset["one"])
        self.assertEquals(2.0, self.zset["two"])
        with self.assertRaises(KeyError):
            self.zset[1.0]
        with self.assertRaises(KeyError):
            self.zset[2.0]
        self.assertEquals(0, self.zset.rank("one"))
        self.assertEquals(1, self.zset.rank("two"))
        self.assertEquals(None, self.zset.rank(1.0))
        self.assertEquals(None, self.zset.rank(2.0))

        # re-insert a value
        self.assertFalse(self.zset.insert("one", 3.0))

        # validate the update
        self.assertEquals(2, len(self.zset))
        self.assertEquals(3.0, self.zset.score("one"))
        self.assertEquals(0, self.zset.rank("two"))
        self.assertEquals(1, self.zset.rank("one"))

    def test_remove(self):
        """
        Removal maintains order.
        """
        # insert a few elements
        self.zset["one"] = 1.0
        self.zset["uno"] = 1.0
        self.zset["three"] = 3.0
        self.zset["two"] = 2.0

        # cannot remove a member that is not present
        self.assertEquals(False, self.zset.remove("four"))

        # removing an existing entry works
        self.assertEquals(True, self.zset.remove("two"))
        self.assertEquals(3, len(self.zset))
        self.assertEquals(0, self.zset.rank("one"))
        self.assertEquals(1, self.zset.rank("uno"))
        self.assertEquals(None, self.zset.rank("two"))
        self.assertEquals(2, self.zset.rank("three"))

        # delete also works
        del self.zset["uno"]
        self.assertEquals(2, len(self.zset))
        self.assertEquals(0, self.zset.rank("one"))
        self.assertEquals(None, self.zset.rank("uno"))
        self.assertEquals(None, self.zset.rank("two"))
        self.assertEquals(1, self.zset.rank("three"))

    def test_scoremap(self):
        self.zset["one"] = 1.0
        self.zset["uno"] = 1.0
        self.zset["two"] = 2.0
        self.zset["three"] = 3.0
        self.assertEquals([(1.0, "one"), (1.0, "uno")], self.zset.scorerange(1.0, 1.1))
        self.assertEquals([(1.0, "one"), (1.0, "uno"), (2.0, "two")],
                          self.zset.scorerange(1.0, 2.0))
