import requests
from multiprocessing import Pool
import os

yuebing_dir=r"D:\OneDrive - CUHK-Shenzhen\Linkeer365BookReview\source\_posts"
yuebing_path=r"D:\OneDrive - CUHK-Shenzhen\Linkeer365BookReview\source\_posts\【长期更新】每日传书计划.md"

auth=("genesis","upload")

headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}

def get_all_urls():
    with open(yuebing_path,"r",encoding="utf-8") as f:
        lines=f.readlines()
    urls=[]
    idxs=[]
    for each_idx,each_line in enumerate(lines):
        if "(" in each_line and ")" in each_line:
            url=(each_line.rsplit("(",maxsplit=1)[1])[:-4]
            urls.append(url)
            idxs.append(each_idx)
    del urls[0]
    del idxs[0]
    print("目前已经上传{}本书".format(len(urls)))
    for each_url in urls:
        print(each_url)

    return urls,idxs

def is_bad_link(some_link):
    bad_msg="No record with such MD5 hash has been found</body></html>"
    resp_text=requests.get(url=some_link,headers=headers).text
    pred=(resp_text[0]=='N')
    return pred



def get_title_from_one_line(some_line):
    return some_line.split("|")[1]

def print3times(some_url,some_idx,idxs,lines):
    if is_bad_link(some_url):
        print("BadBadBad")
        this_line_idx = idxs[some_idx]
        this_line = lines[this_line_idx]
        this_title = get_title_from_one_line(this_line)
        print("Title:{}".format(this_title))
    else:
        print("GoodGoodGood")
        # this_line_idx = idxs[some_idx]
        # this_line = lines[this_line_idx]
        # this_title = get_title_from_one_line(this_line)
        # print("Title:{}".format(this_title))

def main():
    with open(yuebing_path,"r",encoding="utf-8") as f:
        lines=f.readlines()

    urls,idxs=get_all_urls()
    pool=Pool(processes=64)

    for each_idx,each_url in enumerate(urls):
        pool.apply_async(print3times,args=(each_url,each_idx,idxs,lines))

    pool.close()
    pool.join()
    print("done.")


if __name__ == '__main__':
    main()

