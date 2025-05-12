# MyTmuxConf

## Dependency

```bash
tmux 1.4
```

```bash
pip install tmux-conf
```

## Purpose of my setup style

I want to use the same tmux conf on all the systems I use.

Since they don't always run the same version of tmux, at first I need to
check if a given feature is available on that tmux, and either skip an
unavailable feature, or set something as close as possible up, given that
versions limitations.

Secondly I want to easily see what type of system I am working on via
the status bar color scheme.

Local machine, iSH on the iPad, local vhost, cloud host, test, acceptance,
production etc

Thirdly I want to in principle always use the same plugins, with
the limitation that some plugins only makes sense on a local system,
and some only work on certain Operating Systems. In some cases plugins
have fairly recent minimal version requirements, so that also needs to
be taken into account.

Finally since I often use new cloud hosts, I want all relevant plugins
to be auto installed first time tmux fires up on a given system.

Given all this, I decided to create a tmux.conf generator, that creates
an appropriate tmux conf for the given system. With all the needed extras to
do the overall tasks needed to keep things going smoothly.

Normally the processing just takes a split second, so starting tmux by
first generating the conf file does not create a noticeable delay when
tmux starts up.

This also adds the advantage of being able to use TERM settings to
identify the running terminal.
If you use iTerm2 this makes quite a difference, since it expects tmux
settings not ideal to other apps to perform well.
All you need to do after re-connecting with another terminal app is to
re-source the config.

This is implemented in Python, using class inheritance to easily override
things depending on environment.

Since I often work on new tmux-plugins, this gave me an easy way to test
compatibility, especially using asdf, where I can have all versions of tmux
available. This led in the end to my tmux conf being fully backwards
compatible all the way back to version 1.7 Not that I would realistically
end up using so old versions, more as a why not, and to see if it could be
handled by this environment without too much pain.

This is not meant as a tmux conf others should use directly as is.
The idea is to provide a tool set where you can use your own preferred config,
with tools that makes it easy to handle the situation if you happen to
run on more than one version of tmux.

See my setup more as an example, than something to be directly used.

As I am writing this, the most commonly available tmux versions
on different platforms are 3.3a 3.2a, and 3.1 and making your env able
to handle those versions should probably be more than enough.
Over time new versions will popup, so for new features new version checks
would need to be included.

Most likely initially you would only need to implement a content method,
where you just paste in your current tmux conf.

If you want to you can use the version controlled plugin handling, replacing it
with the plugins you use. Otherwise just drop your current plugin handling
into the content method along the rest of your current setup.

## Test/Devel env

if a session is started using `myt -2` or with the env variable `T2_ENV=1` set,
it is assumed to be a secondary session typically used for testing stuff.
This env is generated inside `~/t2` and tmux conf will be at `~/t2/tmux/tmux.conf`
This alternate session uses `C-b` as prefix.

This tmux instance will be able to run independent of the main tmux,
either inside or standalone. Ideal for testing out new configs,
and even run a different version of tmux for compatibility tests.

## host name based config

I normally start tmux with myt (in tools) it compiles a fresh tmux.conf
based on hostname.
I have supplied some samples in sample_hosts. Create a folder hostnames and define
hostname based configs there, using the lowercased version of `hostname -s`
for each host.

This way it is dead easy to adopt the setup depending on where it runs.
In most cases I just ~~soft-link~~ (weird no longer works, now I need
to copy the template to the hostname file if not in same dir) one of the
sb/ entries to the hostname, to give it a suitable
styling depending on host role.

Most of my actual hosts are filtered out for privacy reasons, I have left
a few in here, as examples.
