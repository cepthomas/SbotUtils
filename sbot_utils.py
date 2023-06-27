import sys
import os
import re
import platform
import pathlib
import subprocess
import sublime
import sublime_plugin
from . import sbot_common as sc


# TODO Simple git tools: diff, commit, push? https://github.com/kemayo/sublime-text-git.

UTILS_SETTINGS_FILE = "SbotUtils.sublime-settings"


#-----------------------------------------------------------------------------------
class SbotGeneralEvent(sublime_plugin.EventListener):
    ''' Listener for window events of interest. '''

    def on_selection_modified(self, view):
        ''' Show the abs position in the status bar. '''
        caret = sc.get_single_caret(view)
        view.set_status("position", f'???' if caret is None else f'Pos {caret}')


#-----------------------------------------------------------------------------------
class SbotUtilsSplitViewCommand(sublime_plugin.WindowCommand):
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
            caret = sc.get_single_caret(window.active_view())
            sel_row, _ = window.active_view().rowcol(caret)  # current sel
            window.run_command("set_layout", {"cols": [0.0, 1.0], "rows": [0.0, 0.5, 1.0], "cells": [[0, 0, 1, 1], [0, 1, 1, 2]]})
            window.run_command("focus_group", {"group": 0})
            window.run_command("clone_file")
            window.run_command("move_to_group", {"group": 1})
            window.active_view().run_command("goto_line", {"line": sel_row})


#-----------------------------------------------------------------------------------
class SbotUtilsTerminalCommand(sublime_plugin.WindowCommand):
    ''' Open terminal here. '''

    def run(self):
        fn = self.window.active_view().file_name()
        path = os.path.split(fn)[0]

        cmd = '???'
        if platform.system() == 'Windows':
            ver = float(platform.win32_ver()[0])
            # slog(sc.CAT_INF, ver)
            cmd = f'wt -d "{path}"' if ver >= 10 else f'cmd /K "cd {path}"'
        else:
            cmd = f'gnome-terminal --working-directory="{path}"'

        subprocess.run(cmd, shell=False, check=False)

    def is_visible(self):
        fn = self.window.active_view().file_name()
        return fn is not None


#-----------------------------------------------------------------------------------
class SbotUtilsExecCommand(sublime_plugin.WindowCommand):
    '''
    Simple executioner for exes/cmds without args, like you double clicked it.
    Assumes file associations are set to preferences.
    '''

    def run(self):
        fn = self.window.active_view().file_name()
        if fn is not None:
            ext = os.path.splitext(fn)[1]
            if ext in ['.py']:
                sc.run_script(fn, self.window)
            else:
                sc.start_file(fn)

    def is_visible(self):
        # Assumes caller knows what they are doing.
        fn = self.window.active_view().file_name()
        if fn is None:
            return False
        else:
            return True


#-----------------------------------------------------------------------------------
class SbotUtilsRunScriptCommand(sublime_plugin.WindowCommand):
    ''' Script runner. Currently only python. '''

    def run(self):
        fn = self.window.active_view().file_name()
        sc.run_script(fn, self.window)

    def is_visible(self):
        vis = False
        fn = self.window.active_view().file_name()
        if fn is not None:
            ext = os.path.splitext(fn)[1]
            vis = ext in ['.py'] and (platform.system() == 'Windows' or platform.system() == 'Linux')
        return vis
