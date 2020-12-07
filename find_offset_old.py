import sys, os
def reversefinder(file, whatfind):
    whatfind=bytes.fromhex(whatfind)
    size=os.stat(file).st_size
    read_dump=52428800
    with open(file, "rb") as f:
        f.seek(size-read_dump)
        mm=f.read(read_dump)
        offfset=mm.find(whatfind)
        if offfset>0:
            offfset=(size-read_dump)+offfset
            print("finding AVB structure in %s"%(hex(offfset)))
        else:
            print("AVB structure not found!")
    return offfset
    
def main(file, whatfind, savefolder):
    offset=reversefinder(file, whatfind)
    if offset>0:
        fileavbtxt=savefolder+os.sep+os.path.basename(os.path.abspath(file)).split(".")[0]+"_size_no_AVB0.txt"
        ftxt=open(fileavbtxt,'tw')
        print(offset,file=ftxt)
        ftxt.close()
        size=os.stat(file).st_size
        nwritebyte=size-offset
        with open(file,'rb') as f:
            f.seek(offset)
            readbyte=f.read(nwritebyte)
        fileavb=savefolder+os.sep+os.path.basename(os.path.abspath(file)).split(".")[0]+"AVB0.img"
        with open(fileavb,'wb') as favb:
            favb.write(readbyte)
    else:
        return
         
if __name__ == '__main__':
    if sys.argv.__len__() == 3:
        main(sys.argv[1], sys.argv[2],os.path.dirname(os.path.abspath(sys.argv[2])))
    if sys.argv.__len__() == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])