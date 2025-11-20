# Report-Back (`reback`)

A simple agent/server that allows individual agents to report back to a server component with basic metrics and information.

## Motivation

I've been in several spaces where keeping track of ad-hoc machines has been necessary. They change IPs, or people set static IPs without consulting, causing various issues.

Installing and setting up a full monitoring solution has not always been possibile. Sometimes the monitoring server itself has needed to be on a potentially transient IP.

This project aims to provide a lightweight solution to this type of issue.

# Design

## Server

Reback server listens for agents reporting back, simply.

It listens on a specified port, and periodically sends a broadcast ping to allow clients to auto-discover the server in case it moves.

```sh
reback server [-p PORT] [-P periodicity] [-B broadcast_ip] [-l logfile] [-T tags]
```

It records a report from an agent in a local filesystem with files named after the agent's identifier, with a timestamp

If tags (`-T tags`) is specified, the server will only record agents advertising with any of the given tags.

## Agent

The reback agent periodically pings the target server it is configured to talk to (`-t target`). It sends its hostname, uptime, free memory and load averages as standard. The server determines its IP and MAC from the network packet.

If a script file is specified (`-s scriptfile`), that script is executed, and the output is attached as gzip+base64 payload.

If "discovery" mode is enabled (`-D`), it will listen for server ping broadcasts, and also report to such self-announced servers. If the self-broadcasting server is not heard from again wthin a period of time (`-F forget_time`), the agent will stop reporting to it.

The agent can also specify tags with its ping, which servers can optionally use to filter on.

```sh
reback agent [-t main_target] [-D] [-s scriptfile] [-F forget_time] [-T tags]
```

