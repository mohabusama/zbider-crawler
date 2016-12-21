# Pipeline for User item


class SerializerPipeline:

    def process_item(self, item, spider):
        for field, field_dict in item.fields.items():
            value = item[field]
            item[field] = self.process_item_field(field, field_dict, value, item)
        return item

    def process_item_field(self, field, field_dict, value, item=None):
        if 'serializer' in field_dict:
            return field_dict['serializer'](value, item=item)

        return value
