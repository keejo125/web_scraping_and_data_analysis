# 猫眼
## 网络爬虫
### 获取某电影的所有评论
`get_comments.py`
- 使用说明
    - 1、使用chrome，通过手机浏览的方式，某个电影介绍网页，在开发者工具-Network中找到类似代码中的url（开头为http://m.maoyan.com/review/v2/comments.json?），demo中抓取的是[流浪地球](http://m.maoyan.com/movie/248906/morecomments?_v_=yes)。
    - 2、替换代码中的movieId部分。
    - 3、运行`python3 get_comments.py`即可生成评论的文本。


- 坑与建议
    - 1、由于猫眼网站限制，当`offset`参数大于1000时，就不再提供评论数据。所以无法通过修改`offset`的方式来抓取全部评论。可通过修改`ts`时间的方式来抓取信息。

### 关于防止被网站屏蔽
- 1、修改useragent，比如可以用fake_useragent包，但需要注意的是加载这个包的时候默认会去服务器更新，需要翻墙，建议创建的时候使用`ua = UserAgent(use_cache_server=False)`停用cache服务器。如果仍然报错，可以尝试改成`ua = UserAgent(use_cache_server=False, verify_ssl=False)`。
