import scrapy

class CarSpider(scrapy.Spider):
    name = 'carmudi'

    start_urls = ['https://www.carmudi.co.id/mobil-dijual/indonesia?type=used&page_number=1&page_size=25']
    #start_urls = ['https://www.carmudi.co.id/dijual/toyota-avanza-g-dki-jakarta-ampera/11551902']

    def parse(self, response):
        car_links = response.xpath('//h2[@class="listing__title  epsilon  flush"]/a')
        yield from response.follow_all(car_links, self.parse_car)

        next_page = response.xpath('//li[@class="next"]/a').css('::attr(href)')
        yield from response.follow_all(next_page, self.parse)

    def parse_car(self, response):

        def get_value(text):
            return response.xpath(f'//span[contains(text(), "{text}")]/following-sibling::*').css('::text').get()
        
        general_info = response.css('div.o-container li[itemprop="itemListElement"] span::text').getall()

        def get_general_info(idx):
            try:
                v = general_info[idx]
            except:
                return None
            
            return v
        
        yield {
            'url': response.url,
            'merk': get_general_info(2),
            'model': get_general_info(3),
            'varian' : get_general_info(4),
            'title' : response.xpath('//h1').css('::text').get(),
            'tahun' : get_value("Tahun Kendaraan"),
            'kilometer' : get_value('Kilometer'),
            'warna': get_value('Warna'),
            'engine cc': get_value('Cakupan mesin'),
            'transmisi': get_value('Transmisi'),
            'penumpang': get_value('Penumpang'),
            'pintu': get_value('Pintu'),
            'panjang': get_value('Panjang'),
            'lebar': get_value('Lebar'),
            'tinggi': get_value('Tinggi'),
            'harga': response.xpath("//div[@class='listing__item-price']/h3").css('::text').get()
        }