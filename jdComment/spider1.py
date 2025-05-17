import os
import pandas as pd
from DrissionPage import ChromiumPage, ChromiumOptions


dp = ChromiumPage()
dp.scroll.to_bottom()
dp.listen.start('api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments')
dp.get("https://item.jd.com/100149708972.html")

dp.ele('css:#detail > div.tab-main.large > ul > li:nth-child(5)').click()

dp.ele('css:#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-child(5) > a').click()

result = []
for page in range(1, 21):
    print(f'正在爬取第{page}页')
    resp = dp.listen.wait()
    json_data = resp.response.body 
    comments = json_data["comments"]
    for index in comments:
        dit = {
            "昵称": index["nickname"],
            "日期": index["creationTime"],
            "地区": index["location"],
            "产品": index["productColor"],
            "评分": index["score"],
            "评论": index["content"].strip(),
            '标签': "好评"
        }
        result.append(dit)
        print(dit)
    dp.ele('css:.ui-pager-next').click()
    dp.scroll.to_bottom()
        
# df = pd.DataFrame(result, columns=columns)
# df.to_csv("comment.csv", index=False)
