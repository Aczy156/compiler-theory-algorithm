from tools.Eliminate_Left_Recursion import EliminateLeftRecursion


class recDesc_analysis:
    def __init__(self, file_name):

        self.file_object = file_name  # 获取句柄
        self.grammer = {}
        self.ac_set = []
        self.string = ""  # 测试字符串
        self.p = 0  # 字符串指针
        self.replace = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        for line in self.file_object.readlines():

            div_list = line.replace(' ', '').strip('\n').split('->')
            if div_list[0] not in self.grammer.keys():
                self.grammer[div_list[0]] = []
            self.grammer[div_list[0]].append(div_list[1])

            for ch in line:
                if ch.isupper() and ch not in self.ac_set:
                    self.ac_set.append(ch)

    def LCP(self, i, j, rules):  # 获取的最长公共前缀
        """ LCP 获取两个字符串之间最长公共前缀 """
        strs = [rules[i], rules[j]]
        res = ''
        for each in zip(*strs):
            if len(set(each)) == 1:
                res += each[0]
            else:
                return res
        return res

    # 获得最长公共前缀的元素的索引
    def get_lcp_res(self, key):  # 获得每个拥有公共前缀的元素下标
        """ 利用字典存放 获取到的所有的非终结符对应的产生式的所有右半部分的推到的部分的共同前缀 """
        res = {}
        rules = self.grammer[key]
        for i in range(len(rules)):
            for j in range(i + 1, len(rules)):
                temp = self.LCP(i, j, rules)
                if temp not in res.keys():
                    res[temp] = set()
                res[temp].add(i)
                res[temp].add(j)
        if '' in res.keys():
            res.pop('')
        return res

    # 消去公因子
    def remove_common_factor(self):
        """ 消去公因子 """
        keys = list(self.grammer.keys())  # 备份一份没有修改过的grammer的key
        for key in keys:
            while (True):
                res = self.get_lcp_res(key)
                if res == {}:  # 不断迭代，直到没有公共前缀
                    break
                dels = []  # 存储需要删除的符号串
                lcp = list(res.keys())[0]  # 策略：每次取一个公共前缀
                ch = ''

                for temp in self.replace:
                    if temp not in self.ac_set:
                        ch = temp
                        break

                self.ac_set.append(ch)
                for i in res[lcp]:  # res[lcp]存储的要消除公共因子的元素下标
                    string = self.grammer[key][i]
                    dels.append(string)
                    string = string.lstrip(lcp)
                    if string == '':
                        string += 'ε'
                    if ch not in self.grammer.keys():
                        self.grammer[ch] = []
                    self.grammer[ch].append(string)  # 加到新的产生式里面
                for string in dels:  # 从原来的产生式里面删除
                    self.grammer[key].remove(string)
                self.grammer[key].append(lcp + ch)
        return self.grammer, self.ac_set

    def match(self, ch):
        """ 递归下降进行匹配 """
        for i in range(len(self.grammer[ch])):
            rule = self.grammer[ch][i]
            print(i, '--->>>', rule)
            record_p = self.p  # 记录指针位置，方便回溯
            flag = True
            for item in rule:
                if item in self.ac_set:
                    flag = self.match(item)  # 如果碰到了非终结符，直接递归非终结符的子程序
                    if flag == 0: break
                elif self.p < len(self.string) and item == self.string[self.p]:
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

    def output(self, grammer):
        res = []
        for key in grammer.keys():
            for item in grammer[key]:
                res.append(key + '->' + item)
        for item in res:
            print(item)

    def run(self):
        print('～～～～', self.grammer, '+++++++', self.ac_set)
        # 消除左递归
        eliminate_left_recursion = EliminateLeftRecursion(grammer=self.grammer
                                                          , nonter=self.ac_set)
        self.grammer, self.ac_set = eliminate_left_recursion.remove_left_recursion()
        print('==========', self.grammer, '+++++++', self.ac_set)
        # 提取公因子
        self.grammer, self.ac_set = self.remove_common_factor()
        print('-----------------', self.grammer, '+++++++', self.ac_set)
        print('grammer after processing:')
        self.output(self.grammer)
        while (True):
            self.string = input('输入测试字符串(输入exit则结束):')
            self.p = 0
            if self.string == 'exit':
                break
            flag = (self.match(self.ac_set[0]) & (self.p == len(self.string)))  # 必须要遍历完测试字符串
            if flag:
                print(self.string + ' 分析成功')
            else:
                print(self.string + ' 分析失败')


file_object = open('grammer_for_ll1_and_RD.txt')
RDP = recDesc_analysis(file_object)
RDP.run()
