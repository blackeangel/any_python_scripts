import os
import sys
import struct
import tarfile
import argparse

__version__ = '0.1.0a'
__author__ = 'unix3dgforce [MiuiPro.by DEV Team]'
__copyright__ = 'Copyright (c) 2018 Miuipro.by'


class UnpackTar(object):
    def __init__(self):
        self.BASE_DIR = os.path.dirname(sys.argv[0]).replace('/', os.sep) + os.sep
        self.PROJECT_NAME = None

    def __appendf(self, msg, log_file):
        with open(log_file, 'a', newline='\n') as file:
            print(msg, file=file)

    def unpack(self, input_file, output_dir, compression='r'):
        self.PROJECT_NAME = os.path.basename(input_file).split('.')[0]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        with tarfile.open(input_file, compression) as tar:
            for item in tar:
                if item.isdir() or item.isfile():
                    self.__appendf('%s %s %s %s' % (item.path[1:], item.uid, item.gid, oct(item.mode)[-4:]), 'project____%s____statfile.txt' % self.PROJECT_NAME)
                    item.path = (output_dir + item.path).replace('/', os.sep)
                    tar.extract(item)
                elif item.issym():
                    self.__appendf('symlink("%s", "%s");' % (item.linkpath, item.path), 'project____%s____symlinks.txt' % self.PROJECT_NAME)
                    with open((output_dir + item.path).replace('/', os.sep), 'wb') as out:
                        tmp = bytes.fromhex('213C73796D6C696E6B3EFFFE')
                        for index in list(item.linkpath):
                            tmp = tmp + struct.pack('>sx', index.encode('utf-8'))
                        out.write(tmp + struct.pack('xx'))
                        os.system('attrib +s %s' % (output_dir + item.path).replace('/', os.sep))

def createParser():
    parser = argparse.ArgumentParser(description='Unpack Tar archives', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-v', '--version', action='version',
                       version='Firmware Service version [' + __version__ + '] ')
    parser.add_argument('-i', '--input', help='path to input file')
    parser.add_argument('-o', '--output', help='path to output dir')
    parser.add_argument('-c', '--compression', help='gzip: -c gz or --compression gz\n'
                                                    'bzip2: -c bz2 or --compression bz2\n'
                                                    'lzma: -c xz or --compression xz')
    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    if len(sys.argv) >= 2:
        if namespace.compression:
            UnpackTar().unpack(namespace.input, namespace.output, compression='r:' + namespace.compression)
        else:
            UnpackTar().unpack(namespace.input, namespace.output)
        sys.exit(0)
    else:
        parser.print_usage()
        sys.exit(1)
