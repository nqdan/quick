from configloader import VSConfigLoader
from core.target import TargetScanner
from vsbuildwriter import VSTargetWriter
from vstargetscanner import VSTargetScanner


class VSTargetBuilder(object):
    def __init__(self):
        self.config = VSConfigLoader()
        self.scanner = VSTargetScanner()
        self.writer = VSTargetWriter()

    def build(self):
        root_dir = self.config.get_root_path()
        ignore_path_names = self.config.get_ignore_path()

        custom_target = self.config.get_custom_target()
        auto_target = self.scanner.scan(root_dir, ignore_path_names)
        all_target = self.unify(custom_target, auto_target)

        self.writer.write(all_target)
        print all_target

    @staticmethod
    def unify(custom_target, auto_target):
        result = {}
        result.update(custom_target)

        for k, v in auto_target.iteritems():
            new_k = k
            if k in custom_target:
                new_k = TargetScanner.handle_duplicated_name(custom_target, k)
            result[new_k] = v

        return result

if __name__ == "__main__":
    vst = VSTargetBuilder()
    vst.build()
