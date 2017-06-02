
# coding: utf-8

# In[2]:

import scrapy
from bs4 import BeautifulSoup
from scrapy_douban.items import ScrapyDoubanItem


class MoviesSpider(scrapy.Spider):
    name="movies"
    #控制翻页数目
    count = 0
    start_urls = [ 
        # 'http://quotes.toscrape.com/page/1/'
        'https://movie.douban.com/tag/美国',
    ]
    def parse(self,response):
        print('------------------------------------------------')
        #抽取首页的电影链接
        for movie_link in response.css('div.pl2>a::attr(href)').extract():
            #对每个链接请求，解析
            yield scrapy.Request(movie_link, callback=self.extract_info)
        #翻页
        next_page = response.css('#content > div > div.article > div.paginator > span.next > a::attr(href)').extract_first()
        print(next_page)
        if next_page is not None and self.count<25:
            yield scrapy.Request(next_page, callback=self.parse)
            self.count += 1
            
        print('------------------------------------------------')

    def extract_with_css(self,query,response):
        if response.css(query).extract_first():
            return response.css(query).extract_first().strip()

    def extract_with_xpath(self,query,response):
        if response.xpath(query).extract():
            return response.xpath(query).extract()

    def extract_info(self, response):
            item = ScrapyDoubanItem()
            #使用BeautifulSoup解析
            soup = BeautifulSoup(response.body,'html.parser')
            # #解析电影名
            # name_span = soup.select('span[property="v:itemreviewed"]')
            #解析类型
            type_span = soup.select('span[property="v:genre"]')
            type_string = []
            for i in type_span:
                type_string.append(i.string.strip())
            #解析上映日期
            release_span = soup.select('span[property="v:initialReleaseDate"]')
            release_string = []
            for j in release_span:
                release_string.append(j.string.strip())
            #解析时长
            duration_span = soup.select('span[property="v:runtime"]')
            #解析编剧
            scenarist_string = []
            for i in response.css('#info > span:nth-child(3) > span.attrs a::text').extract():
                scenarist_string.append(i.strip())
            #解析演员
            actors_string = []
            for i in response.css('#info > span.actor > span.attrs a::text').extract():
                actors_string.append(i.strip())
            #解析影评
            brief_into = soup.select('div#link-report span[property="v:summary"]')[0]
            #解析评分
            ratings_string = self.extract_with_css('#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong::text',response)
            #请求IMDb页面
            IMDb_link = self.extract_with_css('#info > a::attr(href)',response)
            if IMDb_link:
                yield scrapy.Request(IMDb_link, callback=self.extract_IMDb_info)
            try:
                item['english'] = 0
                item['name'] = self.extract_with_css('#content > h1 > span:nth-child(1)::text',response)
                item['director'] = self.extract_with_css('#info > span:nth-child(1) > span.attrs > a::text',response)
                item['scenarists'] = scenarist_string
                item['actors'] = actors_string
                item['movie_type'] = type_string
                item['release_date'] = release_string
                item['duration'] = duration_span[0].string.strip()
                item['IMDB'] = IMDb_link
                item['brief_into'] = brief_into.text.strip()
                item['ratings'] = ratings_string
                yield item
            except Exception as e:
                print('Exception:%s' % (e))
                # continue
                
            # if duration_span and release_span and ratings_string and brief_into:
            #     yield{
            #         'english':0,
            #         'name':self.extract_with_css('#content > h1 > span:nth-child(1)::text',response),
            #         'director':self.extract_with_css('#info > span:nth-child(1) > span.attrs > a::text',response),
            #         'scenarists':scenarist_string,
            #         'actors':actors_string,
            #         'type':type_string,
            #         'release_date':release_string,
            #         'duration':duration_span[0].string.strip(),
            #         'IMDb':IMDb_link,
            #         'brief_into':brief_into.text.strip(),
            #         #'brief_into':self.extract_with_css('#link-report > span:nth-child(1)::text',response),
            #         'ratings':ratings_string,
            #     }
    def extract_IMDb_info(self, response):
        item = ScrapyDoubanItem()
        soup = BeautifulSoup(response.body,'html.parser')
        #解析电影名
        name_string = self.extract_with_xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/h1/text()',response)
        if name_string:
            name_string = name_string[0].strip()
        #解析时长
        duration_span = soup.select('time[itemprop="duration"]')
        #解析上映日期
        release_span = soup.select('a[title="See more release dates"]')
        #解析类型
        type_string = []
        type_span = soup.select('span[itemprop="genre"]')
        for i in type_span:
            type_string.append(i.string.strip())
        # #解析导演
        # director_string = []
        # director_span = soup.select('span[itemprop="name"]')
        # for i in director_span:
        #     director_string.append(i.string.strip())
        #解析编剧
        scenarist_string = []
        scenarist_span = soup.select('span[itemprop="creator"] span[itemprop="name"]')
        for i in scenarist_span:
            scenarist_string.append(i.text.strip())
        #解析演员
        actors_string = []
        actors_span = soup.select('span[itemprop="actors"] span[itemprop="name"]')
        for i in actors_span:
            actors_string.append(i.text.strip())
        #解析评分
        # ratings_string = soup.select('span[itemprop="ratingValue"]')[0].text.strip()
        ratings_string = self.extract_with_xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()',response)
        #解析影评
        brief_into_string=''
        brief_into_p = soup.select('div#titleStoryLine div[itemprop="description"] p')[0]
        if brief_into_p.find('a'):
            brief_into_string = brief_into_p.text.split('Written by')[0].strip()
        else:
            brief_into_string = brief_into_p.text.strip()

        try:
            item['english'] = 1
            item['name'] = name_string
            item['duration'] = duration_span[0].text.strip()
            item['release_date'] = release_span[0].text.strip()
            item['director'] = self.extract_with_xpath('//*[@id="title-overview-widget"]/div[3]/div[2]/div[1]/div[2]/span/a/span/text()',response)
            item['scenarists'] = scenarist_string
            item['actors'] = actors_string
            item['movie_type'] = type_string
            item['ratings'] = ratings_string
            item['brief_into'] = brief_into_string
            item['IMDB'] = None
        except Exception as e:
            print('Exception:%s' % (e))
            # continue
        # if duration_span and release_span and ratings_string and brief_into_string:
        #     yield{
        #         'english':1,
        #         'name':name_string,
        #         'duration':duration_span[0].text.strip(),
        #         'release_date':release_span[0].text.strip(),
        #         'director':self.extract_with_xpath('//*[@id="title-overview-widget"]/div[3]/div[2]/div[1]/div[2]/span/a/span/text()',response),
        #         'scenarists':scenarist_string,
        #         'actors':actors_string,
        #         'type':type_string,
        #         'ratings':ratings_string,
        #         # 'ratings':ratings_string,
        #         'brief_into':brief_into_string,
        #     }
        

# In[ ]:



