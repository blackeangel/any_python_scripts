import mmap, sys, os, binascii, argparse
def finder(file, whatfind):
      wfrez=whatfind
      whatfind=bytes.fromhex(whatfind)
      mass = []
      with open(file, 'rb') as f:
          step=4096
          offset=0
          size = os.stat(file).st_size
          mm=mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
          m=mm.find(whatfind)
          while True:
                if offset + step > size:
                      break
                pos = mm.find(whatfind, offset, offset + step)
                if pos == -1:
                      offset += step
                else:
                      mm.seek(pos)
                      mass.append(hex(pos)[2:])
                      print('finding value: %s offset: %s'%(wfrez, hex(pos)))
                      offset = pos + len(whatfind)
      return m
def main(file,wf):
    offs=finder(file,wf)
    print(offs)
    with open(file, "r+b") as ff:
        mms=mmap.mmap (ff.fileno(),0)
        mms.seek(offs)
        mms.write(b'\x00\x00\x00\x00')
    
if __name__ == '__main__':
    if sys.argv.__len__() == 3:
        print(main(sys.argv[1], sys.argv[2]))