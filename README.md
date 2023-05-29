# SbotUtils

Odds and ends in the Sbot family that don't have a better home for now. You can add them to your personal menus.

Built for ST4 on Windows and Linux.

- Display absolute text position in status bar.
- One click view splitter that works like VS, Word, etc.
- Execute current file (html, py, etc).
- Open terminal in current dir.
- Menu item to open a file as your cheatsheet, typically something from [ST docs](https://www.sublimetext.com/docs/)


Requires SbotCommon plugin.

## Commands
| Command                | Implementation | Description                                        | Args                        |
| :--------              | :-------       | :-------                                           | :-------                    |
| sbot_cheatsheet        | Main           | Opens your cheatsheet file                         |                             |
| sbot_split_view        | Context        | Toggle split view                                  |                             |
| sbot_exec              | Context        | Run selected executable with output to new view    |                             |
| sbot_run_script        | Context        | Run selected script with output to new view        |                             |
| sbot_terminal          | Context        | Open a terminal here                               |                             |


## Settings
| Setting                    | Description                        | Options                                              |
| :--------                  | :-------                           | :------                                              |
| cheatsheet_path            | Path to a file to open on select   |                                                      |

