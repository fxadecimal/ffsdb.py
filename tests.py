import unittest
from ffsdb import FFSdb
from pathlib import Path


class TestFFSDB(unittest.TestCase):

    def setUp(self):
        self.ffsdb = FFSdb(tablename="mytable", directory="testdb")
        self.ffsdb["item"] = {"hello": "world"}

    # def tearDown(self) -> None:
    #     self.ffsdb.path

    def test_items(self):
        stem, items = list(self.ffsdb.items())[0]
        self.assertEqual(stem, "item")
        self.assertEqual(items, {"hello": "world"})

    def test_keys(self):
        keys = list(self.ffsdb.keys())
        self.assertEqual(keys, ["item"])

    def test_values(self):
        values = list(self.ffsdb.values())
        self.assertEqual(values, [{"hello": "world"}])

    def test_len(self):
        self.assertEqual(len(self.ffsdb), 1)

    def test_bool(self):
        self.assertEqual(bool(self.ffsdb), True)

    def test_get_key_path(self):
        path = self.ffsdb.get_key_path("item")
        self.assertEqual(str(path), "testdb/mytable/item")

    def test_get_item(self):
        item = self.ffsdb["item"]
        self.assertEqual(item, {"hello": "world"})

    def test_set_item(self):
        self.ffsdb["item"] = {"hello": "world!"}
        self.assertEqual(self.ffsdb["item"], {"hello": "world!"})

    def test_delete(self):
        del self.ffsdb["item"]
        self.assertEqual(len(self.ffsdb), 0)


if __name__ == "__main__":
    unittest.main()
