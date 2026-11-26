#!/usr/bin/env python3
"""Regenerate the built-in Iran Lite rule list from pinned GeoSite and GeoIP inputs."""

import gzip
import hashlib
import ipaddress
import json
from pathlib import Path
from urllib.request import urlopen

CHOCOLATE = "https://github.com/Chocolate4U/Iran-v2ray-rules/releases/download/202611251453/"
BOOTMORTIS = "https://github.com/bootmortis/iran-hosted-domains/releases/download/202610230802/"
SOURCES = {
    "geosite.dat": (CHOCOLATE, "7b8025038eacfe89b3bf8b4bee0c27d5769e6c78e276279cf09cb8118e503a2e"),
    "geoip.dat": (CHOCOLATE, "feb0a85645cc954fc2ce551725f7299de938605a911fd6ed9016983d3b3274b3"),
    "iran.dat": (BOOTMORTIS, "bfc270531c9a7ab159fbe4536c23fbeb073454b2cba9c687b34bd81f646e98d4"),
}
CATEGORIES = (
    "ir", "category-ir", "category-mobile-repair",
    *(f"category-{name}-ir" for name in (
        "ads", "bank", "bourse", "education", "forums", "gov", "insurance",
        "media", "news", "payment", "scholar", "shopping", "social-media", "tech", "travel",
    )),
)
DOMAINS = (
    "ir", "xn--mgba3a4f16a", "ipmyp.ir", "eitaa.com", "bale.ai", "gap.im", "gaplication.com",
    "zarinpal.com", "behpardakht.com", "mydigipay.com", "vandar.app", "vandar.io",
    "bank-keshavarzi.com", "karafarinbank.com", "qmehr724.com",
)
OUTPUT = Path(__file__).resolve().parents[1] / "v2rayN/ServiceLib/Sample/custom_routing_iran_lite.gz"


def varint(data, position):
    value = 0
    for shift in range(0, 64, 7):
        byte = data[position]
        position += 1
        value |= (byte & 127) << shift
        if byte < 128:
            return value, position
    raise ValueError("Invalid protobuf varint")


def fields(data):
    position = 0
    while position < len(data):
        tag, position = varint(data, position)
        wire_type = tag & 7
        if wire_type == 0:
            value, position = varint(data, position)
        elif wire_type == 2:
            length, position = varint(data, position)
            if position + length > len(data):
                raise ValueError("Truncated protobuf field")
            value = data[position:position + length]
            position += length
        else:
            raise ValueError(f"Unsupported protobuf wire type {wire_type}")
        yield tag >> 3, value


def read_lists(name):
    base, expected = SOURCES[name]
    with urlopen(base + name, timeout=60) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f"Checksum mismatch for {name}")
    lists = {}
    for tag, group in fields(data):
        if tag == 1:
            values = list(fields(group))
            code = next(value for number, value in values if number == 1).decode()
            lists[code.lower()] = [dict(fields(value)) for number, value in values if number == 2]
    return lists


def domain_rules():
    geosite = read_lists("geosite.dat")
    hosted = read_lists("iran.dat")
    domains = {f"domain:{domain}" for domain in DOMAINS}
    for entries in (*(geosite[name] for name in CATEGORIES), hosted["other"]):
        for entry in entries:
            kind = ("keyword", "regexp", "domain", "full")[entry.get(1, 0)]
            value = entry[2].decode()
            if kind in {"domain", "full"}:
                value = value.encode("idna").decode().lower()
                # The TLD rules already cover every entry below these suffixes.
                if value.endswith((".ir", ".xn--mgba3a4f16a")):
                    continue
            domains.add(f"{kind}:{value}")
    return sorted(domains)


def ip_rules():
    geoip = read_lists("geoip.dat")
    networks = {4: [], 6: []}
    for category in ("ir", "iranserver", "private"):
        for entry in geoip[category]:
            network = ipaddress.ip_network((entry[1], entry.get(2, 0)))
            networks[network.version].append(network)
    return [str(network) for group in networks.values() for network in ipaddress.collapse_addresses(group)]


def main():
    domains = domain_rules()
    ips = ip_rules()
    rules = [
        {"remarks": "Iran domains", "outboundTag": "direct", "domain": domains, "enabled": True},
        {"remarks": "Iran and private IP ranges", "outboundTag": "direct", "ip": ips, "enabled": True},
        {"remarks": "Other destinations", "outboundTag": "proxy", "port": "0-65535", "enabled": True},
    ]
    payload = json.dumps(rules, ensure_ascii=True, separators=(",", ":")).encode()
    with OUTPUT.open("wb") as output, gzip.GzipFile(filename="", fileobj=output, mode="wb", mtime=0) as packed:
        packed.write(payload)
    print(f"{len(domains)} domain matchers and {len(ips)} CIDRs, {OUTPUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
