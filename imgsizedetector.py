import os
import sys
import struct

EXT4_HEADER_MAGIC = 0xED26FF3A
EXT4_SPARSE_HEADER_LEN = 28
EXT4_CHUNK_HEADER_SIZE = 12

class ext4_file_header(object):
    def __init__(self, buf):
        (self.magic,
         self.major,
         self.minor,
         self.file_header_size,
         self.chunk_header_size,
         self.block_size,
         self.total_blocks,
         self.total_chunks,
         self.crc32) = struct.unpack('<I4H4I', buf)


class ext4_chunk_header(object):
    def __init__(self, buf):
        (self.type,
         self.reserved,
         self.chunk_size,
         self.total_size) = struct.unpack('<2H2I', buf)


class Extractor(object):
    def __init__(self):
        self.FileName = ""
        self.BASE_DIR = ""
        self.OUTPUT_IMAGE_FILE = ""
        self.EXTRACT_DIR = ""
        self.BLOCK_SIZE = 4096
        self.TYPE_IMG = 'system'
        self.context = []
        self.fsconfig = []

    def __file_name(self,file_path):
        name = os.path.basename(file_path).split('.')[0]
        name = name.split('-')[0]
        name = name.split('_')[0]
        name = name.split(' ')[0]
        return name

    def __ImgSizeFromSparseFile(self, target):
        with open(target, "rb") as img_file:
            if self.sign_offset > 0:
                img_file.seek(self.sign_offset, 0)
            header = ext4_file_header(img_file.read(28))
            imgsize=header.block_size*header.total_blocks
        return imgsize

    def __ImgSizeFromRawFile(self, target):
        with open(target, "rb") as img_file:
            m = ''
            see = 0x404
            for i in reversed(range(0, 4)):
                img_file.seek(see + i, 0)
                m = m + img_file.read(1).hex()
                imgsize = int('0x' + m, 0) * 4096
        return imgsize

    def checkSignOffset(self, file):
        import mmap
        mm = mmap.mmap(file.fileno(), 52428800, access=mmap.ACCESS_READ)  # 52428800=50Mb
        offset = mm.find(struct.pack('<L', EXT4_HEADER_MAGIC))
        return offset

    def __getTypeTarget(self, target):
        filename, file_extension = os.path.splitext(target)
        if file_extension == '.img':
            with open(target, "rb") as img_file:
                setattr(self, 'sign_offset', self.checkSignOffset(img_file))
                if self.sign_offset > 0:
                    img_file.seek(self.sign_offset, 0)
                header = ext4_file_header(img_file.read(28))
                if header.magic != EXT4_HEADER_MAGIC:
                    return 'img'
                else:
                    return 'simg'

    def main(self, target, output_dir):
        self.BASE_DIR = (os.path.realpath(os.path.dirname(target)) + os.sep)
        self.EXTRACT_DIR = os.path.realpath(os.path.dirname(output_dir)) + os.sep + self.__file_name(os.path.basename(output_dir)) #output_dir
        self.OUTPUT_IMAGE_FILE = self.BASE_DIR + os.path.basename(target)
        self.FileName = self.__file_name(os.path.basename(target))
        target_type = self.__getTypeTarget(target)
        if target_type == 'simg':
            print(self.__ImgSizeFromSparseFile(target))
        if target_type == 'img':
            print(self.__ImgSizeFromRawFile(target))


if __name__ == '__main__':
    if sys.argv.__len__() == 3:
        Extractor().main(sys.argv[1], sys.argv[2])
    else:
        if sys.argv.__len__() == 2:
            Extractor().main(sys.argv[1], os.path.realpath(os.path.dirname(sys.argv[1])) + os.sep + os.path.basename(sys.argv[1]).split('.')[0])
        else:
            print("Must be at least 1 argument...")
            sys.exit(1)
