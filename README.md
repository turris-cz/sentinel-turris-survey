# Turris survey

This is collector of Turris routers (Turris OS) usage. We want to collect
information that helps developers to do informative decisions. That is at minimum
list of installed software and also some other network information.

This is using Turris Sentinel infrastructure to send/collect information from
routers.


## Usage

```
turris_survey [options]
```

Options:
- `-s` / `--socket`: path of ZMQ socket to Sentinel Proxy,
  default is: `ipc:///tmp/sentinel_pull.sock`
- `-T` / `--topic`: topic under which data are sent by Sentinel Proxy to server,
  default is: `sentinel/collect/survey`


## Testing

To see outgoing data, run `dev_proxy` from
[Sentinel:Proxy repository](https://gitlab.nic.cz/turris/sentinel/proxy)
and `turris_survey` on the same socket e.g. `ipc:///tmp/turris-survey-testing.sock`.
