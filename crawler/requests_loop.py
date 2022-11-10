import requests


def requests_get_loop(link, headers, proxies):
    retry_cnt = 0
    while True:
        try:
            r = requests.get(link,
                             headers=headers,
                             proxies=proxies,
                             verify=False)
            return r
        except Exception as e:
            retry_cnt += 1
            print("{}, get ranking failed! retry {}...".format(e, retry_cnt))
