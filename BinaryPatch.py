import sys
import re
import binascii

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2019 Miuipro.info'


class BinaryPatch(object):
    def __init__(self, file=None, search=None, replace=None, symbol='0', max_matches=None):
        self.target = file
        self.search_pattern = self.__text_to_pattern(search)
        if len(replace) < len(search):
            self.replace_pattern = self.__text_to_pattern(replace, symbol=symbol, len=len(search) - len(replace))
        else:
            self.replace_pattern = self.__text_to_pattern(replace)
        bsize = len(b"".join(self.search_pattern))
        self.bufsize = max(bsize, 2 ** 23)   # размер буфера чтения файла
        self.max_matches = max_matches
        self.start = 0
        self.end = 0
        self.verbose = False
        self.find_offset = []
        self.fh = None
        self.__open()

    def __open(self):
        try:
            self.fh = open(self.target, 'r+b')
        except IOError:
            e = sys.exc_info()[1]

    def __hex_to_pattern(self, hex):
        ret = []
        pattern = hex
        if hex[:2] == "0x":
            pattern = hex[2:]
        try:
            ret = [p for p in pattern.split("??")]
            try:  # Python 3.
                return [bytes.fromhex(p) for p in ret]
            except AttributeError:
                return [p.decode("hex") for p in ret]
        except(TypeError, ValueError):
            e = sys.exc_info()[1]

    def __text_to_pattern(self, text, symbol=None, len=None):
        if len:
            tmp = [hex(ord(p))[2:] for p in text]
            for i in range(len):
                tmp += symbol
            return self.__hex_to_pattern(''.join(tmp))
        try:
            return [binascii.unhexlify(t) for t in text.split("?")]
        except TypeError:
            return [t for t in text.split("?")]

    def __search_loop(self, start, end, bufsize, pattern, max_matches, verbose, fh_name, fh_read, fh_seek):
        len_pattern = len(b"?".join(pattern))
        read_size = bufsize - len_pattern
        pattern = b".".join([p for p in pattern])
        regex_search = re.compile(pattern).search
        offset = start or 0
        try:
            if offset:
                fh_seek(offset)
        except IOError:
            e = sys.exc_info()[1]

        try:
            buffer = fh_read(len_pattern + read_size)
            match = regex_search(buffer)
            match = -1 if match == None else match.start()

            while True:
                if match == -1:
                    offset += read_size
                    if end and offset > end:
                        return
                    buffer = buffer[read_size:]
                    buffer += fh_read(read_size)
                    match = regex_search(buffer)
                    match = -1 if match == None else match.start()
                else:
                    if match == -1 and offset + match > end:
                        return
                    find_offset = offset + match
                    self.find_offset.append(find_offset)
                    if max_matches:
                        max_matches -= 1
                        if max_matches == 0:
                            sys.stdout.write("Found maximum number of matches.\n")
                            return
                    match = regex_search(buffer, match + 1)
                    match = -1 if match == None else match.start()
                if len(buffer) <= len_pattern:
                    return

        except IOError:щ
            e = sys.exc_info()[1]

    def search(self, close_file=True):
        self.__search_loop(self.start, self.end, self.bufsize, self.search_pattern, self.max_matches, self.verbose,
                           self.fh.name, self.fh.read, self.fh.seek)
        if close_file:
            self.fh.close()
        return self.find_offset

    def replace(self):
        self.search(close_file=False)
        for item in self.find_offset:
            print("Replace: %s -> %s by offset [ %d (Dec) 0x%0.2X (Hex) ]" % (self.search_pattern[0].hex(), self.replace_pattern[0].hex(), item, item))
            self.fh.seek(item)
            self.fh.write(self.replace_pattern[0])
        self.fh.close()


if __name__ == '__main__':
    BinaryPatch(file='boot.img', search="1387C7", replace="13FFFF").replace()
