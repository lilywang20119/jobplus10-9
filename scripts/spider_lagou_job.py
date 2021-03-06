import scrapy
import random

class JobSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['lagou.com']
    #headers = {
    #    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    #    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #    'Accept-Encoding': 'gzip, deflate, br',
    #    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    #    'Connection': 'keep-alive',
    #    'Cache-Control': 'max-age=0',
    #    'Cookie': 'JSESSIONID=ABAAABAAADEAAFI5F082310E3212713B7E8A6B8B4C50B92; SEARCH_ID=065fcf8222d049fca1d0b9bfdb891e4e; user_trace_token=20180827143708-8c727295-97a8-42dc-b96d-e02a511670b2; _ga=GA1.2.357646922.1535351830; _gat=1; _gid=GA1.2.116543037.1535351830; LGSID=20180827143709-9fb38811-a9c3-11e8-b24b-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2F1%2F; LGUID=20180827143709-9fb389ed-a9c3-11e8-b24b-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535075423; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535351830; LGRID=20180827143720-a5ef602e-a9c3-11e8-b24b-5254005c3644',
    #}
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/gongsi/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def start_requests(self):
        urls = [
            'https://www.lagou.com/zhaopin/{}/'.format(i) for i in range(1, 31)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for job in response.css('ul.item_con_list li'):
            yield {
                'name':job.css('div.list_item_top div.p_top h3::text').extract_first(),
                'salary':job.css('div.list_item_top div.p_bot span.money::text').extract_first(),
                'location': job.css('div.list_item_top div.p_top em::text').extract_first(),
                'tags': job.css('div.list_item_bot div.li_b_l span::text').extract(),
                'experience_requirement': job.css('div.list_item_top div.p_bot div.li_b_l::text').re(r'(.+)\s*/\s*(.+)')[0],
                'degree_requirement':job.css('div.list_item_top div.p_bot div.li_b_l::text').re(r'(.+)\s*/\s*(.+)')[1],
                'release_time':job.css( 'div.list_item_top div.p_top span.format-time::text').extract_first(),
            }

    #自动发现下一页链接，连续爬取可能会被重定向到登录页，导致无法爬取后续页面
    # pages = response.css(
    #     'div.pager_container a.page_no::attr(href)').extract()
    # if pages and pages[-1].startswith('https://'):
    #     yield response.follow(pages[-1], callback=self.parse)