#!/usr/bin/env python3

"""Module to search into base 64 encoded text"""

import dataclasses
import re
import typing
import sys


def encode_to_b64(cur_bytes: str):
    """Encode word to base64"""
    bits = "".join([f"{byte:08b}" for byte in cur_bytes])
    assert len(bits) % 6 == 0
    chunks_6b = re.findall("......", bits)
    return SearchBase64.bits_to_word(chunks_6b)


@dataclasses.dataclass(frozen=True)
class Base64Word:
    """Class to manage base64 words"""

    word: str
    search_word: str = ""
    prefix_skip: int = 0
    suffix_skip: int = 0

    def __post_init__(self):
        assert self.prefix_skip >= 0
        assert self.suffix_skip >= 0
        object.__setattr__(
            self,
            "search_word",
            self.word[
                self.prefix_skip: -self.suffix_skip
                if self.suffix_skip > 0
                else len(self.word)
            ],
        )

    def __repr__(self):
        return f"Base64Word({self.word},{self.search_word},{self.prefix_skip},{self.suffix_skip})"


class SearchBase64:
    """Class to search text into base64 encoded text"""

    dct = {
        f"{idx:06b}": letter
        for idx, letter in enumerate(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        )
    }

    def __init__(self, word: str, encoding="utf-8"):
        self.word = word
        self.bytes = bytes(word, encoding=encoding)
        self.encoding = encoding
        self.b64_words = set()

    def _gen_all_cases(self, cur_bytes, prefix_skip):
        diff = len(cur_bytes) % 3
        if diff == 0:
            b64_word = Base64Word(encode_to_b64(
                cur_bytes), prefix_skip=prefix_skip)
            self.b64_words.add(b64_word)
            return

        suffixes = (
            [i << 6 for i in range(4)] if diff == 2 else [
                i << 12 for i in range(16)]
        )
        for suffix in suffixes:
            new_bytes = cur_bytes + suffix.to_bytes(3 - diff, "big")
            b64_word = Base64Word(
                encode_to_b64(new_bytes),
                prefix_skip=prefix_skip,
                suffix_skip=3 - diff,
            )
            self.b64_words.add(b64_word)

    def gen_b64_words(self):
        """Generate all possible base64 versions of provided clear text"""
        self.b64_words.clear()
        self._gen_all_cases(self.bytes, prefix_skip=0)
        for prefix in range(4):
            new_bytes = prefix.to_bytes(1, "big") + self.bytes
            self._gen_all_cases(new_bytes, prefix_skip=1)
        for prefix in range(16):
            new_bytes = prefix.to_bytes(2, "big") + self.bytes
            self._gen_all_cases(new_bytes, prefix_skip=2)

    def find_in_file(self, filename) -> typing.Tuple[bool, typing.List[bytes]]:
        """Find specified base64 text into provided filename"""
        self.gen_b64_words()
        content = b""
        if filename == "-":
            for line in sys.stdin:
                content += bytes(line, encoding=self.encoding)
        else:
            with open(filename, "rb") as file:
                for line in file.readlines():
                    content += line

        lst = set()
        found = False
        b64_words_to_test = sorted((w.search_word for w in self.b64_words))
        for b64_word in b64_words_to_test:
            if bytes(b64_word, encoding=self.encoding) in content:
                if found is False:
                    print(f"{filename}: found {self.word} =>", end="")
                print(f" {b64_word}", end="")
                lst.add(b64_word)
                found = True
        if found:
            print()

        return found, lst

    @classmethod
    def bits_to_word(cls, word_bytes: typing.List[str]):
        """Convert 6b chunks to word"""
        return "".join([cls.dct.get(idx, "") for idx in word_bytes])

    @classmethod
    def usage(cls):
        """Display usage of current module"""
        print(f"{sys.argv[0]} <clear word to look for> <file to look into>")


def main():
    """Main function"""
    if len(sys.argv) > 1:
        gb64 = SearchBase64(sys.argv[1])
        files = sys.argv[2:] if len(sys.argv) > 2 else ["-"]
        ret = False
        for file in files:
            res, _ = gb64.find_in_file(file)
            if res:
                ret = True
        sys.exit(0 if ret else 1)
    else:
        SearchBase64.usage()


if __name__ == "__main__":
    main()
