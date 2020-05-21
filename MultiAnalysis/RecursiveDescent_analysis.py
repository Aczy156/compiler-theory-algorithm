from tools.Eliminate_Left_Recursion import EliminateLeftRecursion
from tools.Extract_Common_Factors import ExtractCommonFactors
import re
import tools.Draw_Grammer as draw_grammer


class recDesc_analysis:
    def __init__(self, file):
        self.grammer = {}
        self.vn = []
        self.goal_str = ""  # 测试字符串
        self.p = 0  # 字符串指针
        for line in file.readlines():

            div_list = line.replace(' ', '').strip('\n').split('->')
            if div_list[0] not in self.grammer.keys():
                self.grammer[div_list[0]] = []
            self.grammer[div_list[0]].append(div_list[1])

            for ch in line:
                if ch.isupper() and ch not in self.vn:
                    self.vn.append(ch)

    def match(self, ch):
        """ 递归下降进行匹配，通过模拟所有的非终结符的子程序模块 """
        for i in range(len(self.grammer[ch])):
            rule = self.grammer[ch][i]
            # print(i, '--->>>', rule)
            record_p = self.p  # 记录指针位置，方便回溯
            flag = True
            for item in rule:
                if item in self.vn:
                    flag = self.match(item)  # 如果碰到了非终结符，直接递归非终结符的子程序
                    if flag == 0: break
                elif self.p < len(self.goal_str) and item == self.goal_str[self.p]:
                    self.p += 1
                elif item == 'ε':  # 如果rule中所有非ε都已经遍历，就遍历ε
                    break
                else:
                    flag = False
                    break
            if flag == 0:
                self.p = record_p
                continue
            else:
                return True
        return False

    def solve(self):
        """ 文法字典预处理 """
        for i in self.grammer:
            self.grammer[i] = str(self.grammer[i][0]).split('|')
        # print('==========', self.grammer, '+++++++', self.vn)
        draw_grammer.draw_grammer(grammer=self.grammer, vn=self.vn, descrpition='原始文法')  # 打印文法

        """ 消除左递归 """
        eliminate_left_recursion = EliminateLeftRecursion(grammer=self.grammer, vn=self.vn)
        self.grammer, self.vn = eliminate_left_recursion.remove_left_recursion()
        # print('==========', self.grammer, '+++++++', self.vn)
        draw_grammer.draw_grammer(grammer=self.grammer, vn=self.vn, descrpition='消除左递归之后的文法')  # 打印文法

        """ 提取公因子 """
        extractcommonfactors = ExtractCommonFactors(grammer=self.grammer, vn=self.vn)
        self.grammer, self.vn = extractcommonfactors.remove_common_factor()
        # print('==========', self.grammer, '+++++++', self.vn)
        draw_grammer.draw_grammer(grammer=self.grammer, vn=self.vn, descrpition='提取公因子之后的文法')  # 打印文法

        """ 递归下降分析 """
        while True:
            self.goal_str = input('请输入字符串(exit跳出循环):')
            self.p = 0
            if self.goal_str == 'exit':
                break
            flag = (self.match(self.vn[0]) & (self.p == len(self.goal_str)))  # 必须要遍历完测试字符串
            if flag:
                print(self.goal_str + ' 分析成功')
            else:
                print(self.goal_str + ' 分析失败')


if __name__ == '__main__':
    file_object = open('./data/grammer_for_ll1_and_RD.txt')
    RDP = recDesc_analysis(file_object)
    RDP.solve()
