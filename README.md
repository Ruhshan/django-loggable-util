# Django loggable util

An utility to separate create logs for request and response while keeping business code clean for class based views. 

### Example usage

Import the `Loggable` class in your urls.py
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

You can pass usual parameters like `template_name` etc, in `as_view()` function.

This will result in logs like this for every request response cycle:

```text
INFO | 2020-08-17 09:10:12.764 | {'request': {'method': 'GET', 'path': '/someurl', 'username': 'someuser', 'params': <QueryDict: {'somekey':'someval'}>}}
INFO | 2020-08-17 09:10:12.777 | {'response': {'username': 'someuser', 'status_code': 200, 'template': ['sometemplate.html']}}
```

A default configuration is embedded with with library for checking if it works or not which is like this:

```python
default_log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'request_response_formatter': {
            'format': '%(levelname)s | %(asctime)s.%(msecs)03d | %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        }
    },
    'handlers': {
        'request_response_console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'request_response_formatter'
        }

    },
    'loggers': {
        'request_response': {
            'handlers': ['request_response_console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
```
This configuration streams logs to console. When it is needed to stream logs to files or any other service, 
you can add that logging configuration in `settings.py` and provide logger name to use for this library like this:

```python
LOGGABLE_LOGGER='your_logger_name'
```

### Todos
 - Write Tests
 - Support DRF
 - Support FBV

License
----

MIT

**Free Software, Hell Yeah!**