import os


class Project(object):
    ROOT = os.path.dirname(os.path.abspath(__file__)) + "/../../../"
    OUTPUT = ROOT + "output/"
    INPUT = ROOT + "input/"
