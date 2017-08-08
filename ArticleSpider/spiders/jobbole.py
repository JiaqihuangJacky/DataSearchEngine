# -*- coding: utf-8 -*-
import re #to strip
import scrapy
from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    #call this function for download
    def parse(self, response):
        #get all the url and return to scrapy and download and update
        #get all article's url, after download and send it to parse
        #extract will create an array
        #response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract() will give us array
        #response.css("#archive .floated-thumb .post-thumb a::attr(href)") gives us a nodes
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            #call back function to call get the article's information
            #urljoin make the response.url + post_url

            #get nodes' the image
            image_url = post_node.css("img::attr(src)").extract_first("")

            #get nodes's url
            post_url = post_node.css("::attr(href)").extract_first("")

            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},callback=self.parse_detail)
            #get the next page and let scrapy to download

        #This is used to get the next url
        #Using attr the get the url
        #extract first is used for the error checking, and "" is default
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")

        #if we have this value then we join the url together
        #send the next page to scrapy to download
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)



    #get ariticle's certain information / div
    def parse_detail(self, response):

        # 提取文章的具体字段
        # #unilike array
        # #start from 1
        # #not working
        # #re_selector = response.xpath("/html/body/div[3]/div[3]/div[1]/div[1]/h1");
        # #this working
        # #//*[@id="post-110287"]/div[1]/h1
        # #id = xxx must be unique
        # #text() function to reject getting h1, get the text only
        # #re_selector = response.xpath("/html/body/div[1]/div[3]/div[1]/div[1]/h1");
        # #re_selector2 = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()');
        #
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·","").strip()
        # praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]
        # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = match_re.group(1)
        #
        #
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = match_re.group(1)
        # else:
        #     comment_nums = 0
        #
        # content = response.xpath("//div[@class='entry']").extract()[0]
        #
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)



        # via css to get the information
        # extract first is for the error checking

        #get the image url, get avoid error
        front_image_url = response.meta.get("front_image_url", "")

        #get title
        title = response.css(".entry-header h1::text").extract()[0]

        #get create day
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·","").strip()
        praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        fav_nums = response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0

        content = response.css("div.entry").extract()[0]

        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)




        pass

