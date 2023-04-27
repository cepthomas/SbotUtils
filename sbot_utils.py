import sys
import os
import re
import platform
import pathlib
import subprocess
import sublime
import sublime_plugin
from .sbot_common import *

UTILS_SETTINGS_FILE = "SbotUtils.sublime-settings"


#-----------------------------------------------------------------------------------
class SbotGeneralEvent(sublime_plugin.EventListener):
    ''' Listener for window events of interest. '''

    def on_selection_modified(self, view):
        ''' Show the abs position in the status bar. '''
        if len(view.sel()) > 0:
            pos = view.sel()[0].begin()
            view.set_status("position", f'Pos {pos}')


#-----------------------------------------------------------------------------------
class SbotSplitViewCommand(sublime_plugin.WindowCommand):
    ''' Toggles between split file views. '''

    def run(self):
        window = self.window

        if len(window.layout()['rows']) > 2:
            # Remove split.
            window.run_command("focus_group", {"group": 1})
            window.run_command("close_file")
            window.run_command("set_layout", {"cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]]})
        else:
            # Add split.
            sel_row, _ = window.active_view().rowcol(window.active_view().sel()[0].a)  # current sel
            window.run_command("set_layout", {"cols": [0.0, 1.0], "rows": [0.0, 0.5, 1.0], "cells": [[0, 0, 1, 1], [0, 1, 1, 2]]})
            window.run_command("focus_group", {"group": 0})
            window.run_command("clone_file")
            window.run_command("move_to_group", {"group": 1})
            window.active_view().run_command("goto_line", {"line": sel_row})


#-----------------------------------------------------------------------------------
class SbotCheatsheetCommand(sublime_plugin.WindowCommand):

    def run(self):
        settings = sublime.load_settings(UTILS_SETTINGS_FILE)

        fn = settings.get('cheat_sheet_path')
        if fn is not None and os.path.exists(fn):
            self.window.open_file(fn)
        else:
            sublime.error_message(f'Invalid file: {fn}')            
        # fn = os.path.join(sublime.packages_path(), 'SbotUtils', 'ST-commands.md')

    def is_visible(self):
        settings = sublime.load_settings(UTILS_SETTINGS_FILE)
        fn = settings.get('cheat_sheet_path')
        return fn is not None

#-----------------------------------------------------------------------------------
class SbotTerminalCommand(sublime_plugin.WindowCommand):
    ''' Open term here. '''

    def run(self):
        fn = self.window.active_view().file_name()
        path = os.path.split(fn)[0]

        cmd = '???'
        if platform.system() == 'Windows':
            ver = float(platform.win32_ver()[0])
            # slog(CAT_INF, ver)
            cmd = f'wt -d "{path}"' if ver >= 10 else f'cmd /K "cd {path}"'
        else:
            cmd = f'gnome-terminal --working-directory="{path}"'

        subprocess.run(cmd, shell=False, check=False)

    def is_visible(self):
        fn = self.window.active_view().file_name()
        return fn is not None


#-----------------------------------------------------------------------------------
class SbotExecCommand(sublime_plugin.WindowCommand):
    ''' Simple executioner for exes/cmds without args, like you double clicked it.
    Assumes file associations are set to preferences.
    '''

    def run(self):
        fn = self.window.active_view().file_name()

        try:
            cmd = [fn] #['python', fn] if fn.endswith('.py') else [fn]

            cp = subprocess.run(cmd, universal_newlines=True, capture_output=True, shell=True, check=True)
            if(len(cp.stdout) > 0):
                create_new_view(self.window, cp.stdout)
        except Exception as e:
            sublime.message_dialog(f'Unhandled exception: {e}!\nGo look in the log.\n')

    def is_visible(self):
        # Assumes caller knows what they are doing.
        fn = self.window.active_view().file_name()
        if fn is None:
            return False
        else:
            ext = os.path.splitext(fn)[1]
            return True # ext in ['.html', '.svg', '.py', etc]


#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------


#   { "command": "open_context_path" }, TODO

# C:\Users\cepth\OneDrive\OneDrive Documents\tech\sublime\ST\Default\open_context_url.py


rex = re.compile(
    r'''(?x)
    \b(?:
        https?://(?:(?:[\w\d\-]+(?:\.[\w\d\-.]+)+)|localhost)|  # http://
        www\.[\w\d\-]+(?:\.[\w\d\-.]+)+                         # www.
    )
    /?[\w\d\-.?,!'(){}\[\]/+&@%$#=:"|~;]*                       # path path and query string
    [\w\d\-~:/#@$*+=]                                           # allowed end chars
    ''')


class OpenContextUrlCommand(sublime_plugin.TextCommand):
    def name(self):
        return 'old_open_context_path'

    def run(self, edit, event):
        path = self.find_path(event)
        webbrowser.open_new_tab(path)

    def is_visible(self, event):
        return self.find_path(event) is not None

    def find_path(self, event):
        pt = self.view.window_to_text((event["x"], event["y"]))
        line = self.view.line(pt)

        line.a = max(line.a, pt - 1024)
        line.b = min(line.b, pt + 1024)

        text = self.view.substr(line)

        it = rex.finditer(text)

        for match in it:
            if match.start() <= (pt - line.a) and match.end() >= (pt - line.a):
                path = text[match.start():match.end()]
                if path[0:3] == "www":
                    return "http://" + path
                else:
                    return path

        return None

    def description(self, event):
        path = self.find_path(event)
        if len(path) > 64:
            path = path[0:64] + "..."
        return "Open " + path

    def want_event(self):
        return True
