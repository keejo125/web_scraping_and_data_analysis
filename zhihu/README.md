# 知乎
## 网络爬虫
### 获取某问题的所有答案
`get_answers.py`
- 使用说明
    - 1、使用chrome打开知乎某个问题网页，在开发者工具-Network中找到类似代码中的url（开头为https://www.zhihu.com/api/v4/questions/28997505/answers），demo中抓取的是[有个漂亮女朋友是什么体验？](https://www.zhihu.com/question/28997505)。
    - 2、替换代码中的url部分。
    - 3、运行`python3 get_answers.py`即可生成两个txt文本，一个为回答，一个为对应的请求url地址。

### 获取话题讨论、精华下的问题和答案 
`get_topic_answers.py`
- 使用说明
    - 1、使用chrome打开知乎首页-话题网页，在开发者工具-Network中找到类似代码中的url  
    开头为`https://www.zhihu.com/api/v4/topics/19550517/feeds/top_activity` 的是讨论tab页的；  
    开头为`https://www.zhihu.com/api/v4/topics/19550517/feeds/essence` 的是精华tab页的。  
    demo中抓取的是[程序员话题]。
    - 2、替换代码中的url的topics编号部分。
    - 3、运行`python3 get_topic_answers.py`即可生成两个csv文本，一个为问题、回答、点赞数，一个为对应的请求url地址。


- 坑与建议
    - 1、知乎的防爬虫会禁用你的ip地址，然后会一直报403错误。跑的太快也会屏蔽一会儿，可通过sleep()来休息一下，但是爬太多了就会禁用你的IP导致一直是403，获取不到response。
    - 2、知乎的网页应该是由js另外渲染生成的，并非通过网址返回html翻页。每个回答都有一是一个请求，返回一个json数据，数据中不仅有回答的内容，还有下一个回答的请求url。所以抓取逻辑是：选择第一个答案请求的url，然后根据返回的json数据中是否有下一个请求url来判断是否继续抓取(有个'is_end'和‘is_start'标志位可以判断是否结束)。由于反爬虫的关系，实际抓取的答案可能也没有'total'字段那么多。
    - 3、每个答案返回的json数据中，答案部分是html代码而非直接的文本。所以可以使用BeautifulSoup来处理提取，很多答案中会有图片和视频，本次都直接忽略了，而且不是所有的答案都在`<p>`标签内，故直接通过soup.text获取文字并替换换行空格等处理了。如需要抓取图片等信息，修改函数`def parse_json(data)`中html处理部分即可，

### 关于防止被网站屏蔽
- 1、增加适当的延迟，比如sleep(random.random()*5)
- 2、修改useragent，比如可以用fake_useragent包，但需要注意的是加载这个包的时候默认会去服务器更新，需要翻墙，建议创建的时候使用ua = UserAgent(use_cache_server=False)停用cache服务器。
- 3、代理，如果有的话。

## 数据分析
`data_analysis.py`
- 提取神回复
    - 处理逻辑：使用pandas读取爬取的问题和答案，筛选出答案字符数少于20，并且按点赞数从高往低排序，最后输出到xls。

- 坑与建议
    - 1、pandas的筛选，网上有些说用loc函数，有时候会提示typeError。  
    ```
    df1.loc([df1['len']<200])  
    Traceback (most recent call last):
    File "<input>", line 1, in <module>
    File "/Users/icbc/Desktop/git/ML-and-DM-in-action-master/DouBanMovie/venv/lib/python3.6/site-packages/pandas/core/indexing.py", line 98, in __call__
        axis = self.obj._get_axis_number(axis)
    File "/Users/icbc/Desktop/git/ML-and-DM-in-action-master/DouBanMovie/venv/lib/python3.6/site-packages/pandas/core/generic.py", line 365, in _get_axis_number
        axis = self._AXIS_ALIASES.get(axis, axis)
    TypeError: unhashable type: 'list'
    ```  
    直接用如下方式就可以筛选了  
    `df[df.answer.str.len() < 20]`
