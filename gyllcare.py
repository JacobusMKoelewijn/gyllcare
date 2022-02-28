import gunicorn.app.base
from key import keys
from gyllcare.config import IN_PRODUCTION
from gyllcare.app import create_app
from gyllcare.app.main.extensions import socketio

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
    if IN_PRODUCTION:
        options = {
            'bind': '%s:%s' % (keys.get('GYLLCARE_IP_ADDRESS'), '9000'),
            'workers': 1,
            'timeout': 120,
            'worker_class': "gevent",
        }
        StandaloneApplication(create_app(), options).run()
    else:
        app = create_app()
        socketio.run(app)
        print("Starting in development mode.")

        # Does this run the app twice??