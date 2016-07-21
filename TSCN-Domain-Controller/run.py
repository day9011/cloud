#!/usr/bin/python
from utils.auth import init_auth
from logging import config as logging_config

def config_logging(log_cfg):
    logging_config.fileConfig(log_cfg)

if __name__ == "__main__":
    init_auth('conf/config.yml')
    from app import domain_controller
    config_logging('conf/logging.ini')
    domain_controller.run(host = "0.0.0.0", port=9999, debug = True)
