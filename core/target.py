import os


class TargetScanner(object):
    def __init__(self):
        pass

    def scan(self, path2scan, ignore_path_list):
        dict_result = {}
        for root, ds, fs in os.walk(path2scan):
            if root in ignore_path_list:
                ds[:] = []
                continue

            child_dict = self._determine(root, fs)
            if child_dict:
                target_name = self.get_target_name(root)
                # handle special keywords
                target_name = self._handle_special_keywords(root, target_name)
                # handle duplicated target
                target_name = self.handle_duplicated_name(dict_result, target_name)

                dict_result[target_name] = child_dict

        return dict_result

    def _handle_special_keywords(self, path, name):
        skw = self._get_special_kw_list()
        if skw and name in skw:
            pref = self.get_prefix_name(path)
            return '%s-%s' % (pref, name)
        return name

    @staticmethod
    def handle_duplicated_name(a_dict, name):
        ret_name = name
        idx = 1
        while ret_name in a_dict:
            ret_name = '%s%d' % (name, idx)
            idx += 1
        return ret_name

    @staticmethod
    def _get_special_kw_list():
        return []

    def _determine(self, *thing_to_determine):
        pass

    @staticmethod
    def get_prefix_name(root):
        last_sep = root.rfind(os.sep)
        near_last_sep = root.rfind(os.sep, 0, last_sep - 1)
        pref = root[near_last_sep + 1: last_sep]
        return pref.lower()

    @staticmethod
    def get_target_name(root):
        last_sep = root.rfind(os.sep)
        target_name = root[last_sep + 1:]
        return target_name.lower()


class TargetWriter(object):
    def __init__(self):
        pass

    def write(self, target):
        pass
