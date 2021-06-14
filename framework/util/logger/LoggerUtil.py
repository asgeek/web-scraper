from config.LogConfig import LogConfig
from framework.util.logger.LogMethod import LogMethod
from framework.util.logger.Level import Level
from datetime import datetime
import codecs


class LoggerUtil(object):

    @staticmethod
    def write_log(message, log_level, not_allowed_levels):
        level = LogConfig.LOG_LEVEL
        log_out = LogConfig.LOG_TO
        log_path = LogConfig.LOG_FILE
        if level not in not_allowed_levels:
            if log_out == LogMethod.CONSOLE:
                print(LoggerUtil.format_log_out(message, log_level))
            elif log_out == LogMethod.FILE:
                LoggerUtil.write_to_file(log_path, LoggerUtil.format_log_out(message, log_level))

    @staticmethod
    def format_log_out(message, level):
        date_time = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
        log_line = '{0} <{1}> {2}'.format(date_time, level, message)
        return log_line

    @staticmethod
    def write_to_file(file_name, log_line):
        with codecs.open(file_name, "a", "utf-8-sig") as text_file:
            text_file.write(log_line + "\n")
