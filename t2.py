#!/usr/bin/env python3
#
#  Copyright (c) 2022: Jacob.Lundqvist@gmail.com
#  License: MIT
#
#  Part of https://github.com/jaclu/my_tmux_conf
#
#  This sets up the t2 environment, meant to run an "inner" tmux, with
#  its own prefix (will be displayed on the status bar)
#
#  This keeps it's own plugin dirs and environment.
#  It is quite convenient to be able to test tmux settings or plugins
#  inside another tmux session without risking to wreck your entire tmux
#  foring you to fix it and then close everythinh down and restart tmux
#  hoping your primary or outer env comes back.
#
#  Also convenient for simply running this on another host than where
#  your primary tmux is running, without having colliding prefix issues
#

# everything, a lot of this is setup
#  in the default file, this is for color theme and selection of often
#  changing list of plugins I am testing
#  out.
import os
import mtc_utils

if mtc_utils.HOSTNAME == "ish-hetz1":
    from sb.sb_acceptance import SB
else:
    # normal theme
    from sb.sb_t2 import SB


class T2(SB):
    """Inner tmux session"""

    t2_env = "1"

    # plugin_handler = "manual"
    # plugin_handler: str = "tmux-plugins/tpm"
    # bind_meta = False
    # use_embedded_scripts = False
    # is_limited_host = True
    status_interval = 5

    #
    #  Override default plugins with empty stubs for plugins
    #  not wanted in T2_ENV
    #  not_ prefix is when I temp allow them, but keeping the opt out
    #  in case I want them gone again
    #

    #
    #  wont work in an inner tmux, outer is capturing key
    #  in both states. If this is really needed in the inner tmux
    #  a separate capture key for t2 could be defined
    #

    # def plugin_which_key(self) -> list:
    #     return ['alexwforsythe/tmux-which-key', 3.0, ""]

    def plugin_menus(self) -> list:  # 1.8
        conf = """
        set -g @menus_log_file ~/tmp/tmux-menus-t2.log
        # set -g @menus_use_cache no
        """
        #
        #  This plugin works in tmux 1.7, but that version do not support
        #  @variables, so we say 1.8 here...
        #
        return ["jaclu/tmux-menus", 1.8, conf]

    def not_plugin_packet_loss(self):  # 1.9
        min_vers = 1.9
        # if mtc_utils.IS_ISH or mtc_utils.HOSTNAME == "ish-hetz1" or self.is_tmate():
        # if mtc_utils.IS_ISH or self.is_tmate():
        if self.is_tmate():
            #  this will draw lots of CPU on hetz1, so disable it
            min_vers = 99.1  # disable for tmate
        return [
            "jaclu/tmux-packet-loss",
            min_vers,
            """
            set -g @packet-loss-ping_host 1.1.1.1

            set -g @packet-loss-ping_count   6
            set -g @packet-loss-history_size 6
            set -g @packet-loss-level_alert 18 # 4-26 6-18 7-15

            set -g @packet-loss-display_trend    no
            set -g @packet-loss-hist_avg_display yes
            set -g @packet-loss-run_disconnected no

            set -g @packet-loss-level_disp   5

            set -g @packet-loss-color_alert colour21

            set -g @packet-loss-level_crit 50

            set -g @packet-loss-color_bg    colour226

            set -g @packet-loss-log_file  $HOME/tmp/tmux-packet-loss-t2.log

            """,
        ]

    def plugin_resurrect(self) -> list:  # 1.9
        #
        #  Saves & Restores server sessions
        #
        #  save: <prefix> C-s restore: <prefix> C-r
        #
        #  Does not work on: iSH
        #
        #  This plugins fails to restore sessions in iSH, at least on my
        #  devices. so no point enabling tmux-resurrect & tmux-continuum
        #  on iSH
        #
        if self.is_tmate():
            return ["tmux-plugins/tmux-resurrect", 99, ""]

        plugins_dir = self.plugins.get_plugin_dir()
        # go up one and put it beside plugins_dir
        resurect_dir = f"{os.path.dirname(plugins_dir)}/resurrect"

        procs = "zsh bash ash ssh sudo top htop watch psql mysql sqlite sqlite3 "
        procs += "glow bat batcat"

        conf = f"""
        #
        #  Default keys:  save: <prefix> C-s restore: <prefix> C-r
        #
        #  All the process names needs to be added on one long line...
        #  Only long running processes needs to be listed, ie those that
        #  might be running in a pane when the session was saved.
        #
        #  If it is a command triggered by a full path you can refer to it
        #  with a ~ prefix, this will match all commands ending with this
        #  name, regardless of where from it was started.
        #
        set -g @resurrect-processes "{procs}"
        #  Env dependent settings for tmux-plugins/tmux-resurrect
        set -g @resurrect-dir "{resurect_dir}"
        """
        #  Line continuation without passing col 80 here
        # conf += "mysql glow sqlite sqlite3 top htop  ~packet_loss "
        # conf += "~common_pull ~sysload_tracker ~Mbrew ~Mapt'\n"

        return ["jaclu/tmux-resurrect", 1.9, conf]

    def plugin_zz_continuum(self) -> list:  # 1.9
        #
        #  Auto restoring a session just as tmux starts on a limited
        #  host will just lead to painfull lag.
        #
        #  It is also not desired on inner tmux sessions. They are
        #  typically for testing purposes, being able to manually restore
        #  a session makes sense, but auto-resuming does not.
        #
        if self.is_tmate():
            vers_min = 99.0  # make sure this is never used
        else:
            vers_min = 1.9
        #
        #  Automatically save and restore tmux server's open sessions.
        #
        #   Saves every 15 mins (default) Restores last save when tmux is
        #   starting
        #
        #  Depends on tmux-resurrect for actual save/restore.
        #
        #  In the below switch-statement I set the variables even if the
        #  values are defaults, since when re-running the config after
        #  changing this,
        #  If a variable is unset in the new state, the already set value
        #  will still be in effect. - Boy did that bite me...
        #
        #  2020-12-24
        #  ==========
        #  Due to a bug tmux-continuum should be as close to last plugin
        #  as possible to minimize the risk of a crucial tmux variable
        # `status-right` is not overwritten (usually by theme plugins).
        #
        conf = """
        set -g @continuum-save-interval  15
        set -g @continuum-restore        on
        """
        return ["jaclu/tmux-continuum", vers_min, conf]


if __name__ == "__main__":
    T2().run()
