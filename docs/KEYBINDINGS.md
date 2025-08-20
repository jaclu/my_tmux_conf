# KeyBindings

## Bindings pilosophy

I have tried hard to make all essential commands available without
depending on the M-key, since on some terminal apps it is not available.
In order to not have to struggle in such scenarios, I have landed
on a non M-dependant config. But truth be told I mostly use the
M based short-cuts in everyday usage whenever available.

I have only listed my own additional bindings. Defaults remain

Where the M-key is unavailable I use the plugin tmux-menus for M-key
dependent actions.

## Key bindings

| Note  | Description                           |
| ----- | ------------------------------------- |
| `<p>` | Prefix key                            |
| \*    | when use_prefix_arrow_nav_keys is set |
| \*\*  | Rebound with: detach-on-destroy off   |

### Pane handling

| Key                 | No Prefix   | Default       | Description                         |
| ------------------- | ----------- | ------------- | ----------------------------------- |
|                     |             | `<p> ;`       | Previously active pane              |
| `<p> h`\*           | `M-Left`    | `<p> Left`    | Select pane to the left             |
| `<p> j`\*           | `M-Down`    | `<p> Down`    | Select pane below                   |
| `<p> k`\*           | `M-Up`      | `<p> Up`      | Select pane above                   |
| `<p> l`\*           | `M-Right`   | `<p> Right`   | Select pane to the right            |
|                     |             | `<p> {`       | Swap pane backwards                 |
|                     |             | `<p> }`       | Swap pane forwards                  |
|                     |             |               |                                     |
| `<p> P`             |             |               | Set pane title                      |
|                     |             | `<p> x`       | Kill pane \*\*                      |
| `<p> B`             |             |               | Choose paste buffer(-s)             |
| `<p> M-l`           |             |               | Clear history & screen              |
| `<p> M-E`           |             |               | Save history to file (with escapes) |
| `<p> M-H`           |             |               | Save history to file (no escapes)   |
| `<p> s`             |             |               | Set pane size (w x h)               |
|                     |             |               |                                     |
| `<p> C-h` `M-Left`  |             |               | Split pane to the left              |
| `<p> C-j` `M-Down`  |             | `<p> %`       | Split pane below                    |
| `<p> C-k` `M-Up`    |             |               | Split pane above                    |
| `<p> C-l` `M-Right` |             | `<p> "`       | Split pane to the right             |
|                     |             |               |                                     |
| `<p> H`             | `C-S-Left`  | `<p> C-Left`  | Resize the pane left by 1           |
| `<p> J`             | `C-S-Down`  | `<p> C-Down`  | Resize the pane down by 1           |
| `<p> K`             | `C-S-Up`    | `<p> C-Up`    | Resize the pane up by 1             |
| `<p> L`             | `C-S-Right` | `<p> C-Right` | Resize the pane right by 1          |
|                     |             |               |                                     |
|                     | `M-S-Left`  |               | Resize the pane left by 5           |
|                     | `M-S-Down`  |               | Resize the pane down by 5           |
|                     | `M-S-Up`    |               | Resize the pane up by 5             |
|                     | `M-S-Right` |               | Resize the pane right by 5          |

### Window handling

| Key                         | No Prefix           | Default | Description               |
| --------------------------- | ------------------- | ------- | ------------------------- |
| `<p> -`                     | `M--`               |         | Previously current window |
| `<p> 9`                     | `M-0` (`C-M-Left`)  | `<p>` p | Previow window            |
| `<p> 0`                     | `M-9` (`C-M-Right`) | `<p>` n | Next window               |
| `<p> =`                     | `M-=`               | `<p>` c | New window                |
| `<p> <`                     | `M-<`               |         | Swap window left          |
| `<p> >`                     | `M->`               |         | Swap window right         |
|                             |                     |         |                           |
| `<p> W`                     |                     | `<p> ,` | Rename window             |
| `<p> X`                     |                     | `<p> &` | Kill window \*\*          |
| `<p> *`                     |                     |         | Toggle synchronized tabs  |
| `<p> e`                     |                     | `<p> E` | Spread panes out evenly.  |
|                             |                     |         |                           |
| `<p> M-H`                   |                     |         | Split window left         |
| `<p> M-J`                   |                     |         | Split window down         |
| `<p> M-K`                   |                     |         | Split window up           |
| `<p> M-L`                   |                     |         | Split window right        |

### Session handling (sometimes referred to as clients by tmux man)

| Key       | No Prefix        | Default | Description                |
| --------- | ---------------- | ------- | -------------------------- |
| `<p> _`   | `M-_`            |         | Previously current session |
|           | `C-M-Down`       | `<p> )` | Next session in order      |
|           | `C-M-Up`         | `<p> (` | Previous session in order  |
|           |                  |         |                            |
| `<p> S`   |                  | `<p> $` | Rename session             |
| `<p> M-x` |                  |         | Kill session               |
| `<p> +`   | `M-+`            |         | Create named session       |

### General environment

| Key       | Default | Description              |
| --------- | ------- | ------------------------ |
|           | `C-v`   | Page Down                |
|           | `M-v`   | Page Up                  |
|           |         |                          |
| `<p> i`   |         | Popup ipython            |
| `<p> y`   |         | Popup lazygit            |
| `<p> N`   |         | Navigate ses/win/pane    |
| `<p> O`   |         | Scratchpad popup session |
| `<p> M-P` |         | List all plugins defined |
| `<p> R`   |         | Re-source config         |
| `<p> M-X` |         | Kill Server              |

### Mouse handling

| Key                | Description                       |
| ------------------ | --------------------------------- |
| `<p> M`            | Toggle tmux mouse handling on/off |
| `DoubleClick3Pane` | Toggle zoom for clicked pane      |

### Status bar

| Key     | Description                  |
| ------- | ---------------------------- |
| `<p>` T | Toggle display of status bar |
