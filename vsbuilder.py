import os
import argparse
import subprocess as sub
import configloader as cloader

import config


targets = dict(config.targets)


class VSCommander(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='quick',
                                              description='A convenient command '
                                                          'to build source code.')

        subparser = self.parser.add_subparsers()
        buildparser = subparser.add_parser('build',
                                           help='Build one or more targets.')
        buildparser.add_argument('targets', help='One or more targets.',
                                 nargs='*')
        buildparser.add_argument('-c', '--custom',
                                 help='Run custom command passed by user.',
                                 nargs='?', dest='uc')
        # buildparser.add_argument('-r', '--rebuild',
        #                          help='Rebuild one or more targets.',
        #                          nargs='?', dest='rebuild', default='')
        buildparser.set_defaults(execute=BuildRunner().build)

        showparser = subparser.add_parser('show', help='Show all targets.')
        showparser.set_defaults(execute=ShowRunner.show)

        self.command = self.parser.parse_args()

    def run(self):
        self.command.execute(self.command)


class ShowRunner(object):

    @staticmethod
    def show(cmd=None, keys=targets.keys(), vals=targets.values()):
        max_key = max([len(k) for k in keys])
        max_val = max([len(v) for v in vals])
        for k in sorted(keys):
            value = targets[k]
            if isinstance(value, dict) and 'location' in value:
                value = value['location']
            print '{key:{kw}}{space:10}{val:{valw}}'.format(key=k, kw=max_key,
                                                            val=value,
                                                            valw=max_val,
                                                            space='')


class BuildRunner(object):

    def __init__(self):
        self.config = cloader.VSConfigLoader()
        self.fail_list = []
        self.success_list = []

    def build(self, cmd):
        cmd_targets = cmd.targets
        uc = cmd.uc
        for tg in cmd_targets:
            if tg not in targets:
                self.suggestion(tg)
                return

        for tg in cmd_targets:
            self.__build_target(tg, uc)

        self.report()

    def suggestion(self, target):
        sk = [key for key in targets.keys() if key.find(target) != -1]
        if sk:
            print 'Suggestion for "{}":'.format(target)
            ShowRunner.show(keys=sk)
        else:
            print 'No suggestion for "{}".'.format(target)

    def __build_target(self, target, custom_command=None):
        build_obj = targets.get(target)
        if isinstance(build_obj, list):
            self.__build_list(build_obj, custom_command)
        elif isinstance(build_obj, dict):
            self.__build_dict(build_obj, custom_command)

    def __build_list(self, blist, custom_command):
        for tg in blist:
            self.__build_target(tg, custom_command)

    def __build_dict(self, bdict, custom_command):
        loc = bdict['location']
        cmd = custom_command or bdict['command']
        cmd_list = cmd.split()
        cmd_list[0] = self.config.get_command(cmd_list[0])
        cmd = ' '.join(cmd_list)

        os.chdir(loc)
        print 'Running {}'.format(cmd)
        ret = sub.call(cmd)
        if ret != 0:
            self.fail_list.append(loc)
        else:
            self.success_list.append(loc)

    def report(self):
        end_line_no = 1
        mul_char = 35
        print "\n" * end_line_no
        print "=" * mul_char + "REPORT" + "=" * mul_char
        print "FAIL: %d" % len(self.fail_list)
        for f in self.fail_list:
            print f
        print "\n"

        print "SUCCESS: %d" % len(self.success_list)
        # for s in successList:
        #     print s
        print "\n"

        # print "COPIED: %d" % len(copiedList)
        # for f in copiedList:
        #     print f

        print "=" * mul_char + "REPORT" + "=" * mul_char
        print "\n" * end_line_no
