# KeyBindings

## Bindings pilosophy

I have tried hard to make all essential commands available without
depending on the M-key, since on some terminal apps it is not available.
In order to not have to struggle in such scenarios, I have landed
on a non M-dependant config. But truth be told I mostly use the
M based short-cuts in everyday usage whenever available.

I have only listed my own bindings.

Where the M-key is unavailable I use the plugin tmux-menus for M-key
dependent acctions.

## Key bindings

Note | Description
-|-
`<p>` | Prefix key
**  | Displayed since alt key is set
*** | Rebound with: detach-on-destroy off

### General environment

Key | Description
-|-
`<p>` e   | Edit config
`<p>` R   | Re-source config
`<p>` M-P | List all plugins defined
`<p>` N   | Navigate ses/win/pane
`<p>` O   | Scratchpad popup session
`<p>` M-X | Kill Server

### Mouse handling

Key | Description
-|-
`<p>` M | Toggle tmux mouse handling on/off
DoubleClick3Pane | Toggle zoom for clicked pane

### Status bar

Key | Description
-|-
`<p>` t | Toggle display of status bar

### Session handling

Key | Alt key(-s) | Description
-|-|-
`<p>` ( | M-( | Previous session **
`<p>` ) | M-) | Next session **
`<p>` _ | M-_ | Last session
`<p>` + | M-+ | Create named session
`<p>` S | | Rename session
`<p>` M-x | | Kill session

### Window handling

Key | Alt key(-s) | Description
-|-|-
`<p>` 9 | M-9 | Previous window
`<p>` 0 | M-0 | Next window
`<p>` - | M-- | Last window
`<p>` = | M-=| New window
`<p>` < | M-< | Swap window left
`<p>` > | M-> | Swap window right
`<p>` M-H | C-M-S-Left | Split window left
`<p>` M-J | C-M-S-Down | Split window down
`<p>` M-K | C-M-S-Up | Split window up
`<p>` M-L | C-M-S Right | Split window right
`<p>` * | | Toggle synchronized tabs
`<p>` W | | Rename window
`<p>` & | `<p>` X | Kill window ***

### Pane handling

Key | Alt key | Description
-|-|-
`<p>` B | | Choose paste buffer(-s)
`<p>` M-l | | Clear history & screen
`<p>` M-e | | Save history to file (with escapes)
`<p>` M-h | | Save history to file (no escapes)
`<p>` h | M-Left | Select pane to the left
`<p>` j | M-Down | Select pane below
`<p>` k | M-Up | Select pane above
`<p>` l | M-Right | Select pane to the right
`<p>` C-h | M-S-Left | Split pane to the left
`<p>` C-j | M-S-Down | Split pane below
`<p>` C-k | M-S-Up | Split pane above
`<p>` C-l | M-S-Right | Split pane to the right
`<p>` H | C-M-Left | Resize the pane left
`<p>` J | C-M-Down | Resize the pane down
`<p>` K | C-M-Up | Resize the pane up
`<p>` L | C-M-Right | Resize the pane right
`<p>` s | | Set pane size (w x h)
`<p>` P | | Set pane title
`<p>` x | | Kill pane ***
