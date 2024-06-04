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
`*`   | Default key bindings
**    | Displayed since alt key is set
***   | Rebound with: detach-on-destroy off

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
 ------ | ------ | ------
 `<p>` ( | M-( | Previous session **
 `<p>` ) | M-) | Next session **
 `<p>` _ | M-_ | Last session
 `<p>` + | M-+ | Create named session
 `<p>` S | | Rename session
 `<p>` M-x | | Kill session

### Window handling

Key | Alt key(-s) | Description
------ | ------ | ------
`<p>` 9   | M-9     | Previous window
`<p>` 0   | M-0     | Next window
`<p>` -   | M--     | Last window
`<p>` =   | M-=     | New window
`<p>` <   | M-<     | Swap window left
`<p>` >   | M->     | Swap window right
`<p>` *   |         | Toggle synchronized tabs
`<p>` W   |         | Rename window
`<p>` & * | `<p>` X | Kill window ***
<nbsp> |<nbsp> |<nbsp>
`<p>` M-H | `<p>` M-S-Left  | Split window left
`<p>` M-J | `<p>` M-S-Down  | Split window down
`<p>` M-K | `<p>` M-S-Up    | Split window up
`<p>` M-L | `<p>` M-S Right | Split window right

### Pane handling

Key | Alt key | Default | Description
-|-|-|-
`<p>` B   | | | Choose paste buffer(-s)
`<p>` M-l | | | Clear history & screen
`<p>` M-e | | | Save history to file (with escapes)
`<p>` M-h | | | Save history to file (no escapes)
`<p>` s   | | | Set pane size (w x h)
`<p>` P   | | | Set pane title
`<p>` x * | | | Kill pane ***
<nbsp> |<nbsp> |<nbsp> | <nbsp>
`<p>` h | M-Left  | `<p>` Left  | Select pane to the left
`<p>` j | M-Down  | `<p>` Down  | Select pane below
`<p>` k | M-Up    | `<p>` Up    | Select pane above
`<p>` l | M-Right | `<p>` Right | Select pane to the right
<nbsp> |<nbsp> |<nbsp> | <nbsp>
`<p>` H | C-M-Left  | `<p>` C-Left  | Resize the pane left by 1
`<p>` J | C-M-Down  | `<p>` C-Down  | Resize the pane down by 1
`<p>` K | C-M-Up    | `<p>` C-Up    | Resize the pane up by 1
`<p>` L | C-M-Right | `<p>` C-Right | Resize the pane right by 1
<nbsp> |<nbsp> |<nbsp> | <nbsp>
<nbsp> | `<p>` C-M-Left  | `<p>` M-Left  | Resize the pane left by 5
<nbsp> | `<p>` C-M-Down  | `<p>` M-Down  | Resize the pane down by 5
<nbsp> | `<p>` C-M-Up    | `<p>` M-Up    | Resize the pane up by 5
<nbsp> | `<p>` C-M-Right | `<p>` M-Right | Resize the pane right by 5
<nbsp> |<nbsp> |<nbsp> | <nbsp>
`<p>` C-h | M-S-Left  |         | Split pane to the left
`<p>` C-j | M-S-Down  | `<p>` % | Split pane below
`<p>` C-k | M-S-Up    |         | Split pane above
`<p>` C-l | M-S-Right | `<p>` " | Split pane to the right
