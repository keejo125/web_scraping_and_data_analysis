# 爱奇艺
## 网络爬虫
### 获取某视频的所有评论
`get_comments.py`
- 使用说明
    - 1、使用chrome，通过手机浏览的方式，打开某视频页面，demo中抓取的是[我是唱作人](https://m.iqiyi.com/v_19rsh3hwuo.html)。
    - 2、在开发者工具-Network中找到评论请求地址（搜索关键字`get_comments.action`）,并获取请求中的`content_id`的参数。
    - 3、替换代码中的content_id部分。
    - 3、运行`python3 get_comments.py`即可生成评论的csv。


- 坑与建议
    - 1、爱奇艺网页版（www开头的网址）无法展示评论，必须通过访问手机地址（m开头）才行。
    
## 数据分析
`analysis.py`
- 使用说明
    - 1、需先运行`get_comments.py`获取评论csv文件。
    - 2、替换词云图片`chuangzuoren.jpg`，并修改代码中对应部分。
    - 3、运行`python3 analysis.py`即可。
    - 4、结果会生成词云图片`changzuoren_wordcloud.png`，显示性别柱状图。


- 坑与建议
    - 词云的初始图片背景必须是白色的，不能是透明的。
    - 中文词云需要指定中文字符集，否则会乱码。
    - 建议根据原图片的长宽比例进行一定的缩小，以免生成的图片像素过大而产生报错。
    - `matplot`默认不支持中文，需进行配置，详见代码中配置部分。
    - 坐标轴无法通过配置展示为中文。