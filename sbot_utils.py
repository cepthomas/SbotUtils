import sys
import os
import re
import platform
import pathlib
import subprocess
import shutil
import sublime
import sublime_plugin
from . import sbot_common as sc


#-----------------------------------------------------------------------------------
class SbotGeneralEvent(sublime_plugin.EventListener):
    ''' Listener for window events of interest. '''

    def on_selection_modified(self, view):
        ''' Show the abs position in the status bar. '''
        caret = sc.get_single_caret(view)
        view.set_status("position", f'???' if caret is None else f'Pos {caret}')


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
            caret = sc.get_single_caret(window.active_view())
            sel_row, _ = window.active_view().rowcol(caret)  # current sel
            window.run_command("set_layout", {"cols": [0.0, 1.0], "rows": [0.0, 0.5, 1.0], "cells": [[0, 0, 1, 1], [0, 1, 1, 2]]})
            window.run_command("focus_group", {"group": 0})
            window.run_command("clone_file")
            window.run_command("move_to_group", {"group": 1})
            window.active_view().run_command("goto_line", {"line": sel_row})


#-----------------------------------------------------------------------------------
class SbotTreeCommand(sublime_plugin.WindowCommand):
    ''' Run tree command to a new view. '''

    def run(self, paths=None):
        dir, fn, path = _get_path_parts(self.window.active_view(), paths)
        cmd = f'tree "{dir}" /a /f'  # Linux needs this installed.
        try:
            cp = subprocess.run(cmd, universal_newlines=True, capture_output=True, shell=True, check=True)
            sc.create_new_view(self.window, cp.stdout)
        except Exception as e:
            sc.create_new_view(self.window, f'Well, that did not go well: {e}\n{cp.stderr}')

    def is_visible(self, paths=None):
        dir, fn, path = _get_path_parts(self.window.active_view(), paths)
        vis = platform.system() == 'Windows'
        return vis


#-----------------------------------------------------------------------------------
class SbotExecCommand(sublime_plugin.WindowCommand): 
    '''
    Simple executioner for exes/cmds without args, like you double clicked it.
    Assumes file associations are set to preferences.
    Also runs scripts if supported. Currently only python. Creates a new view with output.
    Supports context and sidebar menus.
    '''

    def run(self, paths=None):
        dir, fn, path = _get_path_parts(self.window.active_view(), paths)

        try:
            # Determine if it is a supported script type.
            _, ext = os.path.splitext(fn)
            if ext in ['.py', '.lua', '.cmd', '.bat']: # list of known script types/execute patterns
                cmd = '???'
                if ext == '.py':
                    cmd = f'python "{path}"'
                elif ext == '.lua':
                    cmd = f'lua "{path}"' # support LUA_PATH?
                else:
                    cmd = path
                data = subprocess.run(cmd, capture_output=True, text=True)
                output = data.stdout
                errors = data.stderr
                if len(errors) > 0:
                    output = output + '============ stderr =============\n' + errors
                sc.create_new_view(self.window, output)
            else:
                if platform.system() == 'Darwin':
                    ret = subprocess.call(('open', path))
                elif platform.system() == 'Windows':
                    os.startfile(path)
                else:  # linux variants
                    re = subprocess.call(('xdg-open', path))
        except Exception as e:
            sc.slog(sc.CAT_ERR, f'{e}')

    def is_visible(self, paths=None):
        # Ensure valid file only.
        dir, fn, path = _get_path_parts(self.window.active_view(), paths)
        return fn is not None


#-----------------------------------------------------------------------------------
class SbotTerminalCommand(sublime_plugin.WindowCommand):
    ''' Open term in this directory. Supports context and sidebar menus. '''

    def run(self, paths=None):
        dir, fn, path = _get_path_parts(self.window.active_view(), paths)

        cmd = '???'
        if platform.system() == 'Windows':
            ver = float(platform.win32_ver()[0])
            # sc.slog(sc.CAT_INF, ver)
            cmd = f'wt -d "{dir}"' if ver >= 10 else f'cmd /K "cd {dir}"'
        else: # mac/linux
            cmd = f'gnome-terminal --working-directory="{dir}"'
        subprocess.run(cmd, shell=False, check=False)


#-----------------------------------------------------------------------------------
class SbotCopyNameCommand(sublime_plugin.WindowCommand):
    ''' Get file or directory name to clipboard. Supports context and sidebar menus. '''

    def run(self, paths=None):
        dir, fn, path = _get_path_parts(self.window.active_view(), paths)
        # sc.slog(sc.CAT_DBG, f'SbotCopyNameCommand, {dir}, {fn}, {path}')
        sublime.set_clipboard(os.path.split(path)[-1])

    def is_visible(self, paths=None):
        # Ensure valid file only.
        dir, fn, path = _get_path_parts(self.window.active_view(), paths)
        return dir is not None and fn is not None


#-----------------------------------------------------------------------------------
class SbotCopyPathCommand(sublime_plugin.WindowCommand):
    ''' Get file or directory path to clipboard. Supports context and sidebar menus. '''

    def run(self, paths=None):
        dir, fn, path = _get_path_parts(self.window.active_view(), paths)
        # sc.slog(sc.CAT_DBG, f'SbotCopyPathCommand, {dir}, {fn}, {path}')
        sublime.set_clipboard(path)

    def is_visible(self, paths=None):
        # Ensure valid path.
        dir, fn, path = _get_path_parts(self.window.active_view(), paths)
        return dir is not None


#-----------------------------------------------------------------------------------
class SbotCopyFileCommand(sublime_plugin.WindowCommand):
    ''' Copy selected file to the same dir. Supports context and sidebar menus. '''

    def run(self, paths=None):
        dir, fn, path = _get_path_parts(self.window.active_view(), paths)

        # Find a valid file name.
        ok = False
        root, ext = os.path.splitext(path)
        for i in range(1, 9):
            newfn = f'{root}_{i}{ext}'
            if not os.path.isfile(newfn):
                shutil.copyfile(path, newfn)
                ok = True
                break

        if not ok:
            sublime.status_message("Couldn't copy file")

    def is_visible(self, paths=None):
        # Ensure file only.
        dir, fn, path = _get_path_parts(self.window.active_view(), paths)
        return fn is not None


#-----------------------------------------------------------------------------------
def _get_path_parts(view, paths):
    ''' To support commands that can be sited in Sidebar and Context menus.
        Returns (dir, fn, path).
        fn will be None for a directory.
        path is fully expanded path.
    '''

    dir = None
    fn = None
    path = None

    if paths is None:
        # Get the view file.
        path = view.file_name()
    elif len(paths) > 0:
        # Get the first element of paths - from sidebar.
        path = paths[0]

    if path is not None:
        exp_path = sc.expand_vars(path)
        if exp_path is None:
            raise RuntimeError(f'Bad path:{path}')

        if os.path.isdir(exp_path):
            dir = exp_path
        else:
            dir, fn = os.path.split(exp_path)
        path = exp_path

    return (dir, fn, path)
