import copy
import random


class recDescParser:
    def __init__(self, file_name):

        self.file_object = file_name  # 获取句柄
        self.grammer = {}
        self.ac_set = []
        self.string = ""  # 测试字符串
        self.p = 0  # 字符串指针
        for line in self.file_object.readlines():

            div_list = line.replace(' ', '').strip('\n').split('::')
            if div_list[0] not in self.grammer.keys():
                self.grammer[div_list[0]] = []
            self.grammer[div_list[0]].append(div_list[1])

            for ch in line:
                if ch.isupper() and ch not in self.ac_set:
                    self.ac_set.append(ch)

    def convert(self, ch_i, ch_j, grammer):

        rules = copy.deepcopy(grammer)
        for key in grammer.keys():
            for item_i in grammer[key]:
                if ch_i == key and ch_j == item_i[0]:
                    rules[key].remove(item_i)
                    for item_j in grammer[ch_j]:
                        rules[key].append(item_j + item_i[1:])
        return rules

    def clean_direct_recur(self, ch_i, grammer, new_ac_set):
        ch = ''
        flag = 0
        rules = copy.deepcopy(grammer)

        while (True):
            temp = chr(random.randint(65, 90))
            if temp not in new_ac_set:
                ch = temp
                break

        for key in grammer.keys():
            for item_i in grammer[key]:
                if ch_i == key and ch_i == item_i[0]:
                    flag = 1
                    if ch not in rules.keys():
                        rules[ch] = []

                    rules[ch].append(item_i[1:] + ch)
                    rules[key].remove(item_i)

        if flag == 0:  # 不存在左递归，不用消去
            return rules, new_ac_set

        for key in grammer.keys():
            for item_i in grammer[key]:
                if ch_i == key and ch_i != item_i[0]:
                    if ch not in rules.keys():
                        rules[ch] = []
                    rules[ch_i].append(item_i + ch)
                    rules[key].remove(item_i)
        rules[ch].append('#')  # 空输入在最后，不会影响递归下降
        new_ac_set.append(ch)
        print(new_ac_set)
        print(rules)
        return rules, new_ac_set

    def remove_left_recursion(self):
        new_grammer = copy.deepcopy(self.grammer)
        new_ac_set = copy.deepcopy(self.ac_set)

        for i in range(len(self.ac_set)):
            for j in range(0, i):
                new_grammer = self.convert(self.ac_set[i], self.ac_set[j], new_grammer)
            new_grammer, new_ac_set = self.clean_direct_recur(self.ac_set[i], new_grammer, new_ac_set)
        return new_grammer, new_ac_set

    def LCP(self, i, j, rules):  # 获取两个字符串之间的最长公共前缀
        strs = [rules[i], rules[j]]
        res = ''
        for each in zip(*strs):
            if len(set(each)) == 1:
                res += each[0]
            else:
                return res
        return res

    def get_lcp_res(self, key):  # 获得每个拥有公共前缀的元素下标
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

    def remove_common_factor(self):
        keys = list(self.grammer.keys())  # 事先保存好没有修改过的grammer_key
        for key in keys:
            while (True):
                res = self.get_lcp_res(key)
                if (res == {}):  # 不断迭代，直到没有公共前缀
                    break
                dels = []  # 存储需要删除的符号串
                lcp = list(res.keys())[0]  # 策略：每次取一个公共前缀
                ch = ''
                while (True):
                    temp = chr(random.randint(65, 90))
                    if temp not in self.ac_set:
                        ch = temp
                        break
                self.ac_set.append(ch)
                for i in res[lcp]:  # res[lcp]存储的要消除公共因子的元素下标
                    string = self.grammer[key][i]
                    dels.append(string)
                    string = string.lstrip(lcp)
                    if string == '':
                        string += '#'
                    if ch not in self.grammer.keys():
                        self.grammer[ch] = []
                    self.grammer[ch].append(string)  # 加到新的产生式里面
                for string in dels:  # 从原来的产生式里面删除
                    self.grammer[key].remove(string)
                self.grammer[key].append(lcp + ch)
        return self.grammer, self.ac_set

    def match(self, ch):
        for i in range(len(self.grammer[ch])):
            rule = self.grammer[ch][i]
            record_p = self.p  # 记录指针位置，方便回溯
            flag = 1
            for item in rule:
                if (item in self.ac_set):
                    flag = self.match(item)
                    if (flag == 0): break
                elif (self.p < len(self.string) and item == self.string[self.p]):
                    self.p += 1
                elif (item == '#'):  # 每个rules集的最后是'#'rule，所以在其他规则不行时，才用这条规则
                    break
                else:
                    flag = 0
                    break
            if flag == 0:
                self.p = record_p
                continue
            else:
                return 1
        return 0

    def output(self, grammer):
        res = []
        for key in grammer.keys():
            for item in grammer[key]:
                res.append(key + '::' + item)
        for item in res:
            print(item)

    def run(self):
        print('～～～～', self.grammer, '+++++++', self.ac_set)
        # 消除左递归
        self.grammer, self.ac_set = self.remove_left_recursion()
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
            if (flag):
                print(self.string + ' is Yes')
            else:
                print(self.string + ' is No')


file_object = open('grammer.txt')
RDP = recDescParser(file_object)
RDP.run()
