import logging


class LoggerConfiguration:
    def configure_console_handler(self):
        log_format = "%(asctime)s.%(msecs)03d %(levelname)s %(process)d --- [%(processName)s] %(module)s : %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"
        logging.basicConfig(format=log_format, datefmt=date_format, level=logging.DEBUG)
