
FIRST = {}

FOLLOW = {}
grammars = [
'E->TG',
'G->+TG',
'G->ε',
'T->FS',
'S->*FS',
'S->ε',
'F->(E)',
'F->i'
]
# grammars = [
# 'E->TG',
# 'G->+TG',
# 'G->-TG',
# 'G->ε',
# 'T->FS',
# 'S->*FS',
# 'S->/FS',
# 'S->ε',
# 'F->(E)',
# 'F->i',]

#初始化 first 集 和follow集合字典的键值对中的 值 为空
def initail():
    for str  in grammars :
        part_begin = str.split("->")[0]
        part_end = str.split("->")[1]
        FIRST[part_begin] = ""
        FOLLOW[part_begin] = "#"


###求first集 中第第一部分针对 ->  直接推出第一个字符为终结符 部分
def getFirst():
    for str in grammars:
        part_begin = str.split("->")[0]
        part_end = str.split("->")[1]
        if not part_end[0].isupper():
            FIRST[part_begin] = FIRST.get(part_begin) + part_end[0]

##求first第二部分 针对 A -> B型  把B的first集加到A 的first集合中
def getFirst_2():
    for str in grammars:
        part_begin = ''
        part_end = ''
        part_begin += str.split('->')[0]
        part_end += str.split('->')[1]
        ##如果型如A ->B 则把B的first集加到A 的first集中去
        if part_end[0].isupper():
            FIRST[part_begin] = FIRST.get(part_begin) + FIRST.get(part_end[0])


def   getFisrt_3():
    while(1):
        test = FIRST
        getFirst_2()
        ##去除重复项
        for i , j  in FIRST.items():
            temp = ""
            for word in list(set(j)):
                temp += word
            FIRST[i] = temp
        if test == FIRST:
            break


def   getFOLLOW_3():
    while(1):
        test = FOLLOW
        getFollow()
        ##去除重复项
        for i , j  in FOLLOW.items():
            temp = ""
            for word in list(set(j)):
                temp += word
            FOLLOW[i] = temp
        if test == FOLLOW:
            break

##计算follow集的第一部分，先计算 S -> A b 类型的
def getFollow():
    for str in grammars:
        part_begin = str.split("->")[0]
        part_end = str.split("->")[1]
        ##如果是 S->a 直接推出终结符 则 continue
        if len(part_end) == 1:
            continue
        ##否则执行下面的操作
        else:
            #将->后面的分开再倒序
            temp = []
            for i in part_end:
                temp.append(i)
            temp.reverse()
            #如果非终结符在句型的末端则把"#" 加入进去
            if temp[0].isupper() :
                FOLLOW[temp[0] ]= FOLLOW.get(temp[0]) + FOLLOW.get(part_begin)
                temp1 = temp[0]
                for i in temp[1:]:
                    if not i.isupper():
                        temp1 = i
                    else:
                        if temp1.isupper():
                            FOLLOW[i] = FOLLOW.get(i) + FIRST.get(temp1).replace("ε","")
                        if ('ε' in FIRST.get(temp1)):
                            FOLLOW[i] = FOLLOW.get(i) + FOLLOW.get(part_begin)
                        else:
                            FOLLOW[i] = FOLLOW.get(i) + temp1
                        temp1 = i
            # 如果终结符在句型的末端
            else:
                temp1 = temp[0]
                for i in temp[1:]:
                    if not i.isupper():
                        temp1 = i
                    else:
                        if temp1.isupper():
                            FOLLOW[i] = FOLLOW.get(i) + FIRST.get(temp1)
                        else:
                            FOLLOW[i] = FOLLOW.get(i) + temp1
                        temp1 = i

initail()
getFirst()
getFisrt_3()
getFisrt_3()
#print(  FIRST )
getFOLLOW_3()
getFOLLOW_3()
#print(FOLLOW)

for i ,j in FIRST.items() :
    str = j[0]
    for temp in j[1:]:
        str = str+ ',' +temp
    print("FIRST("+ i + ")" + " = {"+str+"}")

for i ,j in FOLLOW.items():
    str = j[0]
    for temp in j[1:]:
        str = str + ',' + temp
    print("FOLLOW("+ i + ")" + " = {"+str+"}")
