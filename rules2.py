import sys
def rul(st):
    Listgroup=['0','1000','1001','1002','1003','1004','1005','1006','1007','1008','1009','1010','1011','1012','1013','1014','1015','1016','1017','1018','1019','1020','1021','1023','1024','1026','1027','1028','1029','1030','1031','1032','1033','1034','1035','1036','1037','2000','2001','2002','3001','3002','3003','3004','3005','3006','3007','3008','9997','9998','9999']
    rul8=[]
    for _ in range(778):
        if _>0:
            if _<10:
                rul8.append('00'+str(_))
            elif _<100:
                rul8.append('0'+str(_))
            else:
                rul8.append(str(_))

    result = []
    data = st.replace(' ','')
    for i in data:
        if not i.isdigit():
            data=data.replace(i,'')
    for _ in range(2) :
        if data[0] != '0':
             result.append(data[:4])
             data = data[4:]
        else:
            result.append(data[0])
            data = data[1:]
    result.append(data)
    print(result)
    return ' '.join(result)
 
if __name__ == '__main__':
    #print(rul(sys.argv[1]))
    print(rul("2000 0000 644"))