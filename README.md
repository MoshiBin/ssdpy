# SSDPy: Python SSDP library [![Build Status](https://travis-ci.org/MoshiBin/ssdpy.svg?branch=master)](https://travis-ci.org/MoshiBin/ssdpy)

SSDPy is a pythonic implementation of SSDP supporting both the IETF and UPnP versions of the protool.

## Example usage

```python
>>> from ssdpy import discover
>>> devices = discover()
>>> for device in devices:
...     print(device.get("usn"))
uuid:Dell-Printer-1_0-dsi-secretariat::urn:schemas-upnp-org:service:PrintBasic:1
uuid:00000000-0000-0000-0200-00125A8A0960::urn:schemas-microsoft-com:nhed:presence:1
```

## Features

- [x] Service discovery
- [ ] Notify
- [ ] Server listening to SSDP multicasts
