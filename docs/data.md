# Data - Documentation - Django Event Management

Contents:

- [Predefined data](#predefined-data)
- [Fixtures: Import and Export](#fixtures-import-and-export)

## Predefined data

The project uses predefinded data for the models **Country**, **Level** and **Unit**.  
The data is available in the [fixtures directory](../events/fixtures).

## Fixtures: Import and Export

- <https://docs.djangoproject.com/en/4.2/howto/initial-data/>
- <https://docs.djangoproject.com/en/4.2/topics/serialization/>

### Export: Serialize to fixtures

- <https://docs.djangoproject.com/en/4.2/ref/django-admin/#dumpdata>
- `python manage.py dumpdata --natural-foreign --natural-primary --format xml --output dump.xml`

#### Serialize using the shell

```shell
python manage.py shell
```

```python
from django.core import serializers
from events.models import Country
data = serializers.serialize("xml", Country.objects.all())

f = open("events/fixtures/country.xml", "w") 
f.write(data)
f.close()

exit()
```

```python
from django.core import serializers
from django.contrib.auth.models import User
data = serializers.serialize("xml", User.objects.all())

f = open("events/fixtures/user.xml", "w") 
f.write(data)
f.close()

exit()
```

```python
print(data)
# <?xml version="1.0" encoding="utf-8"?>
# <django-objects version="1.0"><object model="events.country" pk="1"><field name="title" type="CharField">Germany</field></object></django-objects>
```

### Import: Deserialize from fixtures

- <https://docs.djangoproject.com/en/4.2/ref/django-admin/#loaddata>
- `python manage.py loaddata file`

#### Deserialize using the shell

```shell
python manage.py shell
```

```python
from django.core import serializers

f = open("events/fixtures/country.xml", "r")
data = f.read()
f.close()

for obj in serializers.deserialize("xml", data):
  obj.save()

exit()
```

#### Deserialize all fixtures

```python
from django.core import serializers

def import_fixures(files):
    for file in files:
        f = open("events/fixtures/" + file, "r")
        data = f.read()
        f.close()
        for obj in serializers.deserialize("xml", data):
            obj.save()


import_fixures(['country.xml', 'level.xml', 'unit.xml', 'user.xml', 'person.xml', 'event.xml', 'registration.xml'])

exit()
```
