import tarfile, sys, os, struct

def __file_name(file_path):
    return os.path.split(file_path)[1].split('.')[0]

def __appendf(msg, log_file):
    with open(log_file, 'a', newline='\n') as file:
        print(msg, file=file)

def untar(fname, output_dir):
    mass = []
    filename = __file_name(fname)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    with tarfile.open(fname, "r") as tar:
        for tarinfo in tar:
            cap = ''
            con = ''
            if 'RHT.security.selinux' in tarinfo.pax_headers:
                con = tarinfo.pax_headers.get('RHT.security.selinux')
            if 'SCHILY.xattr.security.capability' in tarinfo.pax_headers:
               try:
                   data = bytearray(tarinfo.pax_headers.get('SCHILY.xattr.security.capability').encode('utf-8'))
               except:
                    data = bytearray(tarinfo.pax_headers.get('SCHILY.xattr.security.capability').encode('utf-8', 'surrogateescape'))
               cap = '' + str(hex(struct.unpack("<5I", data)[1]))
            if tarinfo.issym():
                if cap == '' and con == '':
                    mass.append('%s %s %s %s %s' % (("/" + filename + "/" + tarinfo.path).replace("/" + filename + "/" + filename, "/" + filename), tarinfo.uid, tarinfo.gid, oct(tarinfo.mode).__str__()[-4:], tarinfo.linkpath))
                else:
                    if cap == '':
                        mass.append('%s %s %s %s %s %s' % (("/" + filename + "/" + tarinfo.path).replace("/" + filename + "/" + filename, "/" + filename),tarinfo.uid, tarinfo.gid, oct(tarinfo.mode).__str__()[-4:], con, tarinfo.linkpath))
                    else:
                        if con == '':
                            mass.append('%s %s %s %s %s %s' % (("/" + filename + "/" + tarinfo.path).replace("/" + filename + "/" + filename, "/" + filename), tarinfo.uid, tarinfo.gid, oct(tarinfo.mode).__str__()[-4:], cap, tarinfo.linkpath))
                        else:
                            mass.append('%s %s %s %s %s %s %s' % (("/" + filename + "/" + tarinfo.path).replace("/" + filename + "/" + filename, "/" + filename), tarinfo.uid, tarinfo.gid, oct(tarinfo.mode).__str__()[-4:], cap, con, tarinfo.linkpath))
                if os.name == 'nt':
                    pathfile = os.path.normpath(output_dir + tarinfo.path).replace(filename + os.sep + filename, filename)
                    with open(pathfile, 'wb') as out:
                        tmp = bytes.fromhex('213C73796D6C696E6B3EFFFE')
                        for index in list(tarinfo.linkpath):
                            tmp = tmp + struct.pack('>sx', index.encode('utf-8'))
                        out.write(tmp + struct.pack('xx'))
                        os.system('attrib +s %s' % pathfile)
                if os.name == 'posix':
                    pathfile = os.path.normpath(output_dir + tarinfo.path).replace(filename + os.sep + filename, filename)
                    os.symlink(tarinfo.linkpath, pathfile)
            else:
                if cap == '' and con == '':
                    mass.append('%s %s %s %s' % (("/" + filename + "/" + tarinfo.path).replace("/" + filename + "/" + filename, "/" + filename), tarinfo.uid, tarinfo.gid, oct(tarinfo.mode).__str__()[-4:]))
                else:
                    if cap == '':
                        mass.append('%s %s %s %s %s' % (("/" + filename + "/" + tarinfo.path).replace("/" + filename + "/" + filename, "/" + filename),tarinfo.uid, tarinfo.gid, oct(tarinfo.mode).__str__()[-4:], con))
                    else:
                        if con == '':
                            mass.append('%s %s %s %s %s' % (("/" + filename + "/" + tarinfo.path).replace("/" + filename + "/" + filename, "/" + filename), tarinfo.uid, tarinfo.gid, oct(tarinfo.mode).__str__()[-4:], cap))
                        else:
                            mass.append('%s %s %s %s %s %s' % (("/" + filename + "/" + tarinfo.path).replace("/" + filename + "/" + filename, "/" + filename), tarinfo.uid,tarinfo.gid, oct(tarinfo.mode).__str__()[-4:], cap, con))
                tarinfo.path = os.path.normpath(output_dir + tarinfo.path).replace(filename + os.sep + filename, filename)
                tar.extract(tarinfo)
    mass.sort()
    __appendf('\n'.join(mass), os.path.realpath(os.path.dirname(fname)) + os.sep + filename + "_statfile.txt")

if __name__ == '__main__':
    if sys.argv.__len__() == 3:
        untar(sys.argv[1], sys.argv[2] + os.sep)
    else:
        if sys.argv.__len__() == 2:
            untar(sys.argv[1], os.path.realpath(os.path.dirname(sys.argv[1])) + os.sep + __file_name(sys.argv[1]) + os.sep)
        else:
            print("Must be at least 1 argument...")
            sys.exit(1)