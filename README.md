# SbotUtils

Odds and ends in the Sbot family that don't have a better home for now. You can add them to your personal 
Context and Sidebar menus.

Built for ST4 on Windows and Linux.

For the tree command, Linux needs something like: `sudo apt-get install tree`

- Display absolute text position in status bar next to row/col.
- One click view splitter that works like VS, Word, etc.
- Run a script file (py, lua, cmd, bat, sh) and show the output.
- Open file (html, py, etc) as if you double clicked it.
- Open terminal in current path.
- Open path under cursor if formatted like `[abc](my\best\file.txt)`


## Commands
| Command                         | Type                | Description                                            | Args      |
| :--------                       | :-------            | :-------                                               | :-------  |
| sbot_split_view                 | Context or Sidebar  | Toggle split view                                      |           |
| sbot_copy_name                  | Tab or Sidebar      | Copy file/dir name to clipboard                        |           |
| sbot_copy_path                  | Tab or Sidebar      | Copy full file/dir path to clipboard                   |           |
| sbot_copy_file                  | Tab or Sidebar      | Copy selected file to a new file in the same directory |           |
| sbot_run                        | Context or Sidebar  | Run selected script with output to new view            |           |
| sbot_open                       | Context or Sidebar  | Like you clicked it in explorer                        |           |
| sbot_terminal                   | Context or Sidebar  | Open a terminal here                                   |           |
| sbot_tree                       | Context or Sidebar  | Run tree cmd to new view (win only)                    |           |
| sbot_open_context_path          | Context             | Open path under cursor                                 |           |
| sbot_insert_target_from_clip    | Context             | Insert path target from clipboard                      |           |

Context menu items like:
`{ "caption": "Copy Name", "command": "sbot_copy_name"},`

Sidebar menu items like:
`{ "caption": "Copy Name", "command": "sbot_copy_name", "args": {"paths": []} },`


## Settings
No internal but the right click stuff works better with this setting:
```
"preview_on_click": "only_left",
```
