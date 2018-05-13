from core import target

keys_need_update = ['src', 'java', 'lib', 'exec', 'cmd', 'build', 'sys', 'test']


class VSTargetScanner(target.TargetScanner):
    def __init__(self):
        pass

    def _determine(self, path, file_list):
        d = dict(location=path)
        # if both and build file and makefile exist, ant build file has
        # higher priority
        if 'build.xml' in file_list:
            d['command'] = 'ant'
        elif 'makefile' in file_list or 'Makefile' in file_list:
            d['command'] = 'make cfg=release'
        elif 'pom.xml' in file_list:
            d['command'] = 'mvn package'
        elif 'gradle.properties' in file_list:
            d['command'] = 'gradle'
        else:
            return {}

        return d

    @staticmethod
    def _get_special_kw_list():
        return keys_need_update
