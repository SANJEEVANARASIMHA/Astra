import logging
import yaml

with open('../logs/api/api.yaml', 'r') as stream:
    logger_config = yaml.load(stream, yaml.FullLoader)
logging.config.dictConfig(logger_config)
logger = logging.getLogger('API-Logs-Tracking')