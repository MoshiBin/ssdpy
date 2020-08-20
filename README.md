# SSDPy: Python SSDP library [![Build Status](https://travis-ci.org/MoshiBin/ssdpy.svg?branch=master)](https://travis-ci.org/MoshiBin/ssdpy) [![PyPI](https://img.shields.io/pypi/v/ssdpy)](https://pypi.org/project/ssdpy/) [![PyPI - Wheel](https://img.shields.io/pypi/wheel/ssdpy)](https://pypi.org/project/ssdpy/) ![GitHub](https://img.shields.io/github/license/MoshiBin/ssdpy) [![codecov](https://codecov.io/gh/MoshiBin/ssdpy/branch/master/graph/badge.svg)](https://codecov.io/gh/MoshiBin/ssdpy) [![Read the Docs](https://img.shields.io/readthedocs/ssdpy)](https://ssdpy.readthedocs.io/en/latest/)

SSDPy is a lightweight implementation of [SSDP](https://en.wikipedia.org/wiki/Simple_Service_Discovery_Protocol) (Simple Service Discovery Protocol). It is designed for ease of use and high compatibility with the protocol in real-life use. It supports both the IETF and UPnP versions of the protocol. You can read the [full documentation here](https://ssdpy.readthedocs.io/en/latest/).

## Example usage

Send an SSDP discover packet (M-SEARCH):

```python
>>> from ssdpy import SSDPClient
>>> client = SSDPClient()
>>> devices = client.m_search("ssdp:all")
>>> for device in devices:
...     print(device.get("usn"))
uuid:Dell-Printer-1_0-dsi-secretariat::urn:schemas-upnp-org:service:PrintBasic:1
uuid:00000000-0000-0000-0200-00125A8A0960::urn:schemas-microsoft-com:nhed:presence:1
```

Send an SSDP NOTIFY packet, telling others about a service:

```python
>>> from ssdpy import SSDPServer
>>> server = SSDPServer("my-service-identifier")
>>> server.notify()
```

Start an SSDP server which responds to relevant M-SEARCHes:

```python
>>> from ssdpy import SSDPServer
>>> server = SSDPServer("my-service-identifier", device_type="my-device-type")
>>> server.serve_forever()
```

Then, from a client, M-SEARCH for our server:

```python
>>> from ssdpy import SSDPClient
>>> client = SSDPClient()
>>> devices = client.m_search("my-device-type")
>>> for device in devices:
...     print(device.get("usn"))
my-service-identifier
```

## CLI utilities

SSDPy comes with two CLI utilities:

- ssdpy-server is a server that listens for M-SEARCHes and responds if they match its name.
- ssdpy-discover sends an M-SEARCH query and collects all responses.

## Release checklist

- Update `ssdpy/version.py` with new version name.
- Update `CHANGES.md`.
- Commit the changes, tag with version & push.
- Run `make release`.

## Links

* IETF draft of the protocl (still in use by some devices, e.g. redfish) [https://tools.ietf.org/html/draft-cai-ssdp-v1-03](https://tools.ietf.org/html/draft-cai-ssdp-v1-03)
* UPnP Device Architecture 1.1 [https://web.archive.org/web/20150905102426/http://upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v1.1.pdf](https://web.archive.org/web/20150905102426/http://upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v1.1.pdf)
* UPnP Device Architecture 2.0 [https://web.archive.org/web/20151107123618/http://upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v2.0.pdf](https://web.archive.org/web/20151107123618/http://upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v2.0.pdf)
