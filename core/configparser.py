import ConfigParser as cfg


class ConfigLoader(object):
    def __init__(self, cfg_file):
        self.buildConfig = cfg.SafeConfigParser()
        self.buildConfig.read(cfg_file)

    @property
    def config(self):
        return self.buildConfig
