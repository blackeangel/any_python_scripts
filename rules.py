import sys

def rul(st):
    k=''
    st=st.replace(' ','')
    if len(st)==5:
        k=st[0] + ' ' + st[1] + ' ' + st[2:5]
        
    if len(st)==6:
        k=st[0] + ' ' + st[1] + ' ' + st[2:6]
        
    if len(st)==8:
        if st[0]=='0':
            k=st[0] + ' ' + st[1:5] + ' ' + st[5:8]
        else:
            k=st[0:4] + ' ' + st[4] + ' ' + st[5:8]
            
    if len(st)==9:
        if st[0]=='0':
            k=st[0] + ' ' + st[1:5] + ' ' + st[5:9]
        else:
            k=st[0:4] + ' ' + st[4] + ' ' + st[5:9]
            
    if len(st)==11:
        k=st[0:4] + ' ' + st[4:8] + ' ' + st[8:11]
        
    if len(st)==12:
        k=st[0:4] + ' ' + st[4:8] + ' ' + st[8:12]
        
    return k
    
if __name__ == '__main__':
    print(rul(sys.argv[1]))
    
#print(rul("2001 200 107 55"))

#2000 2000 0755
#2000 2000 755
#0 2000 0755
#0 2000 755
#0 0 0755
#0 0 755