from django.db.models import ForeignKey

# this function turns a query into an iterable list
def query_to_list(query, fields_to_ignore=[]):
    data = []
    for obj in query:
        sub_data = []
        for field in obj._meta.get_fields():
            if field.name in fields_to_ignore:
                continue
            value = field.value_from_object(obj)
            print(field.name)
            if isinstance(field, ForeignKey):
                model = field.remote_field.model
                value = str(model.objects.get(pk=value))
            sub_data.append(value)
            print('value', value)
            print('sub_data', sub_data)
        data.append(sub_data)
    return data