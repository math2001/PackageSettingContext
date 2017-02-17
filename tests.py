# -*- encoding: utf-8 -*-

"""
Quick tests to test the PackageSettingContext function.

To run them, uncomment the 'main()' at the end, save this file, and the output's in the console!
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
    sys.stdout.write('----------------------------------------------')
    sys.stdout.write('| PackageSettingContext.tests: Running tests |')
    sys.stdout.write('----------------------------------------------')
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
        ['plugin_settings.notice.the.s', sublime.OP_EQUAL, True, None],
        ['plugin_setting.TestSetting.first', sublime.OP_EQUAL, False, True],
        ['plugin_setting.TestSetting.second', sublime.OP_EQUAL, 4, True],
        ['plugin_setting.TestSetting.third', sublime.OP_NOT_EQUAL, None, True],
        ['plugin_setting.TestSetting.fourth', sublime.OP_NOT_EQUAL, {}, True],
        ['plugin_setting.TestSetting.fourth.this.1.cool.1', sublime.OP_EQUAL, '?', True],
    ]

    for key, operand, operator, expected in tests:
        result = get_setting(key, operand, operator, test_settings=settings)
        if result != expected:
            sys.stdout.write("\nError: the key {!r} return {!r} instead of {!r}".format(key, result, expected))

# main()
