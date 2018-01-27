# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup

# def math(string):
#     try:
#         str1 = string.replace(' ', '').strip()
#         # 正则匹配四则运算
#         re_math = '\(*\d+[+-/*]{1}\(*\d+\)*([+-/*]{1}\(*\d+\)*)*'
#         math_str = re.search(re_math, str1).group()
#         print(eval(math_str))
#     except Exception:
#         print('输入的四则运算表达式有误......')


def missing(words):
    try:
        len_list = []
        url = 'https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word={}'.format(words)
        req = requests.get(url)
        soup = BeautifulSoup(req.content.decode('gbk', 'ignore'), 'html.parser')
        title_list_a = soup.find_all(class_='dl')
        for a in title_list_a:
            em_list = a.find(class_='mb-4').find_all('em')
            len_list.append(em_list.__len__())
        max_index = len_list.index(max(len_list))
        content = title_list_a[max_index].find(class_='answer')
        if content:
            content = content.text
            print(content.replace('答：', ''))
    except Exception:
        pass


missing('横墨文化')