import logging


class Logger:

    @staticmethod
    def get_logger(application):
        logger = logging.getLogger(application)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.getLevelName(logging.INFO))
        log_format = '%(asctime)s %(threadName)-10s %(process)d %(levelname)-8s (%(filename)s:%(lineno)d) %(message)s'
        stream_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(stream_handler)
        return logger

logger = Logger.get_logger("fastapi")
