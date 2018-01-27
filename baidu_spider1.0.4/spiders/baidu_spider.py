import requests
from bs4 import BeautifulSoup
# import re
import settings
from util import common


rule = ['https://jingyan.baidu.com',
        'baike.baidu.com',
        'https://zhidao.baidu.com',
        'https://baike.baidu.com/'
        ]


def crawl(search):
    if search is None:
        search = ''
    else:
        search = search.strip()
    base_url = 'https://www.baidu.com/s'
    queryString = settings.DEFAULT_QUERYSTRING
    queryString['wd'] = search
    if common.math(search):
        return
    headers = settings.DEFAULT_HEADERS
    response = requests.get(url=base_url, params=queryString, headers=headers)
    load_html(response.text, search)


def load_html(content, words):
    html = BeautifulSoup(content, 'lxml')
    # print(html.prettify())
    # print(type(html))
    nodes = html.find('div', id='content_left').find_all("div", class_='c-container')
    # print(nodes.__len__())
    for node in nodes:
        target_url_node = node.find(class_="c-showurl")
        if not target_url_node:
            if node.find('div', class_='c-span-last') is not None:
                abs_content_node = node.find('div', class_='c-span-last')
                print_content = common.process_c_span_last(abs_content_node)
                print(print_content)  # 第一部分，搜索岁数时反馈内容
                return

        # print(node)
        try:
            target_url = target_url_node.text
            # print(target_url_node['href'])      # 链接地址
            # print(target_url)       # 简要地址

            if common.check_url(target_url):   # 'baike', 'zhidao', 'baijia', 'jingyan','zhihu'
                if node.find('div', class_='c-abstract') is not None:
                    abs_content_node = node.find('div', class_='c-abstract')
                    print_content = common.process_c_abstract(abs_content_node)
                elif node.find('div', class_='c-span18') is not None:
                    abs_content_node = node.find('div', class_='c-span18')
                    #   tmp = abs_content_node.text
                    print_content = common.process_c_span(abs_content_node)
                elif node.find('div', class_='c-border') is not None:
                    abs_content_node = node.find('div', class_='c-border')
                    print_content = common.process_c_border(abs_content_node)
                elif node.find('div', class_='c-span24')is not None:
                    abs_content_node = node.find('div', class_='c-span24')
                    print_content = common.process_c_span(abs_content_node)
                else:
                    print_content = ''

            # 第二部分，搜索天气时的反馈结果
            elif node.find_all('div', class_="xpath-log") is not None:
                print_content = common.process_c_xpath_log(node)
                temp = {}
                for i in range(5):
                    temp[print_content[0][i]] = print_content[1][i]
                print(temp)
                return

            elif common.check_music_url(target_url):
                if node.find('div', class_='c-border') is not None:
                    abs_content_node = node.find('div', class_='c-border')
                    print_content = common.process_c_border(abs_content_node)

            if nodes.__len__() == 1:
                if print_content:
                    # print(abs_content_node)   # 显示包括div
                    print(print_content.replace("[专业]", ''))      # 提取div里的text
            
            else:
                if target_url.split(".com")[0].__add__(".com") in rule:     # rule表的网站的问题匹配度都比较高，取其一
                    if print_content:
                        # print("2")
                        # print(target_url_node['href'])
                        # print(print_content)
                        # print(target_url.find("jingyan.baidu"))
                        if target_url.find("jingyan.baidu") >= 0:
                            # print(print_content)
                            r = requests.get(target_url_node['href'], allow_redirects=False)
                            c_url = r.headers['Location']   # 获得重定向后的地址
                            # print(r.headers['Location'])
                            # print(c_url) # 不带网页地址
                            response = requests.get(c_url)      # 百度经验刺激页面...
                            htmls = BeautifulSoup(response.text, 'lxml')
                            node_list = htmls.find_all("div", class_='exp-content')
                            # print(node_list)
                            for i, z in enumerate(node_list, 1):   # 输出经验步骤...
                                print("方法/步骤:", i)
                                print(z.text.replace("百度经验:jingyan.baidu.com", ''))
                            # print(print_content)
                        else:
                            print(print_content.replace("[专业]", ''))
                        return
        except:
            pass
    common.missing(words)


# if __name__ == '__main__':
#     main()
#     # baidu_spider()
#     # test()
