# 当当网
## 当当网所有书籍分类抓取
`get_book_category.py`
- 使用说明
  - 1、运行`python3 get_book_category.py`即可，所有目录会保存在生成的`dd_category.txt`中。

- 坑与建议
  - 1、如果是在python2的环境下注意网页字符编码的设置。在获取的网页信息的`meta`中可以看到当前网页的编码。
  - 2、观察当当网的书籍页面可以发现，书籍分类是通过链接中的由`.`号分割的一串数字实现的，如下面示例网址中的数字部分，所以可以通过使用正则匹配的方式获取子分类。
    ```
    # 教材的一级目录 教材
    href="http://category.dangdang.com/cp01.49.00.00.00.00.html"
    # 教材的二级目录  研究生/本科/专科教材
    href="http://category.dangdang.com/cp01.49.01.00.00.00.html"
    # 教材的二级目录  高职/高专教材
    href="http://category.dangdang.com/cp01.49.05.00.00.00.html"
    ```
