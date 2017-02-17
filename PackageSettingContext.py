# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin

def is_integer(string):
    try:
        int(string)
    except:
        return False
    return int(string) == float(string)

def setting_advanced_get(settings, key):
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

def get_setting(key, operator, operand, test_settings=None):

    if not key.startswith('package_setting.'):
        return

    key = key[len('package_setting.'):]

    if not '.' in key:
        sublime.error_message('[PackageSettingContext] Unvalid key: ' + key)
        return

    package, key = key.split('.', 1)

    settings = test_settings or sublime.load_settings(package + '.sublime-settings')
    setting = setting_advanced_get(settings, key)

    if operator == sublime.OP_EQUAL:
        return setting == operand
    elif operator == sublime.OP_NOT_EQUAL:
        return settings != operand

class PackageSettingContext(sublime_plugin.EventListener):

    def on_query_context(self, view, key, operator, operand, match_all):
        return get_setting(key, operator, operand)
