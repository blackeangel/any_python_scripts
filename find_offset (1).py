import os, sys, mmap
detctbuild = b'\x00\x40\x0d\x01'
#detctbuild = b'\x10\xd4\x00\x00'
#detctbuild = b'\x69\x13\x0f'
file="/sdcard/kernel_orig.tmp"
#mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
#offset = mm.find(detctbuild)
#print (offset)
with open(file, "r+b") as f:
            step = mmap.ALLOCATIONGRANULARITY
            offset = 0
            size = os.stat(file).st_size
            map_ = mmap.mmap(f.fileno(), length=step)
            while True:
                    offset += step
                    if offset + step > size:
                        break
                    if map_.find(detctbuild)==-1:
                        map_ = mmap.mmap(f.fileno(), length=step, offset=offset)
                    else:
                        offset=map_.find(detctbuild)
                        break
print(offset)
print(hex(offset))