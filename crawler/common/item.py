# Base Item

import scrapy


class ZbiderItem(scrapy.Item):
    """Load zbider Item with default field values"""

    # TAGS
    tags_fields = []
    default_tags_str = ''

    raw_data = False

    zbider_fields = scrapy.Field()
    zbider_type = scrapy.Field()
    zbider_raw_data = scrapy.Field()

    @classmethod
    def load(cls, data):
        item = cls()

        for field, field_attrs in cls.fields.items():
            actual_field = field_attrs.get('source', field)
            item[field] = data.get(actual_field, '')

        if item.raw_data:
            item['zbider_raw_data'] = data

        item.set_zbider_fields()
        item['zbider_type'] = item.get_name()

        return item

    @staticmethod
    def get_name(self):
        raise NotImplementedError

    def set_zbider_fields(self):
        raise NotImplementedError

    def get_tags(self) -> list:
        tag_str = ''
        for f in self.tags_fields:
            tag_str += ' ' + self[f]

        if self.default_tags_str:
            tag_str += ' ' + self.default_tags_str

        return [t for t in tag_str.split(' ') if len(t) > 3]
