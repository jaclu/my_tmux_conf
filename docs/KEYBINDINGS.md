# KeyBindings

## Bindings pilosophy

I have tried hard to make all essential commands available without
depending on the M-key, since on some terminal apps it is not available.
In order to not have to struggle in such scenarios, I have landed
on a non M-dependant config. But truth be told I mostly use the
M based short-cuts in everyday usage whenever available.

I have only listed my own bindings.

Where the M-key is unavailable I use the plugin tmux-menus for M-key
dependent actions.

## Key bindings

Note | Description
-|-
`<p>` | Prefix key
**    | Displayed since alt key is set
***   | Rebound with: detach-on-destroy off

### General environment

Key | Description
-|-
`<p>` R   | Re-source config
`<p>` `M-P` | List all plugins defined
`<p>` N   | Navigate ses/win/pane
`<p>` O   | Scratchpad popup session
`<p>` M-X | Kill Server

### Mouse handling

Key | Description
-|-
`<p>` M | Toggle tmux mouse handling on/off
`DoubleClick3Pane` | Toggle zoom for clicked pane

### Status bar

Key | Description
------ | ------
`<p>` t | Toggle display of status bar

### Session handling (sometimes referred to as clients by tmux man)

 Key | Meta key | Default | Description
 ------ | ------ | ------ | ------
 <nbsp> | `M-)` `C-M-S-Down` | `<p>` ) | Next session in order
 <nbsp> | `M-(` `C-M-S-Up`   | `<p>` ( | Previous session in order
 `<p>` _ | `M-_`         | <nbsp>  | Previously current session
 `<p>` +  | `M-+`         | <nbsp>  | Create named session
 `<p>` S  | <nbsp>        | `<p>` $ | Rename session
 <nbsp> | `<p> M-x`       | <nbsp>  | Kill session

### Window handling

Key | Meta key | Default | Description
------ | ------ | ------ | ------
`<p>` 0  | `M-9` `C-M-S-Right` | `<p>` n | Next window
`<p>` -  | `M-0` `C-M-S-Left`  | `<p>` p | Previow window
`<p>` 9  | `M--`   | `<p>` l | Previously current window
`<p>` =  | `M-=`   | `<p>` c | New window
`<p>` <  | `M-<`   | <nbsp>  | Swap window left
`<p>` >  | `M->`   | <nbsp>  | Swap window right
`<p>` *  |         | <nbsp>  | Toggle synchronized tabs
`<p>` W  |         | `<p>` , | Rename window
<nbsp> | `<p>` X | `<p>` & | Kill window ***
<nbsp> |<nbsp> |<nbsp> | <nbsp>
`<p>` `M-H` | `<p>` `M-S-Left`  | <nbsp> | Split window left
`<p>` `M-J` | `<p>` `M-S-Down`  | <nbsp> | Split window down
`<p>` `M-K` | `<p>` `M-S-Up`    | <nbsp> | Split window up
`<p>` `M-L` | `<p>` `M-S-Right` | <nbsp> | Split window right

### Pane handling

Key | Meta key | Default | Description
-|-|-|-
`<p>` B   | | | Choose paste buffer(-s)
<nbsp> | `M-l` | | Clear history & screen
`<p>` `M-e` | | | Save history to file (with escapes)
`<p>` `M-h` | | | Save history to file (no escapes)
`<p>` s   | | | Set pane size (w x h)
`<p>` P   | | | Set pane title
<nbsp> | | `<p>` x | Kill pane ***
<nbsp> |<nbsp> |<nbsp> | <nbsp>
`<p>` h | `M-Left`  | `<p>` Left  | Select pane to the left
`<p>` j | `M-Down`  | `<p>` Down  | Select pane below
`<p>` k | `M-Up`    | `<p>` Up    | Select pane above
`<p>` l | `M-Right` | `<p>` Right | Select pane to the right
<nbsp> |<nbsp> |<nbsp> | <nbsp>
`<p>` H | `C-S-Left`  | `<p>` `C-Left`  | Resize the pane left by 1
`<p>` J | `C-S-Down`  | `<p>` `C-Down`  | Resize the pane down by 1
`<p>` K | `C-S-Up`    | `<p>` `C-Up`    | Resize the pane up by 1
`<p>` L | `C-S-Right` | `<p>` `C-Right` | Resize the pane right by 1
<nbsp> |<nbsp> |<nbsp> | <nbsp>
<nbsp> | `M-S-Left`  | `<p>` `M-Left`  | Resize the pane left by 5
<nbsp> | `M-S-Down`  | `<p>` `M-Down`  | Resize the pane down by 5
<nbsp> | `M-S-Up`    | `<p>` `M-Up`    | Resize the pane up by 5
<nbsp> | `M-S-Right` | `<p>` `M-Right` | Resize the pane right by 5
<nbsp> |<nbsp> |<nbsp> | <nbsp>
`<p>` C-h | `C-M-Left`  |         | Split pane to the left
`<p>` C-j | `C-M-Down`  | `<p>` % | Split pane below
`<p>` C-k | `C-M-Up`    |         | Split pane above
`<p>` C-l | `C-M-Right` | `<p>` " | Split pane to the right
