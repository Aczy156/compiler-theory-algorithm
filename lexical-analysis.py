import re

# valid token
token_dict = {
    'int': 1, 'if': 1, 'else': 1, 'return': 1, 'main': 1, 'void': 1, 'while': 1, 'for': 1, 'break': 1,
    '+': 4, '-': 4, '*': 4, '/': 4, '<': 4, '>': 4, '=': 4,
    ',': 5, ';': 5, '(': 5, ')': 5,
}

# invalid token
invalid_token = ['，', '；', '！', '（', '）']


def myprint(type, tk):
    print('(\'' + str(type) + '\',\'' + str(tk) + '\')')


def solve():
    # load text and transform to token
    s = open("test.txt").read()
    token = re.split('([;,\s&%\?=\+\*;\-/_:,\(\)\.\t\000\r\n\0])', s)
    ans = [i for i in token if i not in ['', ' ', '\n']]
    print()

    # mapping 1key->2allnum->3str+num
    for i in ans:
        if token_dict.get(i) is not None:
            myprint(token_dict.get(i), i)
        elif i.isdigit():
            myprint(3, i)
        else:
            myprint(2, i)


if __name__ == '__main__':
    solve()
