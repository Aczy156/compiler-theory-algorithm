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

        """ 文法归一化 """
        propressed_table = PrettyTable(['编号', '箭头左边', '箭头右边', '产生式'])
        propressed_table.add_row([1, 'S', 'E', 'S->E'])
        idx = 2
        for l, r in result.items():
            for p in r:
                propressed_table.add_row([idx, l, p, l + '->' + p])
                idx += 1
        print('\n--------- 经过归一化后的文法 ----------\n', propressed_table)
        result['S'] = {'#{0}#'.format(first_left)}
        return [(l, p) for l, r in result.items() for p in r]

    def compute_firstvt(g):
        """输入一个算符文法的语法规则，输出所有非终结符的 FIRSTVT 集合"""
        result = defaultdict(set)

        # 添加由文法规则本身得到的集合
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

        # 添加由文法规则本身得到的集合
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
        """ 算符文法的语法规则、非终结符的FIRSTVT、LASTVT集合 填入算符优先分析表,按照·= ·> <· 的顺序"""
        vn = {c for left, right in grammar
              for c in right
              if not c.isupper()}
        result = {k: {k: '  ' for k in vn} for k in vn}

        for left, right in grammar:  # 利用grammer即i 和 i+2 位置上的来计算 '·='
            for i in range(len(right) - 1):
                if right[i].isupper():
                    pass
                elif not right[i + 1].isupper():
                    result[right[i]][right[i + 1]] = '·='
                elif i + 2 < len(right):
                    result[right[i]][right[i + 2]] = '·='

        for left, right in grammar:  # 利用firstvt来计算 '<·'
            for i in range(len(right) - 1):
                if right[i].isupper() or not right[i + 1].isupper():
                    continue
                a = right[i]
                for b in firstvt[right[i + 1]]:
                    if result[a][b] != '<·' and result[a][b] != '  ':
                        return False
                    result[a][b] = '<·'

        for left, right in grammar:  # 利用lastvt来计算 '<·'
            for i in range(len(right) - 1):
                if not right[i].isupper():
                    continue
                b = right[i + 1]
                for a in lastvt[right[i]]:
                    if result[a][b] != '·>' and result[a][b] != '  ':
                        return False
                    result[a][b] = '·>'
        # print(result)
        return result


def solve(grammar, prior_table, sentence):
    """ 算法有限分析实现：结合算符有限表prior_table 和文法grammer 来检测句子goal_str"""

    def update_states(states, new_states):
        for state, seq in new_states.items():
            if state not in states:
                pass
            elif len(seq) < len(states[state]):
                pass
            else:
                continue
            states[state] = seq

    def reduce_single(grammar, states):
        found_states = list(states.keys())
        for state in found_states:
            lastnt = state[-1]
            for left, right in grammar:
                if right != lastnt:
                    continue
                new_state = state[:-1] + left
                if new_state in found_states:
                    continue
                states[new_state] = states[state] + \
                                    [(state, '{0}->{1}'.format(left, right))]
                found_states.append(new_state)

    def reduce_(grammar, states, c):
        new_states = {}
        for state, seq in states.items():
            add_to_new = False

            if len(state) < 1:
                add_to_new = True
            elif not state[-1].isupper():
                if state[-1] not in prior_table:
                    return {}
                if prior_table[state[-1]][c] in ['<·', '·=']:
                    add_to_new = True
            elif len(state) < 2:
                add_to_new = True
            elif state[-2] not in prior_table:
                return {}
            elif prior_table[state[-2]][c] in ['<·', '·=']:
                add_to_new = True

            # 如果不需要归约直接添加
            if add_to_new:
                update_states(new_states, {
                    state + c: seq + [(state, None)]})
                continue

            # 进行归约
            for left, right in grammar:
                if not state.endswith(right):
                    continue
                states_to_reduce = {
                    state[:-len(right)] + left:
                        seq + [(state, '{0}->{1}'.format(left, right))]
                }
                reduce_single(grammar, states_to_reduce)
                update_states(new_states,
                              reduce_(grammar, states_to_reduce, c))

        return new_states

    states = {'': []}
    sentence = '#{0}#'.format(sentence)
    for i, c in enumerate(sentence):
        states = reduce_(grammar, states, c)
        if not states:
            return False, sentence[:i]

    # 寻找最短归约路径
    result = None
    for seq in states.values():
        if not result or len(seq) < len(result):
            # print('seq == ', seq)
            result = seq

    return True, result


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
            print('\n--------- 该文法的算符有限分析表为 ----------\n\n   |  ' + ' |  '.join(vt))
            for c in vt:
                print('---------------------------------------\n {0} | '.format(c) +
                      ' | '.join(prior_table[c][c2] for c2 in vt))

        while True:
            goal_str = str(input('请输入字符串(exit跳出循环):'))
            if goal_str == 'exit':
                break
            else:
                analysis_process_prettytable = PrettyTable(['编号', '栈', '符号串', '动作'])
                result, steps = solve(grammar=grammar, prior_table=prior_table, sentence=goal_str)
                if not result:
                    print('分析失败，该输入串不是一个句子')
                else:
                    print('分析成功')
                    left = '#{0}#'.format(goal_str)
                    width = len(left)
                    count = len(steps)
                    step_width = len(str((count))) + 1
                    for i, (_, act), (cur, _) in zip(range(count), steps, steps[1:]):
                        if not act:
                            left = left[1:]
                            act = '移进 '
                        else:
                            act = '规归 ' + act
                        # print(i,' ~~~ ', cur,' ~~~ ', left,' ~~~ ', act)
                        analysis_process_prettytable.add_row([i, cur, left, act])
                    print(analysis_process_prettytable)
