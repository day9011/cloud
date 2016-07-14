from logging import config as logging_config

def main(*a, **kw):
    from app import app, auth
    auth.init_auth('conf/config.yml')
    app.run(*a, **kw)

def config_logging(log_cfg):
    logging_config.fileConfig(log_cfg)

if __name__ == '__main__':
    config_logging('conf/logging.ini')
    main('0.0.0.0', port=8000, debug=True)