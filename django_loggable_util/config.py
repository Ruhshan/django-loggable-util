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
