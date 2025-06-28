import unittest

from Kuznyechik import Kuznyechik


class TestKuznyechik(unittest.TestCase):
    def test_small_file(self):
        kuz = Kuznyechik()
        string = "hello world"
        hashed = kuz.hash(string)
        self.assertEqual(kuz.from_hash(hashed), string)

    def test_big_file(self):
        kuz = Kuznyechik()
        string = "hello world" * 20_000
        hashed = kuz.hash(string)
        self.assertEqual(kuz.from_hash(hashed), string)

    def test_empty_string(self):
        kuz = Kuznyechik()
        string = ""
        hashed = kuz.hash(string)
        self.assertEqual(kuz.from_hash(hashed), string)

    def test_asian_string(self):
        kuz = Kuznyechik()
        string = "このテキストはハッシュ化する必要があります"
        hashed = kuz.hash(string)
        self.assertEqual(kuz.from_hash(hashed), string)

    def test_russian_string(self):
        kuz = Kuznyechik()
        string = "Этот текст надо захешировать"
        hashed = kuz.hash(string)
        self.assertEqual(kuz.from_hash(hashed), string)

    def test_simple_string(self):
        kuz = Kuznyechik()
        string = "This text need to be hashed"
        hashed = kuz.hash(string)
        self.assertEqual(kuz.from_hash(hashed), string)

    def test_dif_lang_string(self):
        kuz = Kuznyechik()
        string = "Этот текст надо захешировать このテキストはハッシュ化する必要があります This text need to be hashed"
        hashed = kuz.hash(string)
        self.assertEqual(kuz.from_hash(hashed), string)

    def test_emoji_string(self):
        kuz = Kuznyechik()
        string = "🤣😒😒😒😒😒😒😒😒😊🎮👨‍💻🐍❤️📤😍📩📩📩😒🤣😂"
        hashed = kuz.hash(string)
        self.assertEqual(kuz.from_hash(hashed), string)
