# 网络爬虫和数据分析

## 豆瓣
### 豆瓣电影评论抓取
```get_movie_comments.py```
- 使用说明
    - 1、打开豆瓣电影网页，找到要抓取评论的地址。
    - 2、更新 get_movie_comments.py 中的url（默认放了《昨日青空》和《悲伤逆流成河》）的地址。  其实只要更新加粗部分（编号）就好了
    url = 'https://movie.douban.com/subject/***26290410***/comments?start=' + start + '&limit=20&sort=new_score&status=P'
    - 3、运行```python3 get_movie_comments.py```即可，所有评论会保存在csv文件中。

- 坑与建议
    - 1、豆瓣网站的评论只提供220条，再往后都无法显示。每页固定20个，更改limit参数也没用，所以代码中不断更新url中的start来进行翻页处理。
    - 2、每个url返回的是html格式，所以用BeautifulSoup来进行处理和抓取所需信息。写成csv格式，方便后续分析处理。如需修改请根据实际html分析修改代码。
