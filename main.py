import execjs
import requests
import os
import time
import re
import PyPDF2
from fake_useragent import UserAgent


def get_t():
    '''
    执行 JavaScript 代码生成参数 t
    '''
    with open(r'1.js') as f:
        s = f.read()
        s = execjs.compile(s)
        t = s.call('t')
        return t


def get_url(p):
    '''
    生成对应页数的 url
    '''
    url = 'http://bnu.chineseall.cn/v3/book/content/MEhQg/pdf/{}?t={}'
    t = get_t()
    url = url.format(p,t)
    return url


def get_requests(url,p):
    '''
    请求 pdf url
    '''
    while True: # 请求失败，在请求一直成功为止
        try:
            headers = {'User-Agent' : UserAgent().random,
                       'Cookie' : 'JSESSIONID=B57897ED41A2F1ECD2671C41FC82C220; _Tvt5MJ89bV_=739934DDCEE38ADAC1E9FFF6FC2CD718430EC777EF79304BDB160251F1DF866BBC46CA249195D785FDEA3A2BA7D78D92313019BE293C7A63E678CE620BE3BC9ED6FC0C10274612BBF3FE3DB35575054C; LvGPHdwDRT=CW2SRK2QWPBV7C53YMJUMUG7ZI4HPSRD3EV4VMCSUM3GBSIV357GSLVVW2IEHQIVZRWYEUOXXANVNNVJCJPDH2CWQF5JIMTGFIK2YTY'
                       }
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                return response
        except:
            continue


def download_pdf(text,p):
    '''
    下载为 pdf，名称为页码
    '''
    with open(str(p) + '.pdf','wb') as f:
        f.write(text)
        print('第 %s 页下载成功，共 274 页。' % str(p))


def merge_pdf(name):
    '''
    合并 pdf
    '''
    print('正在合并最终 pdf')
    # find all the pdf files in current directory.
    mypath = os.getcwd()
    pattern = r"\.pdf$"
    file_names_lst = [mypath + "\\" + f for f in os.listdir(mypath) if re.search(pattern, f, re.IGNORECASE)
                      and not re.search(name+'.pdf', f)]

    # 对文件路径按页码排序
    dic = {}
    for i in range(len(file_names_lst)):
        page = re.findall(r'(\d+)\.pdf', file_names_lst[i])[0]
        dic[int(page)] = file_names_lst[i]
    file_names_lst = sorted(dic.items(), key=lambda x: x[0])
    file_names_lst = [file[1] for file in file_names_lst]

    # merge the file.
    opened_file = [open(file_name, 'rb') for file_name in file_names_lst]
    pdfFM = PyPDF2.PdfFileMerger()
    for file in opened_file:
        pdfFM.append(file)

    # output the file.
    with open(mypath + "\\" + name + ".pdf", 'wb') as write_out_file:
        pdfFM.write(write_out_file)

    # close all the input files.
    for file in opened_file:
        file.close()

    print('合并完成 %s' % name)


def main():
    '''
    主逻辑
    '''
    for p in range(1,275): # 共有 446 也 pdf
        url = get_url(p) # 构造这一页的 url
        response = get_requests(url,p) # 请求 pdf 链接
        download_pdf(response.content,p) # 图片下载为 pdf
    merge_pdf(name='Android移动开发基础案例教程') # 合并 pdf 文件，name 为电子书名


if __name__ == '__main__':
    main()
