# Turris survey

It collects Turris OS usage information - OS version, list of installed packages
and package lists with their enabled options and sends it through Sentinel
infrastructure to Turris servers.

## Usage

```
turris_survey [options]
```

Options:
- `-s` / `--socket`: path of ZMQ socket to Sentinel Proxy,
  default is: `ipc:///tmp/sentinel_pull.sock`
- `-T` / `--topic`: topic under which data are sent by Sentinel Proxy to server,
  default is: `sentinel/collect/survey`


## Return value

It returns 0 if send to Sentinel-Proxy was successful otherwise 1 is returned.

