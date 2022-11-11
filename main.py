import urllib3

from crawler.artist_crawler import artist_crawler
from crawler.dailyrank_crawler import dailyrank_crawler

# 关闭warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 " \
             "Safari/537.36 "
proxies = {'http': 'http://localhost:7890', 'https': 'http://localhost:7890'}

dc = dailyrank_crawler(user_agent, proxies, 'cookies.txt')
dc.dailyrank_download()

# 需要cookies信息，不然获取的图片列表不全
# ac = artist_crawler('65320493', user_agent, proxies, 'cookies.txt')
# ac.artist_download()

print("done")
