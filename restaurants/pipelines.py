# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from restaurants import settings
from scrapy.exporters import CsvItemExporter
from os import path, mkdir

class ToCsvPipeline(object):
    """Outputs data to a csv file."""

    def open_spider(self, spider):
        scrapedate = datetime.now().strftime('%Y%m%d_%H%M%S')
        if not path.exists(settings.CSV_STORE):
            mkdir(settings.CSV_STORE)
        assert path.isdir(settings.CSV_STORE), \
        '{} is not a directory'.format(settings.CSV_STORE)
        pth_csv = path.join(settings.CSV_STORE, 'data_{}.csv'.format(scrapedate))
        self.file = open(pth_csv, 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.fields_to_export = ['title', 'address', 'cuisines',
                                          'opening', 'phone', 'website'
                                         ]
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
