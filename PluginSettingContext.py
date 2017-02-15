# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin

def is_integer(string):
    try:
        int(string)
    except:
        return False
    return int(string) == float(string)

def get_setting(settings, key):
    """Allow object.key.3 kind of key.
    This example will return '!' for this settings:
    {
        "object": {
            "key": ["this", "is", "cool", "!"]
        }
    }
    """
    keys = key.split('.')
    value = settings.get(keys[0])
    for i, key in enumerate(keys[1:]):
        if isinstance(value, dict):
            try:
                value = value[key]
            except KeyError:
                return
        elif isinstance(value, list) and is_integer(key):
            try:
                value = value[int(key)]
            except IndexError:
                return
        else:
            return
    return value

def quick_tests():
    # CSW: ignore
    print(get_setting(sublime.load_settings('Package Control.sublime-settings'),
                      'package_profiles.Binaries Only.files_to_ignore.0'))


class PluginSettingContext(sublime_plugin.EventListener):

    def on_query_context(self, view, key, operator, operand, match_all):

        if not key.startswith('plugin_setting.'):
            return

        key = key[len('plugin_setting.'):]
        package, setting_name = key.split('.', 1)
        settings = sublime.load_settings(package + '.sublime-settings')
        setting = settings.get(setting_name)
        if operator == sublime.OP_EQUAL:
            return setting == operand
        elif operator == sublime.OP_NOT_EQUAL:
            return settings != operand
