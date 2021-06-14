from framework.util.logger.Level import Level
from framework.util.logger.LogMethod import LogMethod
from framework.util.project.Project import Project


class LogConfig(object):
    LOG_LEVEL = Level.INFO
    LOG_TO = LogMethod.FILE
    LOG_FILE = Project.ROOT + "logs/framework/framework-rent.log"
