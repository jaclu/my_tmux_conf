# NavHints

(r) = repeats

## Basics keyboard without arrows

For actions not available without the M-key, use tmux-menus

### General environment

- Navigate ses/win/pan : Prefix N

### Pane

- pane navigate : Prefix hjkl (r)
- pane split : Prefix C-hjkl
- pane resize : Prefix HJKL (r)
- pane swap : Prefix {}
- pane kill : Prefix x

### Window

- window new : Prefix c / Prefix =
- window last : Prefix -
- window next-prev : Prefix 90 (r) / Prefix np (r)
- window swap : Prefix < >
- window kill : Prefix X

### Session

- session last: Prefix \_
- session next-prev : Prefix () (r)
- session new : Prefix +

## Meta (M-) available

### (M-) General environment

- Page Up : M-v
- List all plugins : Prefix M-P
- kill server : M X

### (M-) Pane

- entire screen (window) split : Prefix M-hjkl
- Clear screen and history: Prefix M-c
- save history with escapes : Prefix M-E
- save history no escapes : Prefix M-H

### (M-) Window

- window new : M =
- window last : M -
- window next-prev : M 9/0
- window swap : M < >

### (M-) Session

- session last : `M _`
- session new : M +
- kill session : M x

## M & Arrows available

### (Arrows) Pane

- pane navigate : Prefix Arrows (r) / (r) M-Arrows
- pane split : Prefix M-Arrows
- entire screen (window) split : Prefix C-M-Arrows
- pane resize : C-S-Arrows
- pane resize (by 5): M-S-Arrows

### (Arrows) Window

- window next-prev : C-M Left/Right

### (Arrows) Session

- session next-prev : M () | C-M Up/Down
