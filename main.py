import urllib3

from crawler.dailyrank_crawler import dailyrank_crawler, get_ranking_list

# 关闭warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 " \
             "Safari/537.36 "
proxies = {'http': 'http://localhost:7890', 'https': 'http://localhost:7890'}

dc = dailyrank_crawler(user_agent, proxies)
dc.download_img(get_ranking_list(dc.get_ranking_page()))

print("done")
