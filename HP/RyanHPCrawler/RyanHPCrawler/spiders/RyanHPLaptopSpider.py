import scrapy
from scrapy import spider
from scrapy import log
from scrapy.exceptions import CloseSpider

from RyanHPCrawler.items import HPLaptopItem

class Crawler(scrapy.Spider):
    name = "ryan_hp_crawler"

    def start_requests(self):
        # Indices
        self.BRAND = 0
        self.MODEL = 1
        self.PROCESSOR = 2
        self.CLOCK_SPEED = 3
        self.CACHE = 4
        self.DISPLAY_TYPE = 5
        self.DISPLAY_SIZE = 6
        self.DISPLAY_RESOLUTION = 7
        self.TOUCH = 8
        self.RAM_TYPE = 9
        self.RAM = 10
        self.GRAPHICS_CHIPSET = 11
        self.GRAPHICS_MEMORY = 12
        self.OPTICAL_DEVICE = 13
        self.NETWORKING = 14
        self.DISPLAY_PORT = 15
        self.AUDIO_PORT = 16
        self.USB_PORT = 17
        self.BATTERY = 18
        self.BACKUP_TIME = 19
        self.WEIGHT = 20
        self.COLOR = 21
        self.OPERATING_SYSTEM = 22
        self.PART_NO = 23
        self.OTHERS = 24
        self.WARRANTY = 25


        # From page 1
        self.main_url = 'https://ryanscomputers.com/notebook/all-notebook/filter/cat/148.html?p='

        self.specification_tab = "#tab-product-view2"

        self.id = 0

        self.current_page = 1

        yield scrapy.Request(self.main_url + str(self.current_page), self.parse)

    def parse(self, response):
        self.main_selection = response.xpath("//h2[@class='product-name']")

        for sel in self.main_selection:
            hp_laptop = HPLaptopItem()
            hp_laptop['raw_name'] = sel.xpath("a/text()").extract_first()
            hp_laptop['url'] = sel.xpath("a/@href").extract_first()

            request = scrapy.Request(hp_laptop['url'] + self.specification_tab, callback=self.parseLaptop)

            request.meta['hp_laptop'] = hp_laptop

            yield request

        # Crwaling next page
        self.current_page += 1

        try:
            yield scrapy.Request(self.main_url + str(self.current_page), self.parse)
        except:
            raise CloseSpider('Done crawling')

    def insert_data(self, _item, hp_laptop):
        doc = {
            "BRAND" : _item[self.BRAND],
            "MODEL" : _item[self.MODEL],
            "PROCESSOR" : _item[self.PROCESSOR],
            "CLOCK_SPEED" : _item[self.CLOCK_SPEED],
            "CACHE": _item[self.CACHE],
            "DISPLAY_TYPE" : _item[self.DISPLAY_TYPE],
            "DISPLAY_SIZE" : _item[self.DISPLAY_SIZE],
            "DISPLAY_RESOLUTION" : _item[self.DISPLAY_RESOLUTION],
            "TOUCH" : _item[self.TOUCH],
            "RAM_TYPE" : _item[self.RAM_TYPE],
            "RAM" : _item[self.RAM],
            "GRAPHICS_CHIPSET" : _item[self.GRAPHICS_CHIPSET],
            "GRAPHICS_MEMORY" : _item[self.GRAPHICS_MEMORY],
            "OPTICAL_DEVICE" : _item[self.OPTICAL_DEVICE],
            "NETWORKING" : _item[self.NETWORKING],
            "DISPLAY_PORT" : _item[self.DISPLAY_PORT],
            "AUDIO_PORT" : _item[self.AUDIO_PORT],
            "USB_PORT" : _item[self.USB_PORT],
            "BATTERY" : _item[self.BATTERY],
            "BACKUP_TIME" : _item[self.BACKUP_TIME],
            "WEIGHT" : _item[self.WEIGHT],
            "COLOR" : _item[self.COLOR],
            "OPERATING_SYSTEM" : _item[self.OPERATING_SYSTEM],
            "PART_NO" : _item[self.PART_NO],
            "OTHERS" : _item[self.OTHERS],
            "WARRANTY" : _item[self.WARRANTY]
        }

        hp_laptop['brand'] = doc['BRAND']
        hp_laptop['model'] = doc['MODEL']
        hp_laptop['processor'] = doc['PROCESSOR']
        hp_laptop['clock_speed'] = doc['CLOCK_SPEED']
        hp_laptop['cache'] = doc['CACHE']
        hp_laptop['display_type'] = doc['DISPLAY_TYPE']
        hp_laptop['display_size'] = doc['DISPLAY_SIZE']
        hp_laptop['display_resolution'] = doc['DISPLAY_RESOLUTION']
        hp_laptop['touch'] = doc['TOUCH']
        hp_laptop['ram_type'] = doc['RAM_TYPE']
        hp_laptop['ram'] = doc['RAM']
        hp_laptop['graphics_chipset'] = doc['GRAPHICS_CHIPSET']
        hp_laptop['graphics_memory'] = doc['GRAPHICS_MEMORY']
        hp_laptop['optical_device'] = doc['OPTICAL_DEVICE']
        hp_laptop['networking'] = doc['NETWORKING']
        hp_laptop['display_port'] = doc['DISPLAY_PORT']
        hp_laptop['audio_port'] = doc['AUDIO_PORT']
        hp_laptop['usb_port'] = doc['USB_PORT']
        hp_laptop['battery'] = doc['BATTERY']
        hp_laptop['backup_time'] = doc['BACKUP_TIME']
        hp_laptop['weight'] = doc['WEIGHT']
        hp_laptop['color'] = doc['COLOR']
        hp_laptop['operating_system'] = doc['OPERATING_SYSTEM']
        hp_laptop['part_no'] = doc['PART_NO']
        hp_laptop['others'] = doc['OTHERS']
        hp_laptop['warranty'] = doc['WARRANTY']

        # self.logger.info(hp_laptop)


    def parseLaptop(self, response):
        self.id += 1

        hp_laptop = response.meta['hp_laptop']

        hp_laptop['_id_'] = self.id

        data_list = response.xpath("//table")[0].xpath("//td/text()").extract()

        # Get the price
        hp_laptop['price'] = response.xpath("//span[@itemprop='price']/text()").extract_first()

        self.insert_data(data_list, hp_laptop)

        yield hp_laptop
