import os, sys, re
configlistfile=[]
with open('/home/sam/PycharmProjects/untitled/config/system_fs_config','rt') as config:
    configmass=config.readlines()
configmass = [[n for n in x.split()] for x in configmass]
for i in range(len(configmass)):
    #print(configmass[i][0])
    configlistfile.append(configmass[i][0])

with open('/home/sam/PycharmProjects/untitled/config/system_file_contexts','rt') as contexts:
    contextsmass=contexts.readlines()
contextsmass = [[m for m in y.split()] for y in contextsmass]

#for i in range(len(contextsmass)):
#    print(contextsmass[i][0]) #нужный столбец только с путями к файлам

root_path = '/home/sam/PycharmProjects/untitled/system/'
mnk=root_path.split(os.sep)
for i in mnk:
    if i == '':
        mnk.remove(i)
file_list=[]
for root, dirs, files in os.walk(root_path):
    for named in dirs:
        file_list.append((os.path.join(root.replace(root_path,mnk[len(mnk)-1]+"/"), named)).replace(os.sep, "/"))
    for namef in files:
        file_list.append((os.path.join(root.replace(root_path,mnk[len(mnk)-1]+"/"), namef)).replace(os.sep, "/"))
file_list.sort()
#for ii in file_list:
#    print(ii)
#списки получены, теперь надо сравнивать
#сначала сравним, не удалили ли что-то
exceptlist_deleted=list(set(configlistfile)-set(file_list))
#если что то удалили, то выкинем это из обоих массивов
if len(exceptlist_deleted)!=0:
    for k in range(len(configmass)-1,-1,-1):
        if  set(file_list) & set(configmass[k]):
            del configmass[k]
    for l in range(len(contextsmass)-1,-1,-1):
        if  set(file_list) & set(contextsmass[l]):
            del contextsmass[l]
tmp2=[[]]
exceptlist_add=list(set(file_list)-set(configlistfile)) #нашли то чего нет в конфигах
#если что то добавили...то будет много кода :)
if len(exceptlist_add)!=0:
    #print(exceptlist_add)
    for y in exceptlist_add:
        tmplistconf = [[]]
        r=y.count("/")
        mfold=y[0:y.rfind("/")]
        #print(mfold)
        for m in configmass:

            for mln in m:
                if mfold in mln:
                    #print(mfold)
                    if mln.count("/") == r:
                        tmplistconf.append(m)
                        #print(m)
        if len(tmplistconf[0])==0:
            del tmplistconf[0]
        #print(tmplistconf)
        k=len(tmplistconf) # k - количество строк в массиве
        k1=len(tmplistconf[0]) # к1 - количество элементов в строке
        #for el in exceptlist_add:
        tmp1=[]
        tmp=[]
        tmp.append(y)
        for j in range(k) :
            st = ''
            for i in range(1,k1) :
                    st += str(tmplistconf[j][i])
            tmp1.append(st)
        times = 0
        for i in set(tmp1) :
            f = tmp1.count(i)
            if times < f :
                times = f
                ki = tmp1.index(i) # ki - индекс строки с самым частым "хвостом"
        tmp.extend(tmplistconf[ki][1:])
        tmp2.append(tmp)
            #print(tmp)
            #tmplistconf.append(tmp)# добавление к массиву "результирующей" строки
        #tmplistconf = [[]]
#вставка столбца в конец:
#for i in tmp2:
#"    i.insert(len(i),0)
tmp2.sort()
print(tmp2)
print(tmplistconf)
     #print(tmplistconf)
        #    pass
#теперь надо получить, права и контексты той папки, в которой лежит файл
#print(len(exceptlist_add))
#for it in exceptlist_add:
#    print(it)
#print(len(exceptlist_deleted))
#for ik in exceptlist_deleted:
#    print(ik)
#print(root_path.count("/")) #сколько / в строке понадобится для глубины поиска
#arr.sort(key = lambda z: z[0]) #сортировка по 0 столбцу
