from collections import defaultdict
import re
from prettytable import PrettyTable


class OF_analysis:
    # def __init__(self, Gram):
    #     self.ter, self.nonter, self.analysis_table, self.stack_str = self.load_grammer_and_init_stack_and_ptr(g=Gram)

    def grammar_preprocess(g):
        """ 文法预处理 """
        result = defaultdict(set)
        first_left = ''

        # 读取语法规则
        for line in re.split('\n', g):
            line = re.compile(r'\s+').sub('', line)
            m = re.compile(r'([A-Z])->(.+)').match(line)
            if not m:
                break
            # 获取左部和右部
            left = m.group(1)
            if not first_left:
                first_left = left
            right = m.group(2)
            # 判断是否为算符文法
            if re.compile(r'[A-Z]{2,}').search(right):
                return False
            # 切割右部并将右部添加到结果集
            right = right.split('|')
            result[left] |= set(right)

        # 经过归一化的数据 添加辅助语法规则
        propressed_table = PrettyTable(['编号', '箭头左边', '箭头右边', '产生式'])
        propressed_table.add_row([1, 'S', 'E', 'S->E'])
        idx = 2
        for l, r in result.items():
            for p in r:
                propressed_table.add_row([idx, l, p, l + '->' + p])
                idx += 1

        print('\n--------- 经过归一化后的文法 ----------\n', propressed_table)
        result['S'] = {'#{0}#'.format(first_left)}

        # print([(l, p) for l, r in result.items() for p in r])
        return [(l, p) for l, r in result.items() for p in r]

    def compute_firstvt(g):
        """输入一个算符文法的语法规则，输出所有非终结符的 FIRSTVT 集合"""

        result = defaultdict(set)

        # 第一轮添加由文法规则本身得到的集合
        for left, right in g:
            new_set = result[left]
            if len(right) >= 1 and not right[0].isupper():
                new_set.add(right[0])
            elif len(right) >= 2:
                new_set.add(right[1])

        # 迭代添加其他集合
        updated = True
        while updated:
            updated = False
            for left, right in g:
                new_set = set(result[left])
                if len(right) >= 1 and right[0].isupper():
                    new_set |= result[right[0]]
                if len(new_set) > len(result[left]):
                    result[left] = new_set
                    updated = True

        return dict(result)

    def compute_lastvt(g):
        """输入一个算符文法的语法规则，输出所有非终结符的 LASTVT 集合"""

        result = defaultdict(set)

        # 第一轮添加由文法规则本身得到的集合
        for left, right in g:
            new_set = result[left]
            if len(right) >= 1 and not right[-1].isupper():
                new_set.add(right[-1])
            elif len(right) >= 2:
                new_set.add(right[-2])

        # 迭代添加其他集合
        updated = True
        while updated:
            updated = False
            for left, right in g:
                new_set = set(result[left])
                if len(right) >= 1 and right[-1].isupper():
                    new_set |= result[right[-1]]
                if len(new_set) > len(result[left]):
                    result[left] = new_set
                    updated = True

        return dict(result)

    def compute_prior(grammar, firstvt, lastvt):
        """输入算符文法的语法规则、非终结符的 FIRSTVT 和 LASTVT 集合，
        输出该算符文法的优先表。
        如果输入的文法不是一个算符优先文法，返回 False。
        """

        vn = {c for left, right in grammar
              for c in right
              if not c.isupper()}
        result = {k: {k: ' ' for k in vn} for k in vn}

        # 根据语法规则计算“=”关系
        for left, right in grammar:
            for i in range(len(right) - 1):
                if right[i].isupper():
                    pass
                elif not right[i + 1].isupper():
                    result[right[i]][right[i + 1]] = '='
                elif i + 2 < len(right):
                    result[right[i]][right[i + 2]] = '='

        # 根据 FIRSTVT 计算“<”关系
        for left, right in grammar:
            for i in range(len(right) - 1):
                if right[i].isupper() or not right[i + 1].isupper():
                    continue
                a = right[i]
                for b in firstvt[right[i + 1]]:
                    if result[a][b] != '<' and result[a][b] != ' ':
                        return False
                    result[a][b] = '<'

        # 根据 LASTVT 计算“>”关系
        for left, right in grammar:
            for i in range(len(right) - 1):
                if not right[i].isupper():
                    continue
                b = right[i + 1]
                for a in lastvt[right[i]]:
                    if result[a][b] != '>' and result[a][b] != ' ':
                        return False
                    result[a][b] = '>'

        return result


if __name__ == '__main__':
    """ main 1输入文法 2输入要分析的字符串 """
    # grammer = str(open('./data/grammer_for_OF.txt').read())
    g = str(open('grammer_for_OF.txt').read())
    grammar = OF_analysis.grammar_preprocess(g=g)
    if not grammar:
        print('不是一个算符文法')
    else:
        vn = list({left for left, right in grammar})
        vt = list({c for left, right in grammar
                   for c in right
                   if not c.isupper()})

        # 计算 FIRSTVT 并输出
        firstvt = OF_analysis.compute_firstvt(grammar)
        print('\n--------- 各个非终结符的FIRSTVT集为 ----------\n')
        for left in vn:
            print('FIRSTVT({0}) = {{{1}}}'.format(left,
                                                  ', '.join("'{0}'".format(c) for c in firstvt[left])))

        # 计算 LASTVT 并输出
        lastvt = OF_analysis.compute_lastvt(grammar)
        print('\n--------- 各个非终结符的LASTVT集为 ----------\n')
        for left in vn:
            print('LASTVT({0}) = {{{1}}}'.format(left,
                                                 ', '.join("'{0}'".format(c) for c in lastvt[left])))

        # 计算优先表并输出
        prior_table = OF_analysis.compute_prior(grammar, firstvt, lastvt)
        if not prior_table:
            print('不是一个算符优先文法')
        else:
            # print(prior_table)
            # print('')
            # print('优先表：')
            # print('    ' + '  '.join(vt))
            for c in vt:
                print(' {0}  '.format(c) +
                      '  '.join(prior_table[c][c2] for c2 in vt))
            print('')
