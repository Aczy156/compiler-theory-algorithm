from prettytable import PrettyTable
import re


class LL1_analysis:
    def __init__(self, Gram):
        self.ter, self.nonter, self.analysis_table, self.stack_str = self.load_grammer_and_init_stack_and_ptr(g=Gram)
        self.ptr = 0

    def load_grammer_and_init_stack_and_ptr(self, g):
        """ 读取文法并解析 """
        """ 首先输出原文法 """
        origin_grammar = PrettyTable(['编号', '箭头左边', '箭头右边', '产生式'])
        idx = 1
        left_recursion_list = []
        origin_list = []
        for line in re.split('\n', g):
            # 清楚空格
            line = "".join([i for i in line if i not in ['', ' ']])
            if '->' in line:
                for i in line.split('->')[1].split('|'):
                    if line.split('->')[0] == i[0] and line.split('->')[0] not in left_recursion_list:
                        left_recursion_list.append(line.split('->')[0])
                    origin_grammar.add_row([idx, line.split('->')[0], i, line.split('->')[0] + '->' + i])
                    origin_list.append([line.split('->')[0], i, line.split('->')[0] + '->' + i])
                    idx += 1
        print(origin_grammar)
        """ 然后判断是否有左递归并消除左递归 """
        advanced_grammar = PrettyTable(['编号', '箭头左边', '箭头右边', '产生式'])
        idx = 1
        if len(left_recursion_list) > 0:
            print('该文法存在左递归!!!      且该文法中存在左递归的非终结符为', end=' ')
            print([i for i in left_recursion_list])
            # 消除左递归
            for lr in left_recursion_list:
                for r in [i[1] for i in origin_list if i[0] == lr]:
                    if r[0] == lr:
                        advanced_grammar.add_row(
                            [idx, lr, r[len(r) - 1] + lr.lower(), lr + '->' + r[len(r) - 1] + lr.lower()])
                        advanced_grammar.add_row([idx + 1, lr.lower(), r[1:len(r)], lr.lower() + '->' + r[1:len(r)]])
                        idx += 2
                    else:
                        advanced_grammar.add_row([idx, lr, r, lr + '->' + r])
                        idx += 1
            for i in origin_list:
                if i[0] not in left_recursion_list:
                    advanced_grammar.add_row([idx, i[0], i[1], i[2]])
                    idx += 1
            print('消除左递归之后的文法为')
            print(advanced_grammar)
        else:
            print('该文法不存在左递归!!!')
            return

        # TODO 对输入进来的文法进行解析 (当前先把数据默认解析好了)
        return 'i+*()#', 'EDTSF', [
            [' ', 'i', '+', '*', '(', ')', '#'],
            ['E', 'TD', None, None, 'TD', None, None],
            ['D', None, '+TD', None, None, 'ε', 'ε'],
            ['T', 'FS', None, None, 'FS', None, None],
            ['S', None, 'ε', '*FS', None, 'ε', 'ε'],
            ['F', 'i', None, None, '(E)', None, None],
        ], '#E'

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
    grammar = str(open("grammer.txt").read())
    ll1_analysis = LL1_analysis(Gram=grammar)
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
