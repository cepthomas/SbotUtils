# SbotUtils

Odds and ends in the Sbot family that don't have a better home for now. You can add them to your personal menus.

Built for ST4 on Windows and Linux.

- Display absolute text position in status bar.
- One click view splitter that works like VS, Word, etc.
- Execute current file (html, py, etc).
- Open terminal in current dir.
- Menu item to open a file as your cheatsheet, typically something from [ST docs](https://www.sublimetext.com/docs/)



## Commands
| Command                | Type     | Description                                        | Args                        |
| :--------              | :------- | :-------                                           | :-------                    |
| sbot_utils_cheatsheet  | Main     | Opens your cheatsheet file                         |                             |
| sbot_utils_split_view  | Context  | Toggle split view                                  |                             |
| sbot_utils_exec        | Context  | Run selected executable with output to new view    |                             |
| sbot_utils_run_script  | Context  | Run selected script with output to new view        |                             |
| sbot_utils_terminal    | Context  | Open a terminal here                               |                             |


## Settings
| Setting                    | Description                        | Options                                              |
| :--------                  | :-------                           | :------                                              |

# From old Sidebar:

# What It Is
Commands added to the sidebar defaults. Similar in concept to SideBarEnhancements
but it has too much extra stuff. This has just the basics and can be extended incrementally.

Built for ST4 on Windows and Linux (with a couple of exceptions).

## Commands
| Command                    | Type     | Description                                         | Args      |
| :--------                  | :------- | :-------                                            | :-------- |
| sbot_sidebar_copy_name     | Sidebar  | Copy file/dir name to clipboard                     |           |
| sbot_sidebar_copy_path     | Sidebar  | Copy full file/dir path to clipboard                |           |
| sbot_sidebar_copy_file     | Sidebar  | Copy selected file to a new file in the same folder |           |
| sbot_sidebar_exec          | Sidebar  | Run selected executable with output to new view     |           |
| sbot_sidebar_run_script    | Sidebar  | Run selected script with output to new view         |           |
| sbot_sidebar_terminal      | Sidebar  | Open a terminal here                                |           |
| sbot_sidebar_tree          | Sidebar  | Run tree cmd to new view (win only)                 |           |

## Settings
No internal but the right click stuff works better with this setting:
```
"preview_on_click": "only_left",
```
