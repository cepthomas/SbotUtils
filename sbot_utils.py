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
class SbotUtilsTreeCommand(sublime_plugin.WindowCommand): # TODO was in Sidebar
    ''' Run tree command to a new view. '''

    def run(self, paths=None):
        if len(paths) > 0:
            path = paths[0] if os.path.isdir(paths[0]) else os.path.split(paths[0])[0]
            cmd = f'tree "{path}" /a /f'  # Linux needs this installed.
            try:
                cp = subprocess.run(cmd, universal_newlines=True, capture_output=True, shell=True, check=True)
                sc.create_new_view(self.window, cp.stdout)
            except Exception as e:
                sc.create_new_view(self.window, f'Well, that did not go well: {e}\n{cp.stderr}')

    def is_visible(self, paths):
        vis = platform.system() == 'Windows' and len(paths) > 0
        return vis


