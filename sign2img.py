import os, sys

class Extractor(object):
    def __file_name(self, file_path):
        return os.path.basename(file_path).split('.')[0]

    def main(self, target):
        new_name = os.path.realpath(os.path.dirname(sys.argv[1])) + os.sep + (self.__file_name(target)).split("-")[0] + ".img"
        with open(target, "rb") as f:
            byte = f.read(16448)
            while byte:
                byte = f.read(16448)
                with open(new_name, 'ab') as p:
                    p.write(byte)

Extractor().main(sys.argv[1])
