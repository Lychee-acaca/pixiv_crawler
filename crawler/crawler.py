import os

import requests


class crawler:
    def __init__(self, user_agent, proxies, cookies_path):
        self.user_agent = user_agent
        self.proxies = proxies
        with open(cookies_path, 'r') as f:
            self.cookies = f.read()

        self.header_referer = {"User-Agent": user_agent, "referer": "https://www.pixiv.net/", "cookie": self.cookies}
        self.header_noreferer = {"User-Agent": user_agent, "cookie": self.cookies}

    def img_download(self, img_id, path="./output/"):
        if not os.path.exists(path):
            os.makedirs(path)
        link = self.get_img_download_link(img_id)
        img_format = link.split('.')[-1]
        link = link.split('_')[0]
        img_cnt = 0
        done = False
        while not done:
            download_link = link + '_p{}.'.format(img_cnt) + img_format
            print('trying download', download_link)
            img_req = self.requests_get_loop(download_link, headers=self.header_referer)
            if len(img_req.content) > 100:
                with open(path + download_link.split('/')[-1], mode="wb") as f:
                    f.write(img_req.content)
                img_cnt += 1
            else:
                print("p{} do not exist".format(img_cnt))
                done = True
        print("total {} imgs downloaded.".format(img_cnt))

    def get_img_download_link(self, img_id):
        check_link = 'https://www.pixiv.net/artworks/' + img_id
        r = self.requests_get_loop(check_link,
                                   headers=self.header_noreferer)
        raw_img_link = r.text.split('"')
        for i in range(len(raw_img_link)):
            if raw_img_link[i] == 'original':
                return raw_img_link[i + 2]

    def requests_get_loop(self, link, headers, params=None):
        retry_cnt = 0
        while True:
            try:
                r = requests.get(link,
                                 headers=headers,
                                 proxies=self.proxies,
                                 params=params,
                                 verify=False)
                return r
            except Exception as e:
                retry_cnt += 1
                print("{}, get ranking failed! retry {}...".format(e, retry_cnt))
