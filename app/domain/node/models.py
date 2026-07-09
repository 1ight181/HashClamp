from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, TypedDict, Unpack
from uuid import UUID, uuid4

import ipaddress
import re

from exceptions import (
    InvalidNodeDataError,
    InvalidNodeUpdateError,
)


HOSTNAME_REGEX = re.compile(
    r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
)


@dataclass
class Node:
    name: str

    os_type: str
    os_version: str

    user_id: UUID

    id: UUID = field(
        init=False,
        default_factory=uuid4,
    )

    hostname: Optional[str] = None
    ip_addresses: Optional[list[str]] = None
    port: Optional[int] = None

    max_roots: int = 50
    default_scan_interval_minutes: int = 30

    created_at: datetime = field(
        init=False,
        default_factory=lambda: datetime.now(timezone.utc),
    )

    updated_at: datetime = field(
        init=False,
        default_factory=lambda: datetime.now(timezone.utc),
    )


    class NodeCreateOptions(TypedDict, total=False):
        hostname: str
        ip_addresses: list[str]
        port: int
        max_roots: int
        default_scan_interval_minutes: int


    @classmethod
    def create(
            cls,
            name: str,
            os_type: str,
            os_version: str,
            user_id: UUID,
            **kwargs: Unpack[NodeCreateOptions],
    ) -> "Node":

        cls._validate_name(name)
        cls._validate_os_type(os_type)
        cls._validate_os_version(os_version)

        if not user_id:
            raise InvalidNodeDataError(
                "User id cannot be empty"
            )

        hostname = kwargs.get("hostname")
        if hostname is not None:
            cls._validate_hostname(hostname)

        ip_addresses = kwargs.get("ip_addresses")
        if ip_addresses is not None:
            cls._validate_ip_addresses(ip_addresses)

        port = kwargs.get("port")
        if port is not None:
            cls._validate_port(port)

        max_roots = kwargs.get("max_roots")
        if max_roots is not None:
            cls._validate_max_roots(max_roots)

        scan_interval = kwargs.get(
            "default_scan_interval_minutes"
        )

        if scan_interval is not None:
            cls._validate_scan_interval(scan_interval)

        return cls(
            name=name,
            os_type=os_type,
            os_version=os_version,
            user_id=user_id,
            **kwargs,
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


    def update(
            self,
            **kwargs: Unpack[NodeUpdateOptions],
    ) -> bool:

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

        unknown_fields = set(kwargs) - allowed_fields

        if unknown_fields:
            raise InvalidNodeUpdateError(
                f"Unknown fields: {unknown_fields}"
            )


        try:
            name = kwargs.get("name")
            if name is not None:
                self._validate_name(name)


            os_type = kwargs.get("os_type")
            if os_type is not None:
                self._validate_os_type(os_type)


            os_version = kwargs.get("os_version")
            if os_version is not None:
                self._validate_os_version(os_version)


            hostname = kwargs.get("hostname")
            if hostname is not None:
                self._validate_hostname(hostname)


            ip_addresses = kwargs.get("ip_addresses")
            if ip_addresses is not None:
                self._validate_ip_addresses(ip_addresses)


            port = kwargs.get("port")
            if port is not None:
                self._validate_port(port)


            max_roots = kwargs.get("max_roots")
            if max_roots is not None:
                self._validate_max_roots(max_roots)


            scan_interval = kwargs.get(
                "default_scan_interval_minutes"
            )

            if scan_interval is not None:
                self._validate_scan_interval(scan_interval)


        except InvalidNodeDataError as error:
            raise InvalidNodeUpdateError(
                str(error)
            )


        if not kwargs:
            return False


        for key, value in kwargs.items():
            setattr(self, key, value)


        self.updated_at = datetime.now(timezone.utc)

        return True


    @staticmethod
    def _validate_name(name: str) -> None:
        if len(name.strip()) < 3:
            raise InvalidNodeDataError(
                "Name must be at least 3 characters long"
            )


    @staticmethod
    def _validate_os_type(os_type: str) -> None:
        if not os_type.strip():
            raise InvalidNodeDataError(
                "OS type cannot be empty"
            )


    @staticmethod
    def _validate_os_version(os_version: str) -> None:
        if not os_version.strip():
            raise InvalidNodeDataError(
                "OS version cannot be empty"
            )


    @staticmethod
    def _validate_hostname(hostname: str) -> None:
        if not HOSTNAME_REGEX.match(hostname):
            raise InvalidNodeDataError(
                "Hostname is invalid"
            )


    @staticmethod
    def _validate_ip_addresses(
            ip_addresses: list[str],
    ) -> None:

        for ip in ip_addresses:
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                raise InvalidNodeDataError(
                    f"Invalid IP address: {ip}"
                )


    @staticmethod
    def _validate_port(port: int) -> None:
        if port < 1 or port > 65535:
            raise InvalidNodeDataError(
                "Port must be between 1 and 65535"
            )


    @staticmethod
    def _validate_max_roots(max_roots: int) -> None:
        if max_roots <= 0:
            raise InvalidNodeDataError(
                "Max roots must be positive"
            )


    @staticmethod
    def _validate_scan_interval(
            scan_interval_minutes: int,
    ) -> None:

        if scan_interval_minutes <= 0:
            raise InvalidNodeDataError(
                "Default scan interval must be positive"
            )