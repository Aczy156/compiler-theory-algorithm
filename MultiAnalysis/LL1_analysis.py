from prettytable import PrettyTable
import re
from tools.Eliminate_Left_Recursion import EliminateLeftRecursion
from tools.Extract_Common_Factors import ExtractCommonFactors
import tools.Draw_Grammer as draw_grammer


class LL1_analysis:
    def __init__(self, Gram):
        self.vt, self.vn, self.analysis_table, self.stack_str = self.init_all_(g=Gram)
        self.ptr = 0

    def init_all_(self, g):
        """ 读取文法并解析 """
        grammer_list = {}  # grammer 字典，对于特定的非终结符vn来来映射产生式
        vn_list = []  # 非终结符列表
        for line in re.split('\n', g):
            # 清楚空格
            line = "".join([i for i in line if i not in ['', ' ']])
            if '->' in line:
                if line.split('->')[0] not in vn_list:
                    vn_list.append(line.split('->')[0])
                for i in line.split('->')[1].split('|'):
                    if grammer_list.get(line.split('->')[0]) is None:
                        grammer_list[line.split('->')[0]] = []
                        grammer_list[line.split('->')[0]].append(i)
                    else:
                        grammer_list[line.split('->')[0]].append(i)  # 用于消除左递归的字典填充
        draw_grammer.draw_grammer(grammer=grammer_list, vn=vn_list, descrpition='在消除左递归之前的文法')  # 打印文法

        """ 消除左递归 """
        print('==========', grammer_list, '+++++++', vn_list)
        eliminate_left_recursion = EliminateLeftRecursion(grammer=grammer_list, vn=vn_list)
        new_grammer, new_vn = eliminate_left_recursion.remove_left_recursion()
        draw_grammer.draw_grammer(grammer=new_grammer, vn=new_vn, descrpition='消除左递归之后的文法')  # 打印文法

        """ 提取公因子 """
        extractcommonfactors = ExtractCommonFactors(grammer=new_grammer, vn=new_vn)
        new_grammer, new_vn = extractcommonfactors.remove_common_factor()
        # print('==========', new_grammer, '+++++++', new_vn)
        draw_grammer.draw_grammer(grammer=new_grammer, vn=new_vn, descrpition='提取公因子之后的文法')  # 打印文法

        """ 获取终结符、打印终结符和非终结符集合 """
        only_grammer = []
        new_vt = []
        for i in new_vn:
            for j in new_grammer[i]:
                only_grammer.append(i + '->' + j)
                for t in j:  # 获取当前的所有的终结符
                    if t not in new_vt and t not in new_vn and t != 'ε':
                        new_vt.append(t)
        new_vt.append('#')
        print('\n\n--------- 消除文法左递归的文法的非终结符为 ----------\n',
              new_vn,
              '\n\n--------- 消除文法左递归的文法的终结符为 ----------\n', new_vt)

        """ 获取FIRST集合和FOLLOW集合并输出 """
        FIRST, FOLLOW = self.get_first_and_follow_set(grammars=only_grammer, vn=new_vn)
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

        """ 利用first集和follow集来产生分析表 """
        analysis_table = [[None] * (1 + len(new_vt)) for row in range(1 + len(new_vn))]
        analysis_table[0][0] = ' '
        for i in range(len(new_vt)):
            analysis_table[0][i + 1] = new_vt[i]
        for i in range(len(new_vn)):
            analysis_table[i + 1][0] = new_vn[i]
            for t in new_grammer[new_vn[i]]:  # 遍历该文法的所有产生式
                if t == 'ε':  # 如果是ε 对应在follow(i)中填上产生式
                    for j in range(len(new_vt)):  # 遍历所有的终结符，并在对应的位置添加上对应的产生式子
                        if new_vt[j] in FOLLOW[new_vn[i]]:  # Follow 为当前的非终结符的follow集
                            analysis_table[i + 1][j + 1] = 'ε'
                else:
                    for j in range(len(new_vt)):
                        if new_vt[j] in FIRST[new_vn[i]]:
                            analysis_table[i + 1][j + 1] = t

        """ 格式化输出分析表 """
        # print(analysis_table)
        pretty_table_title = ['非终结符']
        for i in new_vt:
            pretty_table_title.append(i)
        analysis_pretty_table = PrettyTable(pretty_table_title)
        for i in range(len(analysis_table) - 1):
            analysis_pretty_table.add_row(analysis_table[i + 1])
        print('\n\n--------- 该文法对应的预测分析表为 ----------\n', analysis_pretty_table)

        """ 将所有预处理的数据返回 """
        return "".join(new_vt), "".join(new_vn), analysis_table, '#' + new_vn[0]

    def get_first_and_follow_set(self, grammars,vn):
        FIRST = {}
        FOLLOW = {}
        """ first集和follow集初始化 """
        for str in grammars: # 初始化first 集 和follow集合字典的键值对中的 值 为空
            part_begin = str.split("->")[0]
            part_end = str.split("->")[1]
            FIRST[part_begin] = ""
            FOLLOW[part_begin] = "#"

        """ 获取first集 """
        for str in grammars: # 求first集 中第第一部分针对 ->  直接推出第一个字符为终结符 部分
            part_begin = str.split("->")[0]
            part_end = str.split("->")[1]
            if not part_end[0].isupper():
                FIRST[part_begin] = FIRST.get(part_begin) + part_end[0]
        for i in range(len(vn)):
            while True:
                test = FIRST
                for str in grammars: # 求first第二部分 针对 A -> B型  把B的first集加到A 的first集合中
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
        for i in range(len(vn)):
            while True:
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

    """ LL1分析过程 """
    def LL1_analysis_solve(self, goal_str, ans_table):
        vt, vn, analysis_table, stack_str, ptr = self.vt, self.vn, self.analysis_table, self.stack_str, self.ptr
        while ptr >= 0 and ptr <= len(goal_str):
            stack_top = stack_str[len(stack_str) - 1]  # 获取栈顶
            goal_pos = goal_str[ptr]
            # print(stack_str, '  ', stack_top, '  ', goal_pos)
            if (stack_top not in vt and stack_top not in vn) or goal_pos not in vt:  # 非法输入的情况
                print('输入不合法')
                return
            elif stack_top == goal_pos:
                if stack_top == '#':  # 栈顶符号=当前输入符号=#
                    print('分析成功')
                    ans_table.add_row([stack_str, goal_str[ptr:len(goal_str)], '分析成功'])
                    return
                else:  # 栈顶符号=当前输入符号但是并不都等于#
                    # --printstat相等弹栈，指针前移
                    # print('栈顶符号=当前输入符号，指针前移')
                    ans_table.add_row([stack_str, goal_str[ptr:len(goal_str)], '栈顶符号=当前输入符号，指针前移'])
                    stack_str = stack_str[0:len(stack_str) - 1]  # 弹栈
                    ptr += 1
                    continue
            lookup_table = analysis_table[max(vn.find(stack_top), vt.find(stack_top)) + 1][
                max(vn.find(goal_pos), vt.find(goal_pos)) + 1]
            # print(stack_top, ' ~~~~~~~~~ ', goal_pos, ' ~~~~~~~~~ ', lookup_table)
            if lookup_table is not None:
                if lookup_table == 'ε':
                    # print('ε,弹栈')
                    ans_table.add_row([stack_str, goal_str[ptr:len(goal_str)], 'ε,弹栈'])
                    stack_str = stack_str[0:len(stack_str) - 1]  # 弹栈
                    continue
                else:
                    # print('存在对应的产生式并反向压栈')
                    ans_table.add_row([stack_str, goal_str[ptr:len(goal_str)], '存在对应的产生式并反向压栈'])
                    stack_str = stack_str[0:len(stack_str) - 1]  # 弹栈
                    lt_list = list(lookup_table)
                    lt_list.reverse()
                    stack_str += "".join(lt_list)
                    continue
            else:
                print('分析失败')
                return


if __name__ == '__main__':
    """ main 1输入文法 2输入要分析的字符串 """
    grammer = str(open('./data/grammer_for_ll1_and_RD.txt').read())
    ll1_analysis = LL1_analysis(Gram=grammer)
    while True:
        goal_str = str(input('请输入字符串(exit跳出循环):')) + '#'
        if goal_str == 'exit#':
            break
        else:
            ans_table = PrettyTable(['分析栈', '输入串', '操作'])
            ll1_analysis.LL1_analysis_solve(goal_str=goal_str, ans_table=ans_table)
            print(ans_table)




