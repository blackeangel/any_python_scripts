import os
tmpfile="/sdcard/tmpfile.xml"
arr=[]
open(tmpfile, 'w').write('<?xml version="1.0" ?>\n<data>\n')
for file in os.listdir("/sdcard"):
    if file.endswith(".xml"):
        with open(os.path.join("/sdcard", file)) as f:
            for line in f:
                if 'label="system"' in line or 'label="vendor"' in line:
                    arr.append(line)
for i in arr:
    open(tmpfile, 'a').write(i)
open(tmpfile, 'a').write('</data>')
open(tmpfile, 'a').close()