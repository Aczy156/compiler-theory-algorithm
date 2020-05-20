from prettytable import PrettyTable
import copy
import re
from Eliminate_Left_Recursion import EliminateLeftRecursion


class LL1_analysis:
    def __init__(self, Gram):
        self.ter, self.nonter, self.analysis_table, self.stack_str = self.load_grammer_and_init_stack_and_ptr(g=Gram)
        self.ptr = 0

    def load_grammer_and_init_stack_and_ptr(self, g):
        """ 读取文法并解析 """
        """ 首先输出原文法 """
        origin_grammar = PrettyTable(['编号', '箭头左边', '箭头右边', '产生式'])
        idx = 1
        left_recursion_list = []  # 存在左递归的非终结符
        origin_list = []  # 完整的grammer表格
        grammer_list = {}  # grammer 字典，对于特定的非终结符nonter来来映射产生式
        nonter_list = []  # 非终结符列表
        for line in re.split('\n', g):
            # 清楚空格
            line = "".join([i for i in line if i not in ['', ' ']])
            if '->' in line:
                if line.split('->')[0] not in nonter_list:
                    nonter_list.append(line.split('->')[0])
                for i in line.split('->')[1].split('|'):
                    if grammer_list.get(line.split('->')[0]) is None:
                        grammer_list[line.split('->')[0]] = []
                        grammer_list[line.split('->')[0]].append(i)
                    else:
                        grammer_list[line.split('->')[0]].append(i)  # 用于消除左递归的字典填充
                    origin_grammar.add_row(
                        [idx, line.split('->')[0], i, line.split('->')[0] + '->' + i])  # prettytable 填充
                    # origin_list.append([line.split('->')[0], i, line.split('->')[0] + '->' + i])
                    # grammer_list.append(line.split('->')[0] + '->' + i)
                    idx += 1

        print('\n--------- 在消除左递归之前的文法为 ----------\n', origin_grammar)
        # print('origin grammer :::::', grammer_list)
        # print('origin nonter  [[[[[[[[', nonter_list)

        """ 消除左递归 """
        eliminate_left_recursion = EliminateLeftRecursion(grammer=grammer_list, nonter=nonter_list)
        new_grammer, new_nonter = eliminate_left_recursion.remove_left_recursion()
        # print('new grammer ==== ', new_grammer)
        # print('new nonter ----------', new_nonter)
        advanced_grammar = PrettyTable(['编号', '箭头左边', '箭头右边', '产生式'])  # 利用prettytable来渲染出新的消去左递归的文法
        only_grammer = []
        idx = 1
        new_ter = []
        for i in new_nonter:
            for j in new_grammer[i]:
                advanced_grammar.add_row([idx, i, j, i + '->' + j])
                only_grammer.append(i + '->' + j)
                idx += 1
                for t in j:  # 获取当前的所有的终结符
                    if t not in new_ter and t not in new_nonter and t != 'ε':
                        new_ter.append(t)
        new_ter.append('#')
        print('\n\n--------- 消除左递归的文法为 ----------\n', advanced_grammar, '\n\n--------- 消除文法左递归的文法的非终结符为 ----------\n',
              new_nonter,
              '\n\n--------- 消除文法左递归的文法的终结符为 ----------\n', new_ter)

        """ 调用下面函数来产生FIRST集合和FOLLOW集合 """
        FIRST, FOLLOW = self.get_first_and_follow_set(only_grammer)
        # print(FIRST)
        # print(FOLLOW)
        print('\n\n--------- 文法的FIRST集为 ----------')
        for i, j in FIRST.items():
            str = j[0]
            for temp in j[1:]:
                str = str + ',' + temp
            print("FIRST(" + i + ")" + " = {" + str + "}")
        print('\n\n--------- 文法的FOLLOW集为 ----------')
        for i, j in FOLLOW.items():
            str = j[0]
            for temp in j[1:]:
                str = str + ',' + temp
            print("FOLLOW(" + i + ")" + " = {" + str + "}")

        # print('First集合 ～～～～', FIRST)
        # print('Follow集合 ～～～～', FOLLOW)
        """ 利用first集和follow集来产生分析表 """
        analysis_table = [[None] * (1 + len(new_ter)) for row in range(1 + len(new_nonter))]
        analysis_table[0][0] = ' '
        for i in range(len(new_ter)):
            analysis_table[0][i + 1] = new_ter[i]
        for i in range(len(new_nonter)):
            analysis_table[i + 1][0] = new_nonter[i]
            for t in new_grammer[new_nonter[i]]:  # 遍历该文法的所有产生式
                if t == 'ε':  # 如果是ε 对应在follow(i)中填上产生式
                    for j in range(len(new_ter)):  # 遍历所有的终结符，并在对应的位置添加上对应的产生式子
                        if new_ter[j] in FOLLOW[new_nonter[i]]:  # Follow 为当前的非终结符的follow集
                            analysis_table[i + 1][j + 1] = 'ε'
                else:
                    for j in range(len(new_ter)):
                        if new_ter[j] in FIRST[new_nonter[i]]:
                            analysis_table[i + 1][j + 1] = t

        # print(analysis_table)
        pretty_table_title = ['非终结符']
        for i in new_ter:
            pretty_table_title.append(i)
        analysis_pretty_table = PrettyTable(pretty_table_title)
        for i in range(len(analysis_table) - 1):
            analysis_pretty_table.add_row(analysis_table[i + 1])
        print('\n\n--------- 该文法对应的预测分析表为 ----------\n', analysis_pretty_table)

        # TODO 对输入进来的文法进行解析 (当前先把数据默认解析好了)
        return "".join(new_ter), "".join(new_nonter), analysis_table, '#' + new_nonter[0]

    def get_first_and_follow_set(self, grammars):
        FIRST = {}
        FOLLOW = {}
        # 初始化first 集 和follow集合字典的键值对中的 值 为空
        for str in grammars:
            part_begin = str.split("->")[0]
            part_end = str.split("->")[1]
            FIRST[part_begin] = ""
            FOLLOW[part_begin] = "#"
        """ 获取first集 """
        # 求first集 中第第一部分针对 ->  直接推出第一个字符为终结符 部分
        for str in grammars:
            part_begin = str.split("->")[0]
            part_end = str.split("->")[1]
            if not part_end[0].isupper():
                FIRST[part_begin] = FIRST.get(part_begin) + part_end[0]
        for i in range(2):
            while (1):
                test = FIRST

                # 求first第二部分 针对 A -> B型  把B的first集加到A 的first集合中
                for str in grammars:
                    part_begin = ''
                    part_end = ''
                    part_begin += str.split('->')[0]
                    part_end += str.split('->')[1]
                    ##如果型如A ->B 则把B的first集加到A 的first集中去
                    if part_end[0].isupper():
                        FIRST[part_begin] = FIRST.get(part_begin) + FIRST.get(part_end[0])

                # 去除重复项
                for i, j in FIRST.items():
                    temp = ""
                    for word in list(set(j)):
                        temp += word
                    FIRST[i] = temp
                if test == FIRST:
                    break

        """ 获取follow集合 """
        for i in range(2):
            while (1):
                test = FOLLOW

                # 计算follow集的第一部分，先计算 S -> A b 类型的
                for str in grammars:
                    part_begin = str.split("->")[0]
                    part_end = str.split("->")[1]
                    ##如果是 S->a 直接推出终结符 则 continue
                    if len(part_end) == 1:
                        continue
                    ##否则执行下面的操作
                    else:
                        # 将->后面的分开再倒序
                        temp = []
                        for i in part_end:
                            temp.append(i)
                        temp.reverse()
                        # 如果非终结符在句型的末端则把"#" 加入进去
                        if temp[0].isupper():
                            FOLLOW[temp[0]] = FOLLOW.get(temp[0]) + FOLLOW.get(part_begin)
                            temp1 = temp[0]
                            for i in temp[1:]:
                                if not i.isupper():
                                    temp1 = i
                                else:
                                    if temp1.isupper():
                                        FOLLOW[i] = FOLLOW.get(i) + FIRST.get(temp1).replace("ε", "")
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

                ##去除重复项
                for i, j in FOLLOW.items():
                    temp = ""
                    for word in list(set(j)):
                        temp += word
                    FOLLOW[i] = temp
                if test == FOLLOW:
                    break
        return FIRST, FOLLOW

    def LL1_analysis_solve(self, goal_str, ans_table):
        ter, nonter, analysis_table, stack_str, ptr = self.ter, self.nonter, self.analysis_table, self.stack_str, self.ptr
        """ LL1 analysis solution """
        while ptr >= 0 and ptr <= len(goal_str):
            stack_top = stack_str[len(stack_str) - 1]  # 获取栈顶
            goal_pos = goal_str[ptr]
            print(stack_str, '  ', stack_top, '  ', goal_pos)
            if (stack_top not in ter and stack_top not in nonter) or goal_pos not in ter:  # 非法输入的情况
                # --printstat不合法
                print('输入不合法')
                return
            elif stack_top == goal_pos:
                if stack_top == '#':  # 栈顶符号=当前输入符号=#
                    # --printstat成功
                    print('分析成功')
                    ans_table.add_row([stack_str, goal_str[ptr:len(goal_str)], '分析成功'])
                    return
                else:  # 栈顶符号=当前输入符号但是并不都等于#
                    # --printstat相等弹栈，指针前移
                    print('相等弹栈，指针前移')
                    ans_table.add_row([stack_str, goal_str[ptr:len(goal_str)], '相等弹栈，指针前移'])
                    stack_str = stack_str[0:len(stack_str) - 1]  # 弹栈
                    ptr += 1
                    continue
            lookup_table = analysis_table[max(nonter.find(stack_top), ter.find(stack_top)) + 1][
                max(nonter.find(goal_pos), ter.find(goal_pos)) + 1]
            print(stack_top, ' ~~~~~~~~~ ', goal_pos, ' ~~~~~~~~~ ', lookup_table)
            if lookup_table is not None:
                if lookup_table == 'ε':
                    # --printstat ε,弹栈
                    print('ε,弹栈')
                    ans_table.add_row([stack_str, goal_str[ptr:len(goal_str)], 'ε,弹栈'])
                    stack_str = stack_str[0:len(stack_str) - 1]  # 弹栈
                    continue
                else:
                    # --printstat 存在对应的产生式，就把产生式反向压栈
                    print('存在对应的产生式并反向压栈')
                    ans_table.add_row([stack_str, goal_str[ptr:len(goal_str)], '存在对应的产生式并反向压栈'])
                    stack_str = stack_str[0:len(stack_str) - 1]  # 弹栈
                    lt_list = list(lookup_table)
                    lt_list.reverse()
                    stack_str += "".join(lt_list)
                    continue
            else:
                # --printstat 找不到对应的产生式 ，error 退出
                print('分析失败，没有找到产生式子')
                return


if __name__ == '__main__':
    """ main 1输入文法 2输入要分析的字符串 """
    grammer = str(open("grammer.txt").read())
    ll1_analysis = LL1_analysis(Gram=grammer)
    goal_str = str(input())
    ans_table = PrettyTable(['分析栈', '输入串', '操作'])
    ll1_analysis.LL1_analysis_solve(goal_str=goal_str, ans_table=ans_table)

    # i+i*i#
    print(ans_table)

    # a = '123456'
    # idx = 3
    # print(a[idx])
    # print(a[idx:len(a)])
    # b = a[len(a)-1]
    # print(b)
    # a = a[1:len(a)]
    # print(a)
