import os
from core.configparser import ConfigLoader


class VSConfigLoader(ConfigLoader):
    allow_command = ['make', 'ant', 'ant.bat', 'mvn', 'mvn.cmd', 'gradle', 'gradle.bat']

    def __init__(self, cf=os.path.join('config', 'buildConfig.ini')):
        super(VSConfigLoader, self).__init__(cf)
        self.config_sig = os.path.getmtime(cf)
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
        try:
            last_sig = 0
            signature_file = os.path.join('config', 'signature')
            with open(signature_file, 'rb') as f:
                last_sig = int(f.read())

            if self.config_sig != last_sig:
                self.__build_cmd_dict()
                self.__dump_signature(signature_file)
        except IOError:
            self.__build_cmd_dict()
            self.__dump_signature(signature_file)

        from config import cmds
        return cmds.cmds

    def __dump_signature(self, sig_file):
        with open(sig_file, 'wb') as f:
            f.write(str(self.config_sig))

    def __build_cmd_dict(self):
        from core import cmdresolver
        environments = ['ANT_HOME', 'MAVEN_HOME', 'GRADLE_HOME', 'PATH']
        paths = [self.config.get('default', 'ant-home'),
                 self.config.get('default', 'maven-home'),
                 self.config.get('default', 'gradle-home')]
        cr = cmdresolver.CmdResolver(envs=environments, paths=paths)
        cr.dump()

    def get_command(self, cmd):
        if cmd in self.allow_command:
            if str(cmd).rfind(os.extsep) == -1:
                # commands don't have extension
                return self.__handle_command_on_different_os(cmd) or ''

    def __handle_command_on_different_os(self, cmd):
        if 'nt' in os.name:
            cmd2find = [cmd + ext for ext in ['.exe', '.cmd', '.bat']]
            for c in cmd2find:
                retC = self.__find_command(c)
                if retC:
                    return retC
        elif 'posix' in os.name:
            return self.__find_command(cmd)

    def __find_command(self, cmd):
        for key, vlist in self.cmdDict.iteritems():
            if cmd in vlist:
                return os.path.join(key, cmd)
