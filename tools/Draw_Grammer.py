from prettytable import PrettyTable


def draw_grammer(grammer, vn,descrpition):
    advanced_grammar = PrettyTable(['编号', '箭头左边', '箭头右边', '产生式'])  # 利用prettytable来渲染出新的消去左递归的文法
    idx = 1
    for i in vn:
        for j in grammer[i]:
            advanced_grammar.add_row([idx, i, j, i + '->' + j])
            # only_grammer.append(i + '->' + j)
            idx += 1
    print('\n\n--------- '+descrpition+' ----------\n', advanced_grammar)
