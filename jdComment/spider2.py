import os
import time
import pandas as pd
from DrissionPage import ChromiumPage, ChromiumOptions


dp = ChromiumPage()
dp.scroll.to_bottom()
dp.listen.start('api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments')
dp.get("https://item.jd.com/100149708972.html")

dp.ele('css:#detail > div.tab-main.large > ul > li:nth-child(5)').click()

time.sleep(1)
# dp.ele('css:#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-child(5) > a').click()

comment_dict = {
    # "好评": "css:#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-child(5) > a",
    # "中评": "css:#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-child(6) > a",
    "差评": "css:#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-child(7) > a"
}

result = []
columns = ["昵称", "日期", "地区", "产品", "评分", "评论", "标签"]
for key, value in comment_dict.items():
    time.sleep(1)
    dp.ele(value).click()
    for page in range(1, 21):
        print(f'正在爬取 - {key} - 第{page}页')
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
                '标签': key
            }
            result.append(dit)
            print(dit)
        time.sleep(8)
        dp.scroll.to_bottom()
        dp.ele('css:.ui-pager-next').click()
        dp.scroll.to_bottom()
        
df = pd.DataFrame(result, columns=columns)
df.to_csv("comment.csv", index=False, mode='a')