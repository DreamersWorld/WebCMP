# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class HPLaptopItem(Item):
    _id_ = Field()
    raw_name = Field()
    brand = Field()
    url = Field()
    price = Field()
    product_id_ryans = Field()
    description = Field()
    # Specification
    processor = Field()
    clock_speed = Field()
    model = Field()
    cache = Field()
    display_type = Field()
    display_size = Field()
    display_resolution = Field()
    touch = Field()
    ram_type = Field()
    ram = Field()
    graphics_chipset = Field()
    graphics_memory = Field()
    optical_device = Field()
    networking = Field()
    display_port = Field()
    audio_port = Field()
    usb_port = Field()
    battery = Field()
    backup_time = Field()
    weight = Field()
    color = Field()
    operating_system = Field()
    part_no = Field()
    others = Field()
    warranty = Field()
