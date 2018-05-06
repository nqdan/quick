import os
from core.configparser import ConfigLoader


class VSConfigLoader(ConfigLoader):

    def __init__(self, cf=os.path.join('config', 'buildConfig.ini')):
        super(VSConfigLoader, self).__init__(cf)
        self.cmdDict = self.__resolve_command()

    def get_root_path(self):
        return self.config.get('default', 'dev-home')

    def get_ignore_path(self):
        paths = self.config.get('exclude', 'exclude-paths')
        if paths:
            return paths.split(',')
        return []

    def get_custom_target(self):
        ctlist = self.config.items('custom-targets')
        return {tup[0]: tup[1].split(',') for tup in ctlist}

    def __resolve_command(self):
        # do not allow users to pass any command
        ant_home = os.getenv('ANT_HOME', self.config.get('default', 'ant-home'))
        maven_home = os.getenv('MAVEN_HOME', self.config.get('default', 'maven-home'))
        gradle_home = os.getenv('GRADLE_HOME', self.config.get('default', 'gradle-home'))

        antC = os.path.join(ant_home, 'bin', 'ant')
        mvnC = os.path.join(maven_home, 'bin', 'mvn')
        gradleC = os.path.join(gradle_home, 'bin', 'gradle')
        if os.name == 'nt':
            antC += '.bat'
            mvnC += '.cmd'
            gradleC += '.bat'

        result = {
            'make': '',
            'ant': antC,
            'mvn': mvnC,
            'gradle': gradleC
        }

        return result

    def get_command(self, cmd):
        return self.cmdDict.get(cmd, '')
