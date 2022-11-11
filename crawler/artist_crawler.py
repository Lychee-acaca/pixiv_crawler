import json

from crawler.crawler import crawler


class artist_crawler(crawler):
    def __init__(self, artist_id, user_agent, proxies, cookies_path):
        super(artist_crawler, self).__init__(user_agent, proxies, cookies_path)
        self.artist_id = artist_id
        self.img_id_list = self.get_img_id_list()

    def get_img_id_list(self):
        img_list_link = 'https://www.pixiv.net/ajax/user/' + self.artist_id + '/profile/all?lang=zh'
        print("getting img id list", img_list_link)
        r = self.requests_get_loop(img_list_link,
                                   headers=self.header_noreferer)

        img_list_js = json.loads(r.text)

        # illusts manga novels mangaSeries novelSeries
        # illusts only
        img_id_list = []
        for i in img_list_js['body']['illusts'].keys():
            img_id_list.append(i)
        print("got it.")

        return img_id_list

    def artist_download(self, path="./output/"):
        print("{} (series) imgs will be download".format(len(self.img_id_list)))
        for i in self.img_id_list:
            self.img_download(i, path + "{}/".format(self.artist_id))
        print("artist", self.artist_id, "downloaded.")
