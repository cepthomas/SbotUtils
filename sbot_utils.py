import sys
import os
import pathlib
import sublime
import sublime_plugin


UTILS_SETTINGS_FILE = "SbotUtils.sublime-settings"


#-----------------------------------------------------------------------------------
class SbotGeneralEvent(sublime_plugin.EventListener):
    ''' Listener for window events of interest. '''

    def on_selection_modified(self, view):
        ''' Show the abs position in the status bar. '''
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
