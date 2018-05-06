import json
import os

from core.target import TargetWriter


class VSTargetWriter(TargetWriter):
    def __init__(self, file_path=os.path.join('config', '__init__.py')):
        self.path = file_path

    def write(self, target):
        import py_compile

        with open(self.path, 'wb') as f:
            f.write('targets=')
            json.dump(target, f)

        py_compile.compile(self.path)
        os.remove(self.path)
