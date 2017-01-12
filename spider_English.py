#-*-coding:utf-8-*-
#coding=gbk
import sys
import requests
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool


reload(sys)
sys.setdefaultencoding('utf-8')

def towrite(content_dic):
    f.writelines(u'topic：' + str(content_dic['comment_topic']) + '\n')
    f.writelines(u'score：' + str(content_dic['comment_score']) + '\n')
    f.writelines(u'reviewer：' + str(content_dic['comment_id']) + '\n')
    f.writelines(u'time：' + str(content_dic['comment_time']) + '\n')
    f.writelines(u'content：' + str(content_dic['comment_content']) + '\n')

# First we need to obtain an URL text file (include the url you want your spider to catch)	
def spider(url):
    html = requests.get(url)
    selector = etree.HTML(html.text)
	#let your spider find where the customer review are
    content_field = selector.xpath('//div[@class = "a-section review"]')
    item = {}
	
	# the content in xpath varied according to what you want to get
    for each in content_field:
        comment_topic = each.xpath('div[1]/a[2]/text()')
        comment_score = each.xpath('div[1]/a[1]/i/span/text()')
        comment_id = each.xpath('div[2]/span[1]/a/text()')
        comment_time = each.xpath('div[2]/span[4]/text()')
        comment_content = each.xpath('div[4]/span/text()')

        item['comment_topic'] = comment_topic[0]
        item['comment_score'] = comment_score[0]
        item['comment_id'] = comment_id[0]
        item['comment_time'] = comment_time[0]
        item['comment_content'] = comment_content[0]

        towrite(item)

# change the pages of the url 
if __name__ == '__main__':
	# multiprocessing: accelrate your speed~
    pool = ThreadPool(8)
	# open/create a file to write down the customer review
    f = open(r'C:\data_for_use\test.txt','w')

    name_url = requests.get("https://www.amazon.com/8-Foot-Yoga-Strap-Durable-Cotton/product-reviews/B00XB0DVJS/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber=2")
    name_selector = etree.HTML(name_url.text)
	#find out the product name
    product_name = name_selector.xpath('/html/body/div[1]/div[2]/div/div[1]/div[1]/div/div[2]/div/div/div[2]/div[1]/h1/a/text()')
    f.write(str(product_name[0]) + '\n')

    page = []
    for i in range(1, 21):
        pages = "https://www.amazon.com/8-Foot-Yoga-Strap-Durable-Cotton/product-reviews/B00XB0DVJS/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber=" + str(i)
        page.append(pages)

    pool.map(spider, page)
    pool.close()
    pool.join()
    f.close()



