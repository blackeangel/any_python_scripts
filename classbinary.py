import os, sys, mmap
class BinaryPatch(object):
    def init(self, file=None, search=None, replace=None, symbol=None):
        self.target = file
        self.search_pattern = self.__text_to_pattern(search)
        if len(replace) < len(search):
            self.replace_pattern = self.__text_to_pattern(replace, symbol=symbol, len=len(search)-len(replace))
        else:
            self.replace_pattern = self.__text_to_pattern(replace)
        bsize = len(b"".join(self.search_pattern))*2
        self.bsize = max(bsize, 2 ** 23)
        self.max_matches = None
        self.start = 0
        self.end = 0
        self.verbose = False
        self.find_offset = []

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
            return [t.encode('utf-8') for t in text.split("?")]
        except TypeError:
            return [t for t in text.split("?")]

    def search(self, fh):
        self.__search_loop(self.start, self.end, self.bsize, self.search_pattern, self.max_matches, self.verbose, fh.name, fh.read, fh.seek)

    def __search_loop(self, start, end, bsize, pattern, max_matches, verbose, fh_name, fh_read, fh_seek):
        len_pattern = len(b"?".join(pattern))
        read_size = bsize - len_pattern
        pattern = [re.escape(p) for p in pattern]
        pattern = b".".join(pattern)
        regex_search = re.compile(pattern, re.DOTALL + re.MULTILINE).search
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
        except IOError:
            e = sys.exc_info()[1]

    def patch(self):
        try:
            filehandler = open(self.target, 'r+b')
        except IOError:
            e = sys.exc_info()[1]
        self.search(filehandler)
        for item in self.find_offset:
            filehandler.seek(item)
            filehandler.write(self.replace_pattern[0])
        filehandler.close()
        
#Using:      
#BinaryPatch(file="ПУТЬ к ФАЙЛУ", search="СТРОКА_ПОИСКА"), replace="СТРОКА_ЗАМЕНЫ", symbol='00').patch()