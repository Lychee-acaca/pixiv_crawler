import os.path

from bs4 import BeautifulSoup

from crawler.requests_loop import requests_get_loop


def get_download_link(original_link):
    split_link = original_link.split('/')
    download_link = 'https://i.pximg.net/img-original/img'
    for j in range(6):
        download_link += '/' + split_link[7 + j]
    download_link += '/' + split_link[13].split('_')[0] + '_' + split_link[13].split('_')[1]
    return download_link


def get_ranking_list(r):
    soup = BeautifulSoup(r.content, "html.parser")
    imgList = soup.find_all("section", class_="ranking-item")
    download_link = []
    for i in imgList:
        link = i.find("img").get("data-src")
        download_link.append(get_download_link(link))
    return download_link


class dailyrank_crawler:
    def __init__(self, user_agent, proxies):
        self.user_agent = user_agent
        self.proxies = proxies
        self.header_referer = {"User-Agent": user_agent, "referer": "https://www.pixiv.net/"}
        self.header_noreferer = {"User-Agent": user_agent}

    def get_ranking_page(self):
        print("getting ranking page....")
        r = requests_get_loop('https://www.pixiv.net/ranking.php',
                              headers=self.header_noreferer,
                              proxies=self.proxies)
        print("got it.")
        return r

    def download_img(self, download_link):
        path = "./output/"
        if not os.path.exists(path):
            os.makedirs(path)
        for raw_link in download_link:
            success = False
            link = raw_link + '.png'
            while not success:
                print("downloading " + link)
                img_req = requests_get_loop(link, headers=self.header_referer, proxies=self.proxies)

                if len(img_req.content) > 100:
                    with open(path + link.split('/')[-1], mode="wb") as f:
                        f.write(img_req.content)
                    success = True
                else:
                    if link.split('.')[-1] != 'jpg':
                        link = raw_link + '.jpg'
                    else:
                        break
            if success:
                print("success.")
            else:
                print('unknown format!!!')
