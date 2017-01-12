#-*-coding:utf-8-*-
#coding=gbk
import sys
import requests
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool


reload(sys)
sys.setdefaultencoding('gbk')

def towrite(content_dic):
    f.writelines(u'评论标题：' + str(content_dic['comment_topic']) + '\n')
    f.writelines(u'评论者：' + str(content_dic['comment_id']) + '\n')
    f.writelines(u'评论时间：' + str(content_dic['comment_time']) + '\n')
    f.writelines(u'评论内容：' + str(content_dic['comment_content']) + '\n')

def spider(url):
    html = requests.get(url)
    selector = etree.HTML(html.text)
    content_field = selector.xpath('//div[@class = "a-section review"]')
    item = {}
    for each in content_field:
        comment_topic = each.xpath('div[1]/a[2]/text()')
        comment_id = each.xpath('div[2]/span[1]/a/text()')
        comment_time = each.xpath('div[2]/span[4]/text()')
        comment_content = each.xpath('div[4]/span/text()')

        item['comment_topic'] = comment_topic[0]
        item['comment_id'] = comment_id[0]
        item['comment_time'] = comment_time[0]
        item['comment_content'] = comment_content[0]

        towrite(item)

##亚马逊，页码数会改变
if __name__ == '__main__':
    pool = ThreadPool(4)
    f = open(r'/media/ljy/learning&download/learning/learning file/HOMEWORK/project/amazon_shujujiegou.txt','w')
    page = []
    for i in range(1, 21):
        pages = "https://www.amazon.cn/product-reviews/B002WC7NGS/ref=cm_cr_getr_d_paging_btm_" + str(i) +"?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber=" + str(i)
        page.append(pages)

    pool.map(spider, page)
    pool.close()
    pool.join()
    f.close()


