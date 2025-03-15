# NavHints

(r) = repeats

## Basics keyb no arrows

For actions not available without the M-key, use tmux-menus

### Pane

- pane navigate : Prefix hjkl (r) / Prefix Arrows (r)
- pane split :    Prefix C-hjkl
- pane resize :   Prefix HJKL (r)
- pane swap :     Prefix {}
- pane kill :     Prefix x
- save history with escapes : Prefix M-e
- save history no escapes :   Prefix M-h

### Window

- window last : Prefix -
- window next-prew : Prefix 90 (r) / Prefix np (r)
- window new :    Prefix c / =
- window split : Prefix C-M-hjkl
- window swap :   Prefix < >
- window kill :   Prefix X

### Session

- session last:  Prefix _
- session next-prev : Prefix () (r)
- session new :   Prefix +

### General environment

- Navigate ses/win/pan : Prefix N
- session pOpup :        Prefix O
- List all plugins :     Prefix M-P
- Kill server :          Prefix M-X
- session wizard :       Prefix T

## Adv keys for nav, can be disabled to force basic keys to be remembered

- pane navigate : M-Arrows
- pane split :    Prefix M-Arrows
- pane resize :   C-S-Arrows (by 1) / M-S-Arrows (by 5)

- next-prew win : M 9/0 | C-M Left/Right
- last window :   M -
- entire window split : Prefix C-M-HJKL Prefix C-M-Arrows
- swap window :   M < >
- new window :    M =

- next-prev ses : M () | C-M Up/Down
- last session : `M _`
- new session :   M +

- kill session :  M x
- kill server :   M X
