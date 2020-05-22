import copy


class EliminateLeftRecursion:
    def __init__(self, grammer, vn):
        self.grammer = grammer
        self.vn = vn
        # 非终结符中用于增添的可选择的大写字母
        self.replace = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                   'U', 'V', 'W', 'X', 'Y', 'Z']

    def remove_left_recursion(self):
        """ 消除左递归 """
        new_grammer = copy.deepcopy(self.grammer)
        new_ac_set = copy.deepcopy(self.vn)
        for i in range(len(self.vn)): # 利用两层循环来消除左递归
            for j in range(0, i):
                new_grammer = self.convert(self.vn[i], self.vn[j], new_grammer)
            new_grammer, new_ac_set = self.clean_direct_recur(self.vn[i], new_grammer, new_ac_set)
        return new_grammer, new_ac_set

    def convert(self, ch_i, ch_j, grammer):
        """ 对特定的字符进行转换 """
        rules = copy.deepcopy(grammer)  # 复制一份
        for key in grammer.keys():
            for item_i in grammer[key]:
                if ch_i == key and ch_j == item_i[0]:
                    rules[key].remove(item_i)
                    for item_j in grammer[ch_j]:
                        rules[key].append(item_j + item_i[1:])
        return rules

    def clean_direct_recur(self, ch_i, grammer, new_ac_set):
        """ 清除直接左递归 """
        ch = ''
        flag = 0
        rules = copy.deepcopy(grammer)

        for temp in self.replace: # 选择未被使用的非终结符
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
        rules[ch].append('ε')  # 空输入在最后，不会影响递归下降
        new_ac_set.append(ch)
        # print(new_ac_set)
        # print(rules)
        return rules, new_ac_set
