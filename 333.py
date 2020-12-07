import sys, binascii

def finder(file, woffset, nbytes):
    with open(file, "rb") as f:
         f.seek(int(woffset, 16))
         m=binascii.hexlify(f.read(nbytes)).decode("ascii")
    return m

if __name__ == '__main__':
    if sys.argv.__len__() == 4:
        print(finder(sys.argv[1], sys.argv[2], int(sys.argv[3])))