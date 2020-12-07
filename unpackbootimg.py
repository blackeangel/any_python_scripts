from __future__ import print_function

import binascii
import os
import struct
import sys
import traceback

BOOT_MAGIC = "ANDROID!"
BOOT_MAGIC_SIGN = "BFBF"
BOOT_MAGIC_SIZE = 8
BOOT_NAME_SIZE = 16
BOOT_ARGS_SIZE = 512

MODE_STANDARD = 1
MODE_DEGAS = 2

if sys.version_info >= (3,0):
    unicode = str
	
class BootImg(object):

    def __init__(self,
                 board=None, base=None, cmdline=None, page_size=None,
                 kernel_offset=None, ramdisk_offset=None, second_offset=None,
                 tags_offset=None, kernel=None, ramdisk=None, second=None, dt=None,
                 signature=None):

        self.board = board
        self.base = base
        self.cmdline = cmdline
        self.page_size = page_size
        self.kernel_offset = kernel_offset
        self.ramdisk_offset = ramdisk_offset
        self.second_offset = second_offset
        self.tags_offset = tags_offset
        self.kernel = kernel
        self.ramdisk = ramdisk
        self.second = second
        self.dt = dt
        self.signature = signature

    def __int_address(self, addr):
        if addr is None:
            return None

        return int(addr, 16) if type(addr) in (str, unicode) else addr

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, value):
        self._base = self.__int_address(value)

    @property
    def cmdline(self):
        return self._cmdline

    @cmdline.setter
    def cmdline(self, value):
        self._cmdline = value

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        self._page_size = int(value) if value is not None else None

    @property
    def kernel_offset(self):
        return self._kernel_offset

    @kernel_offset.setter
    def kernel_offset(self, value):
        self._kernel_offset = self.__int_address(value)

    @property
    def ramdisk_offset(self):
        return self._ramdisk_offset

    @ramdisk_offset.setter
    def ramdisk_offset(self, value):
        self._ramdisk_offset = self.__int_address(value)

    @property
    def second_offset(self):
        return self._second_offset

    @second_offset.setter
    def second_offset(self, value):
        self._second_offset = self.__int_address(value)

    @property
    def tags_offset(self):
        return self._tags_offset

    @tags_offset.setter
    def tags_offset(self, value):
        self._tags_offset = self.__int_address(value)

    @property
    def kernel(self):
        return self._kernel

    @kernel.setter
    def kernel(self, value):
        self._kernel = value

    @property
    def ramdisk(self):
        return self._ramdisk

    @ramdisk.setter
    def ramdisk(self, value):
        self._ramdisk = value

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, value):
        self._second = value

    @property
    def second_size(self):
        return os.path.getsize(self._second) if self._second and os.path.exists(self._second) else 0

    @property
    def dt(self):
        return self._dt

    @property
    def dt_size(self):
        return os.path.getsize(self._dt) if self._dt and os.path.exists(self._dt) else 0

    @dt.setter
    def dt(self, value):
        self._dt = value

    @property
    def signature(self):
        return self._signature

    @signature.setter
    def signature(self, value):
        self._signature = value


def read_padding(f, itemsize, pagesize):
    pagemask = pagesize - 1

    if (itemsize & pagemask) == 0:
        return 0

    count = pagesize - (itemsize & pagemask)

    f.read(count)

    return count


def bytes_to_str(data):
    temp = binascii.hexlify(data).decode("utf-8")
    #return "\\x" + "\\x".join(a + b for a, b in zip(temp[::2], temp[1::2]))
    return "".join(a + b for a, b in zip(temp[::2], temp[1::2]))


show_output = True
use_stdout = False


def print_i(line):
    if show_output:
        if use_stdout:
            print(line)
        else:
            print(line, file=sys.stderr)


def extract(filename, directory, mode = MODE_STANDARD):
    basename = os.path.split(filename)[1]
    f = open(filename, 'rb')
    temp = f.read(BOOT_MAGIC_SIZE)
    if temp == BOOT_MAGIC.encode("ASCII"):
        print("Found Android header")
        f.seek(0, os.SEEK_SET)
    elif temp[0:4]== BOOT_MAGIC_SIGN.encode("ASCII"):
        print("Found BF header")
        f.seek(16448, 0)
    else:
        raise Exception("Android header not found")

    # Read Android header
    sformat = '<'
    sformat += str(BOOT_MAGIC_SIZE) + 's'  # magic
    sformat += '10I'                       # kernel_size, kernel_addr,
                                           # ramdisk_size, ramdisk_addr,
                                           # second_size, second_addr,
                                           # tags_addr, page_size,
                                           # dt_size, unused
    sformat += str(BOOT_NAME_SIZE) + 's'   # name
    sformat += str(BOOT_ARGS_SIZE) + 's'   # cmdline
    sformat += str(8 * 4) + 's'            # id (unsigned[8])

    header_size = struct.calcsize(sformat)
    header = f.read(header_size)

    if mode == MODE_DEGAS:
        magic, kernel_size, kernel_addr, \
            ramdisk_size, ramdisk_addr, \
            second_size, second_addr, \
            dt_size, unused, \
            tags_addr, page_size, \
            board, cmdline, ident = struct.unpack(sformat, header)
    else:
        magic, kernel_size, kernel_addr, \
            ramdisk_size, ramdisk_addr, \
            second_size, second_addr, \
            tags_addr, page_size, \
            dt_size, unused, \
            board, cmdline, ident = struct.unpack(sformat, header)

    ramdisk_offset = ramdisk_addr - kernel_addr + 0x00008000
    tags_offset = tags_addr - kernel_addr + 0x00008000
    second_offset = second_addr - kernel_addr + 0x00008000
    base = kernel_addr - 0x00008000
    kernel_offset = kernel_addr - base
    kernel = os.path.join(directory, basename + "-zImage")
    dt = os.path.join(directory, basename + "-dt")
    cmdline =  cmdline.decode('ASCII').rstrip('\0')
    signature = os.path.join(directory, basename + "-signature")

    # cmdline
    out = open(os.path.join(directory, basename + "-cmdline"), 'wb')
    out.write((cmdline + '\n').encode('ASCII'))
    out.close()

    # base
    out = open(os.path.join(directory, basename + "-base"), 'wb')
    out.write(('%08x\n' % (kernel_addr - 0x00008000)).encode('ASCII'))
    out.close()

    # ramdisk_offset
    out = open(os.path.join(directory, basename + "-ramdisk_offset"), 'wb')
    out.write(('%08x\n' % ramdisk_offset).encode('ASCII'))
    out.close()

    # second_offset
    out = open(os.path.join(directory, basename + "-second_offset"), 'wb')
    out.write(('%08x\n' % second_offset).encode('ASCII'))
    out.close()

    # tags_offset
    out = open(os.path.join(directory, basename + "-tags_offset"), 'wb')
    out.write(('%08x\n' % tags_offset).encode('ASCII'))
    out.close()

    # page_size
    out = open(os.path.join(directory, basename + "-pagesize"), 'wb')
    out.write(('%d\n' % page_size).encode('ASCII'))
    out.close()

    read_padding(f, header_size, page_size)

    # zImage
    out = open(kernel, 'wb')
    k = f.read(kernel_size)
    out.write(k)
    out.close()

    read_padding(f, kernel_size, page_size)

    # ramdisk
    ramdisk = f.read(ramdisk_size)
    if ramdisk[0] == 0x02 and ramdisk[1] == 0x21:
        ramdisk_path = os.path.join(directory, basename + "-ramdisk.lz4")
    else:
        ramdisk_path = os.path.join(directory, basename + "-ramdisk.gz")

    out = open(ramdisk_path, 'wb')
    out.write(ramdisk)
    out.close()

    read_padding(f, ramdisk_size, page_size)

    # second
    out = open(os.path.join(directory, basename + "-second"), 'wb')
    out.write(f.read(second_size))
    out.close()

    read_padding(f, second_size, page_size)

    # dt
    out = open(dt, 'wb')
    out.write(f.read(dt_size))
    out.close()


    img = BootImg(
        board = board,
        base=base,
        cmdline=cmdline,
        page_size=page_size,
        kernel_offset=kernel_offset,
        ramdisk_offset=ramdisk_offset,
        second_offset=second_offset,
        tags_offset=tags_offset,
        kernel=kernel,
        ramdisk=ramdisk_path,
        second=None,
        dt=dt
    )

    if mode == MODE_DEGAS:
        #signature
        out = open(signature, 'wb')
        out.write(f.read(256))
        out.close()
        img.signature = signature

    f.close()

    print(img)
    return img


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_i("Usage: %s -i boot.img [-o output_directory]" % sys.argv[0])
        sys.exit(1)

    filename = ""
    directory = ""

    counter = 1
    degas = False
    while counter < len(sys.argv):
        if sys.argv[counter] == "-i":
            filename = sys.argv[counter + 1]
            counter += 2
        elif sys.argv[counter] == "-o":
            directory = sys.argv[counter + 1]
            counter += 2
        elif sys.argv[counter] == '--degas':
            degas = True
            counter += 1
        else:
            print_i("Unrecognized argument " + sys.argv[counter])
            sys.exit(1)

    if filename == "":
        print_i("No boot image specified")
        sys.exit(1)

    if not os.path.exists(filename):
        print_i(filename + " does not exist")
        sys.exit(1)

    if directory == "":
        directory = os.getcwd()
    elif not os.path.exists(directory):
        os.makedirs(directory)

    try:
        use_stdout = True
        extract(filename, directory, MODE_DEGAS if degas else MODE_STANDARD)
    except Exception as e:
        use_stdout = False
        print(traceback.format_exc())
        print_i("Failed: " + str(e))