import multiprocessing
from gyllcare.main import create_app
import gunicorn.app.base


# def number_of_workers():
    # return 1
    # return (multiprocessing.cpu_count() * 2) + 1


# def handler_app(environ, start_response):
#     response_body = b'Works fine'
#     status = '200 OK'

#     response_headers = [
#         ('Content-Type', 'text/plain'),
#     ]

#     start_response(status, response_headers)

#     return [response_body]


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '%s:%s' % ('192.168.178.31', '9000'),
        'workers': 1,
        'timeout': 120,
        'worker_class': "gevent",
    }
    StandaloneApplication(create_app, options).run()