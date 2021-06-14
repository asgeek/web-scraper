from framework.util.logger.LoggerUtil import LoggerUtil
from framework.util.logger.Level import Level


class Log(object):
    # TODO: Fine tune log filtering

    @staticmethod
    def debug(message):
        level = Level.DEBUG
        not_allowed_levels = [Level.TRACE, Level.WARNING, Level.INFO, Level.FATAL, Level.ERROR, Level.OFF]
        LoggerUtil.write_log(message, level, not_allowed_levels)

    @staticmethod
    def error(message):
        level = Level.ERROR
        not_allowed_levels = [Level.OFF]
        LoggerUtil.write_log(message, level, not_allowed_levels)

    @staticmethod
    def fatal(message):
        level = Level.FATAL
        not_allowed_levels = [Level.OFF]
        LoggerUtil.write_log(message, level, not_allowed_levels)

    @staticmethod
    def info(message):
        level = Level.INFO
        not_allowed_levels = [Level.OFF]
        LoggerUtil.write_log(message, level, not_allowed_levels)

    @staticmethod
    def trace(message):
        level = Level.TRACE
        not_allowed_levels = [Level.DEBUG, Level.WARNING, Level.INFO, Level.FATAL, Level.ERROR, Level.OFF]
        LoggerUtil.write_log(message, level, not_allowed_levels)

    @staticmethod
    def warning(message):
        level = Level.WARNING
        not_allowed_levels = [Level.OFF]
        LoggerUtil.write_log(message, level, not_allowed_levels)
