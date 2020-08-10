### Latest changes (not in a release)

- Fixed an issue where NOTIFY messages were not conforming to UPnP (thanks @hotab)

### 0.3.0
(2020-08-10)

- Dropped support for Python 3.4
- Fixed a compatibility issue in protocol.py (thanks @ZacJW)

### 0.2.3
(2019-11-28)

- Added `--json` flag to ssdpy-discover.
- `SSDPServer.serve_forever()` will skip packets it cannot send instead of crashing.

### 0.2.2
(2019-11-14)

- Fixed a dependency issue with mock on Python 2.7.

### 0.2.1
(2019-11-13)

- Added `--address` to ssdpy-server.
- Binding to an interface now explicitly subscribes the interface to the multicast group.
- Removed `constants.IPv4` and `constants.IPv6` in favor of raw strings: `("ipv4", "ipv6")`.
- Added code coverage reports.
- Added tests for ssdpy-server.
- Increase testing breadth to include more python versions (2.7, >=3.4).

### 0.2.0
(2019-11-07)

- Added ssdpy-server CLI command.
- Added ssdpy-discover CLI command.
- Internal: Added helper scripts to manage releases.
- Internal: Added python package metadata.

### 0.1.2
(2019-11-03)

- Quoted the `MAN` field in `M-SEARCH` to be compatible with current implementations of SSDP.

### 0.1.1
(2019-11-02)

- Added `dev-requirements.txt`.

### 0.1.0
(2019-11-02)

- Initial release.
