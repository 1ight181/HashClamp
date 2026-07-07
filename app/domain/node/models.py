from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional, TypedDict, Unpack
import re
import ipaddress
from uuid import UUID, uuid4

# RFC 1123
HOSTNAME_REGEX = re.compile(
    r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
)


@dataclass
class Node:
    name: str

    os_type: str
    os_version: str

    user_id: UUID

    id: UUID = field(init=False, default_factory=uuid4())

    hostname: Optional[str] = None
    ip_addresses: Optional[list[str]] = None
    port: Optional[int] = None

    max_roots: int = 50
    default_scan_interval_minutes: int = 30

    created_at: datetime = field(init=False, default_factory=datetime.now(timezone.utc))
    updated_at: datetime = field(init=False, default_factory=datetime.now(timezone.utc))

    class NodeCreateOptions(TypedDict, total=False):
        hostname: str
        ip_addresses: list[str]
        port: int
        max_roots: int
        default_scan_interval_minutes: int

    @classmethod
    def create(cls, name: str, os_type: str, os_version: str, user_id: UUID, **kwargs: Unpack[NodeCreateOptions]):
        """
        Creates a new node.

        Args:
            name: Human-readable node name.
            os_type: Operating system name.
            os_version: Operating system version.
            user_id: Owner user identifier.
            **kwargs:
                hostname: Optional node hostname.
                ip_addresses: Optional list of IPv4/IPv6 addresses.
                port: Optional node listening port.
                max_roots: Maximum number of roots allowed for the node.
                default_scan_interval_minutes: Default scan interval in minutes.

        Returns:
            A new Node instance.

        Raises:
            TypeError: If an argument has an invalid type.
            ValueError: If an argument has an invalid value.
        """
        if len(name.strip()) < 3:
            raise ValueError("Name is required and must be at least 3 character long")

        if not os_type.strip():
            raise ValueError("OS type is required and cannot be empty")

        if not os_version.strip():
            raise ValueError("OS version is required and cannot be empty")

        if not user_id:
            raise ValueError("User id is required and cannot be empty")

        hostname = kwargs.get("hostname")
        if hostname is not None:
            if not HOSTNAME_REGEX.match(str(hostname)):
                raise ValueError("Hostname is invalid")

        ip_addresses = kwargs.get("ip_addresses")
        if ip_addresses is not None:
            if not isinstance(ip_addresses, list):
                raise TypeError("Ip addresses must be a list")
            for ip in ip_addresses:
                try:
                    ipaddress.ip_address(ip)
                except ValueError:
                    raise ValueError(f"Invalid IP address: {ip}")

        port = kwargs.get("port")
        if port is not None:
            if isinstance(port, int):
                if port < 1 or port > 65535:
                    raise ValueError(f"Port {port} must be between 1 and 65535")
            else:
                raise TypeError("Port must be integer between 1 and 65535")

        max_roots = kwargs.get("max_roots")
        if max_roots is not None:
            if isinstance(max_roots, int):
                if max_roots <= 0:
                    raise ValueError(f"Max roots {max_roots} must be positive")
            else:
                raise TypeError("Max roots must be a positive integer")

        default_scan_interval_minutes = kwargs.get("default_scan_interval_minutes")
        if default_scan_interval_minutes is not None:
            if isinstance(default_scan_interval_minutes, int):
                if default_scan_interval_minutes <= 0:
                    raise ValueError(f"Default scan interval minutes {default_scan_interval_minutes} must be positive")
            else:
                raise TypeError("Default scan interval minutes must be a positive integer")

        return cls(
            name=name,
            os_type=os_type,
            os_version=os_version,
            user_id=user_id,
            **kwargs
        )

    class NodeUpdateOptions(TypedDict, total=False):
        name: str
        os_type: str
        os_version: str
        hostname: str
        ip_addresses: list[str]
        port: int
        max_roots: int
        default_scan_interval_minutes: int

    def update(self, **kwargs: Unpack[NodeUpdateOptions]) -> bool:
        """
            Updates the entity.

            Returns:
                bool: True if at least one field was changed, False otherwise.
        """
        allowed_fields = {
            "name",
            "os_type",
            "os_version",
            "hostname",
            "ip_addresses",
            "port",
            "max_roots",
            "default_scan_interval_minutes",
        }

        unknown = set(kwargs) - allowed_fields
        if unknown:
            raise ValueError(f"Unknown fields {unknown}")

        name = kwargs.get("name")
        if name is not None:
            if len(str(name).strip()) < 3:
                raise ValueError("Name must be at least 3 character long")

        hostname = kwargs.get("hostname")
        if hostname  is not None:
            if not HOSTNAME_REGEX.match(str(hostname)):
                raise ValueError("Hostname is invalid")

        ip_addresses = kwargs.get("ip_addresses")
        if ip_addresses is not None:
            if not isinstance(ip_addresses, list):
                raise TypeError("Ip addresses must be a list")
            for ip in ip_addresses:
                try:
                    ipaddress.ip_address(ip)
                except ValueError:
                    raise ValueError(f"Invalid IP address: {ip}")

        port = kwargs.get("port")
        if port is not None:
            if isinstance(port, int):
                if port <= 0 or port > 65535:
                    raise ValueError(f"Port {port} must be between 1 and 65535")
            else:
                raise TypeError("Port must be an integer between 1 and 65535")

        max_roots = kwargs.get("max_roots")
        if max_roots is not None:
            if isinstance(max_roots, int):
                if max_roots <= 0:
                    raise ValueError(f"Max roots {max_roots} must be positive")
            else:
                raise TypeError("Max roots must be a positive integer")

        default_scan_interval_minutes = kwargs.get("default_scan_interval_minutes")
        if default_scan_interval_minutes is not None:
            if isinstance(default_scan_interval_minutes, int):
                if default_scan_interval_minutes <= 0:
                    raise ValueError(f"Default scan interval minutes {default_scan_interval_minutes} must be positive")
            else:
                raise TypeError("Default scan interval minutes must be a positive integer")

        was_updated = False
        for key, value in kwargs.items():
            setattr(self, key, value)
            was_updated = True

        if was_updated:
            self.updated_at = datetime.now()

        return was_updated