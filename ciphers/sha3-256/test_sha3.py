import unittest
from main import Sha3
from hashlib import sha3_256


def to_binary(string):
    if type(string) != str:
        string = str(string)

    with open("input.txt", "w", encoding='utf-8') as file:
        file.write(string)
        file.close()

    with open("input.txt", "rb") as file:
        content = file.read()
        return content


class TestSha3(unittest.TestCase):
    def test_empty_string(self):
        string = ""
        to_hash = to_binary(string)
        orig = sha3_256(to_hash).hexdigest()
        my_ver = Sha3(256).hash(to_hash).hex()
        self.assertEqual(orig, my_ver)

    def test_simple_string(self):
        string = "This text need to be hashed"
        to_hash = to_binary(string)
        orig = sha3_256(to_hash).hexdigest()
        my_ver = Sha3(256).hash(to_hash).hex()
        self.assertEqual(orig, my_ver)

    def test_asian_string(self):
        string = "このテキストはハッシュ化する必要があります"
        to_hash = to_binary(string)
        orig = sha3_256(to_hash).hexdigest()
        my_ver = Sha3(256).hash(to_hash).hex()
        self.assertEqual(orig, my_ver)

    def test_russian_string(self):
        string = "Этот текст надо захешировать"
        to_hash = to_binary(string)
        orig = sha3_256(to_hash).hexdigest()
        my_ver = Sha3(256).hash(to_hash).hex()
        self.assertEqual(orig, my_ver)

    def test_dif_lang_string(self):
        string = "Этот текст надо захешировать このテキストはハッシュ化する必要があります This text need to be hashed"
        to_hash = to_binary(string)
        orig = sha3_256(to_hash).hexdigest()
        my_ver = Sha3(256).hash(to_hash).hex()
        self.assertEqual(orig, my_ver)

    def test_emoji_string(self):
        string = "🤣😒😒😒😒😒😒😒😒😊🎮👨‍💻🐍❤️📤😍📩📩📩😒🤣😂"
        to_hash = to_binary(string)
        orig = sha3_256(to_hash).hexdigest()
        my_ver = Sha3(256).hash(to_hash).hex()
        self.assertEqual(orig, my_ver)

    def test_medium_size_string(self):
        string = "qwerty_size" * 1000
        to_hash = to_binary(string)
        orig = sha3_256(to_hash).hexdigest()
        my_ver = Sha3(256).hash(to_hash).hex()
        self.assertEqual(orig, my_ver)

    def test_long_string(self):
        string = "qwerty_size" * 50_000
        to_hash = to_binary(string)
        orig = sha3_256(to_hash).hexdigest()
        my_ver = Sha3(256).hash(to_hash).hex()
        self.assertEqual(orig, my_ver)

    def test_mb_string(self):
        string = "a" * 1_048_576
        to_hash = to_binary(string)
        orig = sha3_256(to_hash).hexdigest()
        my_ver = Sha3(256).hash(to_hash).hex()
        self.assertEqual(orig, my_ver)

    def test_more_mb_string(self):
        string = "ab" * 1_048_576
        to_hash = to_binary(string)
        orig = sha3_256(to_hash).hexdigest()
        my_ver = Sha3(256).hash(to_hash).hex()
        self.assertEqual(orig, my_ver)

    def test_numbers(self):
        num = 1234567890
        to_hash = to_binary(num)
        orig = sha3_256(to_hash).hexdigest()
        my_ver = Sha3(256).hash(to_hash).hex()
        self.assertEqual(orig, my_ver)
