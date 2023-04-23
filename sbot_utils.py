import sys
import os
import platform
import pathlib
import subprocess
import sublime
import sublime_plugin

try:
    import SbotCommon.sbot_common as sbot
except ModuleNotFoundError as e:
    sublime.message_dialog('SbotUtils plugin requires SbotCommon plugin')
    raise ImportError('SbotUtils plugin requires SbotCommon plugin')

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


#-----------------------------------------------------------------------------------
class SbotTerminalCommand(sublime_plugin.WindowCommand):
    ''' Open term here. '''

    def run(self):
        fn = self.window.active_view().file_name()
        path = os.path.split(fn)[0]

        cmd = '???'
        if platform.system() == 'Windows':
            ver = float(platform.win32_ver()[0])
            sbot.slog(sbot.CAT_INF, ver)
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
            cmd = ['python', fn] if fn.endswith('.py') else [fn]

            cp = subprocess.run(cmd, universal_newlines=True, capture_output=True, shell=True, check=True)
            if(len(cp.stdout) > 0):
                sbot.create_new_view(self.window, cp.stdout)
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
