from shutil import make_archive
import os, sys
def createzip(namezip, fold):
	archive_name = os.path.realpath(fold) + os.sep + namezip
	make_archive(archive_name, 'zip', os.path.realpath(fold))

if __name__ == '__main__':
	createzip(sys.argv[1], sys.argv[2])