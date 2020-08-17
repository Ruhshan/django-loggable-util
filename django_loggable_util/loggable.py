import logging
from functools import wraps

from django.conf import settings

from .config import default_log_config


class Loggable:
    def __init__(self, view_class, log_exception=True):
        self.view_func = view_class
        self.log_exception = log_exception
        self.logger = self._get_logger()

    def _get_logger(self):
        if hasattr(settings, 'LOGGABLE_LOGGER'):
            return logging.getLogger(settings.LOGGABLE_LOGGER)
        else:
            logging.config.dictConfig(self._get_default_log_config())
            return logging.getLogger('request_response')

    @staticmethod
    def _get_default_log_config():
        return default_log_config

    @staticmethod
    def _get_params(request):
        if request.method == 'GET':
            return request.GET
        else:
            post_params = dict(request.POST)
            del post_params['csrfmiddlewaretoken']
            return post_params


    def as_view(self, *args, **kwargs):

        self.view_func = self.view_func.as_view(*args, **kwargs)

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
                if hasattr(response,'context_data'):
                    if 'form' in response.context_data.keys():
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
