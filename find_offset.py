import mmap, sys, os, binascii, argparse
def findoffset(file, whatfind):
      wfrez=whatfind
      whatfind=bytes.fromhex(whatfind)
      mass = []
      with open(file, 'rb') as f:
          step=4096
          offset=0
          size = os.stat(file).st_size
          mm=mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
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
      return mass
      
def perevorot(key, stroka):
    m=''        
    if ' ' in stroka:
        stroka=stroka.replace(" ","")
    if (len(stroka)/2).is_integer()==False:
        stroka='0'+stroka
    while len(stroka)>0:
        if key=="-s":
           m=m+stroka[-2:]+" "
        else:
           m=m+stroka[-2:]
        stroka=stroka[:-2]
    if key=="-s":
       print('inverted value %s'%(m[:-1]))
       return m[:-1]
    else:
        print('inverted value %s'%(m))
        return m

def findbyte(file, woffset, nbytes):
    m=''
    with open(file, "rb") as f:
         f.seek(int(woffset, 16))
         m=binascii.hexlify(f.read(nbytes)).decode("ascii")
         print('new value: %s'%(m))
    return m
    
def writebyte(file, offs, wrp):
    if wrp=="":
        wrp="00"
    wrp=bytes.fromhex(wrp)
    print(wrp)
    offs=int(offs, 16)
    print(offs)
    with open(file, 'r+b') as ff:
        mms=mmap.mmap (ff.fileno(),0)
        print(offs)
        mms.seek(offs)
        print(wrp)
        mms.write(wrp)
        
def replacebyte(file,whatfind,whatreplace):
      if whatreplace=='' or len(whatreplace)==0:
          for i in range(len(whatfind)):
              whatreplace=whatreplace+'0'
      if len(whatfind)!=len(whatreplace):
          return
      whatfind=bytes.fromhex(whatfind)
      whatreplace=bytes.fromhex(whatreplace)
      with open(file, 'r+b') as f:
          step=4096
          offset=0
          size = os.stat(file).st_size
          mm=mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)
          while True:
                if offset + step > size:
                      break
                pos = mm.find(whatfind, offset, offset + step)
                if pos == -1:
                      offset += step
                else:
                      mm.seek(pos)
                      mm.write(whatreplace)
                      offset = pos + len(whatfind)     
def main():
      print('\n')
      firststep=[]
      secondstep=[]
      thirdstep=[]
      firststep=findoffset(FILE, WHATFIND)
      print('\n')
      for poz in firststep:
            secondstep.append(perevorot("",poz))
      print('\n')
      for rop in secondstep: 
           thirdstep.append(findbyte(FILE,rop,BYTEOUTPUT))
      print('\n')
      print(thirdstep)
      for rub in thirdstep:
          replacebyte(FILE, rub, WHATREPLACE)
          #writebyte(FILE, rub, WHATREPLACE)
      #return thirdstep
            
if __name__ == '__main__':
      #if sys.argv.__len__() == 3:
      #      print(startfind(sys.argv[1], sys.argv[2]))      

      parser = argparse.ArgumentParser(description='Asked me(blackeangel) for more informations')
      parser.add_argument('file', type=str, default="kernel_orig.tmp", help='input file')
      parser.add_argument('whatfind', type=str, help='what find in file, for example 014d6f')
      parser.add_argument('-c', '--countfind', type=int, default=0, help='how many times the desired value occurs, by default - all')
      parser.add_argument('-p', '--perevorot', type=int, default=1, help='flip or not value, by default - yes(1)')
      parser.add_argument('-b', '--byteoutput', type=int, default=3, help='how many bytes to output, by default - 3')
      parser.add_argument('-wr', '--whatreplace', type=str, default="", help='what to replace found values')
      
      args = parser.parse_args()

      if args.file: FILE=args.file
      if args.whatfind: WHATFIND=args.whatfind
      if args.countfind: COUNTFIND=args.countfind
      if args.perevorot: PEREVOROT=args.perevorot
      if args.byteoutput: BYTEOUTPUT=int(args.byteoutput)
      if args.whatreplace: WHATREPLACE=args.whatreplace
          
      main()