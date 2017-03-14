# -*- encoding: utf-8 -*-

"""
Quick tests to test the PackageSettingContext function.

To run them, paste

from package_setting_context.all.tests import main; main()

in the console,

, save this file, and the output's in the console!
"""

from .PackageSettingContext import get_setting
import sublime
import sys

class FakeSettings:

    """Only what's needed"""

    def __init__(self, data):
        self.data = data

    def get(self, key, default=None):
        return self.data.get(key, default)

def main():
    sys.stdout.write('----------------------------------------------\n')
    sys.stdout.write('| PackageSettingContext.tests: Running tests |\n')
    sys.stdout.write('----------------------------------------------\n')
    settings = FakeSettings({
        'first': False,
        'second': 4,
        'third': 'hello',
        'fourth': {
            'this': ['is', {
                'cool': ["right", "?"]
            }]
        }
    })

    tests = [
        ['package_settings.notice.the.s', sublime.OP_EQUAL, True, None],
        ['package_setting.TestSetting.first', sublime.OP_EQUAL, False, True],
        ['package_setting.TestSetting.second', sublime.OP_EQUAL, 4, True],
        ['package_setting.TestSetting.third', sublime.OP_NOT_EQUAL, None, True],
        ['package_setting.TestSetting.fourth', sublime.OP_NOT_EQUAL, {}, True],
        ['package_setting.TestSetting.fourth.this.1.cool.1', sublime.OP_EQUAL, '?', True],
    ]

    for key, operand, operator, expected in tests:
        result = get_setting(key, operand, operator, test_settings=settings)
        if result != expected:
            sys.stdout.write("\nError: the key {!r} return {!r} instead of {!r}".format(key, result, expected))
