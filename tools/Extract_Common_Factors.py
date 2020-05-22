import random


class ExtractCommonFactors:
    def __init__(self, grammer, vn):
        self.grammer = grammer
        self.vn = vn

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

    def get_lcp_res(self, key): #获得每个拥有公共前缀的元素下标
        """ 获得LCP公共前缀的索引 """
        res = {}
        rules = self.grammer[key]
        for i in range(len(rules)):
            for j in range(i+1, len(rules)):
                temp = self.LCP(i,j,rules)
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
                    if temp not in self.vn:
                        ch = temp
                        break
                self.vn.append(ch)
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
        return self.grammer, self.vn
