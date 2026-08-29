from typing import TypedDict


class NodeOptions(TypedDict, total=False):
    hostname: str | None
    ip_addresses: list[str] | None
    port: int | None
    max_roots: int
    default_scan_interval_minutes: int

class NodeUpdateOptions(TypedDict, total=False):
    name: str
    os_type: str
    os_version: str
    hostname: str
    ip_addresses: list[str]
    port: int
    max_roots: int
    default_scan_interval_minutes: int