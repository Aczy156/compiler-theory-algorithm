import re

# valid token
token_dict = {
    'int': 1, 'double': 1, 'string': 1, 'if': 1, 'else': 1, 'return': 1, 'main': 1, 'void': 1, 'while': 1, 'for': 1,
    'break': 1,
    '+': 4, '-': 4, '*': 4, '/': 4, '<': 4, '>': 4, '=': 4, '==': 4,
    ',': 5, ';': 5, '(': 5, ')': 5, '{': 5,
}

# invalid token
invalid_token = ['，', '；', '！', '（', '）']


def myprint(type, tk):
    """ 格式化输出 """
    print('(\'' + str(type) + '\',\'' + str(tk) + '\')')


def solve():
    # 加载文本 转换为token
    s = open("test2.txt").read()
    token = re.split('([;,\s&%\?\+\*;\-/_:,\(\)\t\000\r\n\0])', s)

    # token分割后的一些预处理
    # TODO 处理一些特殊情况 main{,for(){,if(){ while --解决
    data1 = []
    for i in token:
        if '){' in i or 'n{' in i:
            data1.append(i[0:len(i) - 1]);
            data1.append('{')
        else:
            data1.append(i)
    # 过滤
    data2 = [i for i in data1 if i not in ['', ' ', '\n']]

    # mapping 1key->2allnum->3str+num
    for i in data2:
        if token_dict.get(i) is not None:
            myprint(token_dict.get(i), i)
        elif i.isdigit():
            myprint(3, i)
        else:
            # TODO 对 前面的余下的一些进行单词判断，查看是否有错误
            myprint(2, i)


if __name__ == '__main__':
    solve()
