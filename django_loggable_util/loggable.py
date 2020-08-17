import logging
from functools import wraps
from django.conf import settings


class Loggable:
    def __init__(self, view_class, log_exception=False):
        self.view_func = view_class.as_view()
        self.log_exception = log_exception
        self.logger = self._get_logger()

    def _get_logger(self):
        if hasattr(settings, 'LOGGABLE_LOGGER'):
            return logging.getLogger(settings.LOGGABLE_LOGGER)
        else:
            logging.config.dictConfig(self._get_default_log_config())
            return logging.getLogger('request_response')

    def _get_default_log_config(self):
        return {
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

    def _get_params(self, request):
        if request.method == 'GET':
            return request.GET
        post_params = dict(request.POST)
        del post_params['csrfmiddlewaretoken']
        return post_params

    def as_view(self):
        @wraps(self.view_func)
        def _wrapped_view_func(request, *args, **kwargs):
            reqMessage = {'method': request.method,
                          'path': request.path,
                          'username': request.user.username,
                          'params': self._get_params(request)
                          }
            self.logger.info({'request': reqMessage})

            try:
                response = self.view_func(request, *args, **kwargs)
                resMessage = {
                    'username': request.user.username,
                    'status_code': response.status_code,
                }
                if hasattr(response, 'template_name'):
                    resMessage['template'] = response.template_name
                if hasattr(response.context_data, 'form'):
                    resMessage['errors'] = response.context_data.get('form').errors
                if hasattr(response, 'url'):
                    resMessage['url'] = response.url
                self.logger.info({'response': resMessage})
                return response
            except Exception as e:
                resMessage = {
                    'username': request.user.username,
                    'exception': e
                }
                if self.log_exception:
                    self.logger.exception({'exception': resMessage})
                raise e

        return _wrapped_view_func
