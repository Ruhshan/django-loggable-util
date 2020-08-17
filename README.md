# Django loggable util

An utility to separate create logs for request and reponses while keeping business code clean for class based views. 

### Example usage

Import the Loggable class in your urls.py
```python
from django-loggable-util import Loggable
```

Now write url configuration as this:

```python
urlpatterns=[
...
path('someurl', Loggable(SomeCBView).as_view(),name='some-url-name'),
...
]
```


### Todos
 - Write Tests
 - Support DRF
 - Support FBV

License
----

MIT

**Free Software, Hell Yeah!**