from bs4 import BeautifulSoup

from crawler.crawler import crawler


class dailyrank_crawler(crawler):
    def __init__(self, user_agent, proxies, cookies_path):
        super(dailyrank_crawler, self).__init__(user_agent, proxies, cookies_path)
        self.img_id_list = self.get_img_id_list()

    def get_img_id_list(self):
        print("getting ranking page....")
        r = self.requests_get_loop('https://www.pixiv.net/ranking.php',
                                   headers=self.header_noreferer)
        soup = BeautifulSoup(r.content, "html.parser")
        imgList = soup.find_all("section", class_="ranking-item")
        img_id_list = []
        for i in imgList:
            link = i.find("img").get("data-src")
            img_id = link.split('/')[-1].split('_')[0]
            img_id_list.append(img_id)
        print("got it.")
        return img_id_list

    def dailyrank_download(self, path="./output/daily/"):
        print("{} (series) imgs will be download".format(len(self.img_id_list)))
        cnt = 0
        for i in self.img_id_list:
            cnt += 1
            print("Download progress: {} / {}".format(cnt, len(self.img_id_list)))
            self.img_download(i, path)
        print("daily rank downloaded.")
