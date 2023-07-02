# SbotUtils

Odds and ends in the Sbot family that don't have a better home for now. You can add them to your personal 
Context and Sidebar menus.

Built for ST4 on Windows and Linux.

- Display absolute text position in status bar next to row/col.
- One click view splitter that works like VS, Word, etc.
- Execute current file (html, py, etc) as if you double clicked it.
- Open terminal in current path.


## Commands
| Command                | Type                | Description                                         | Args      |
| :--------              | :-------            | :-------                                            | :-------  |
| sbot_split_view        | Context or Sidebar  | Toggle split view                                   |           |
| sbot_copy_name         | Context or Sidebar  | Copy file/dir name to clipboard                     |           |
| sbot_copy_path         | Context or Sidebar  | Copy full file/dir path to clipboard                |           |
| sbot_copy_file         | Context or Sidebar  | Copy selected file to a new file in the same folder |           |
| sbot_exec              | Context or Sidebar  | Run selected executable with output to new view     |           |
| sbot_terminal          | Context or Sidebar  | Open a terminal here                                |           |
| sbot_tree              | Context or Sidebar  | Run tree cmd to new view (win only)                 |           |

Context menu items like:
`{ "caption": "Copy Name", "command": "sbot_copy_name"},`

Sidebar menu items like:
`{ "caption": "Copy Name", "command": "sbot_copy_name", "args": {"paths": []} },`


## Settings
No internal but the right click stuff works better with this setting:
```
"preview_on_click": "only_left",
```
