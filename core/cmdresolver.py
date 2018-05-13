import os


class CmdResolver(object):
    path_separator = os.pathsep

    def __init__(self, envs=['PATH'], paths=[]):
        for env in envs:
            env_paths = os.getenv(env).split(os.pathsep)
            paths.extend(env_paths)

        self.paths = paths
        self.cmd_dict = {}
        self.__resolve()

    @property
    def command_dict(self):
        return self.cmd_dict

    def __resolve(self):
        for p in self.paths:
            expand_path = os.path.expandvars(p)
            try:
                exe_files = [
                    f for f in os.listdir(expand_path)
                    if self.__is_executable(os.path.join(expand_path, f))
                ]
                if exe_files:
                    self.cmd_dict[expand_path] = exe_files
            except WindowsError as w:
                print 'Ignored: {}'.format(w)
                continue

    def __is_executable(self, file_path):
        if 'nt' in os.name:
            path_ext = os.getenv('PATHEXT').split(self.path_separator)
            fpath = str(file_path).lower()
            return os.path.isfile(fpath) and \
                [ext for ext in path_ext if fpath.endswith(ext.lower())]
        elif 'posix' in os.name:
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)
        return False

    def dump(self, file_path=os.path.join('..', 'config', 'cmds.py')):
        import json
        import py_compile

        with open(file_path, 'wb') as f:
            f.write('cmds=')
            json.dump(self.cmd_dict, f)

        py_compile.compile(file_path)
        os.remove(file_path)
