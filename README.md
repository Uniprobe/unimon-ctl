# Unimon Control 🎛

Unimon Control is port of [ClickOS Control](https://github.com/sysml/clickos-ctl) into Python. This hopes to make life easier for future edits given the amount of string handling required from this program...

This currently supports all the same features as the original ClickOS Control so can be used as a direct replacement. This program does **not** depend on `libxenstore`, but does depend on `pyxs` for xenstore usage and `flask` for the API.

See the README for ClickOS Control [here](https://github.com/sysml/clickos-ctl/blob/master/README.md).

## Installation

Install using pip (for python 3):
```bash
pip install --user unimon-ctl
sudo unimon-ctl -h
```
(script should be added to `~/.local/bin` by default)

Or use with Docker:

```bash
docker run --rm -it -v /var/run/xenstored/socket:/var/run/xenstored/socket willfantom/unimon-ctl -h
```

## Re-Implemented ClickOS-Ctl Features

- Use xenstore to communicate with clickos instance ✅
- Install/Remove click configs to clickos domains ✅
  - via `install`/`remove` sub commands
- Start/Stop clickos routers ✅
  - via `start`/`stop` sub commands

## Added ClickOS-Ctl Features

- Prints some emoji ✅
- Get list of clickos domain's routers and states ✅
  - via `list` sub command
- Check state of specific router ✅
  - via `state` sub command
- Read element handler value
  - via `get` sub command
- Can run in API mode (more [here](#api-mode)) ✅
  - via `api` sub command

## Unimon Features

Accessible under the `unimon` subcommand

- Get list of router's unimon elements
  - via `list` sub command
- Get state of a unimon element
  - via `state` sub command
- Update poll rate of unimon element
  - via `update-poll` sub command
- Update the target element of a unimon element
  - via `update-target` sub command
- Update the target element handler of a unimon element
  - via `update-handler` sub command
- Get data from a unimon element since a given unix time
  - via `get` sub command
- Toggle activation state of a unimon element
  - via `toggle-state` sub command

## Building
- Pythony (can be installed via `pip`) 🐍
- Dockery (can run in a `docker` container) 🐳

### API Mode

API mode makes all the functions accessible over a REST API. Data is returned in json along with errors. Errors that return a non 200 status code are actually encountered errors. For example, if a router state is returned as `Unknown`, this will still have status code 200. In this example, if there was any issue in communication with the router, a non 200 code would be returned. Errors are also printed to the log. If running in API mode inside a container, ensure the port you specify is mapped.

- `--port <int>` sets the API's port (default: `8080` - listen address `0.0.0.0`)

```bash
sudo unimon-ctl api --port 6767
[or]
docker run --rm -i -p 8080:6767 -v /var/run/xenstored/socket:/var/run/xenstored/socket willfantom/unimon-ctl api --port 6767
```

## Notice

This has been made as part of my PhD work, so will not be maintained beyond the feature set I require.