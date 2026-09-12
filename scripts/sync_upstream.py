#!/usr/bin/env python3
"""Regenerate zigbee2mqtt_2/config.json from the upstream stable add-on manifest.

Everything (version, image, schema, options, map, breaking_versions...) is taken
verbatim from upstream; only the overrides below are re-applied. That way a new
upstream release, or a new config option, lands here automatically instead of
this add-on silently drifting behind -- which is the exact failure mode of the
upstream `edge` add-on this one replaces.

Any failure exits non-zero on purpose: a red workflow run is visible, a silently
stale manifest is not.
"""
import json
import pathlib
import sys
import urllib.request

UPSTREAM = (
    "https://raw.githubusercontent.com/zigbee2mqtt/hassio-zigbee2mqtt"
    "/master/zigbee2mqtt/config.json"
)
TARGET = pathlib.Path(__file__).resolve().parent.parent / "zigbee2mqtt_2" / "config.json"

OVERRIDES = {
    "name": "Zigbee2MQTT 2",
    "slug": "zigbee2mqtt_2",
    "description": "Second Zigbee2MQTT instance (SONOFF dongle) - stock stable image, pinned",
    "url": "https://github.com/exytab/hassio-zigbee2mqtt-2/tree/main/zigbee2mqtt_2",
    # the first instance already publishes host 8485/tcp; a clash blocks startup
    "ports": {"8485/tcp": None, "8099/tcp": None},
}
OPTION_OVERRIDES = {"data_path": "/config/zigbee2mqtt_2"}


def main() -> int:
    with urllib.request.urlopen(UPSTREAM, timeout=30) as resp:
        if resp.status != 200:
            print(f"::error::upstream returned HTTP {resp.status}", file=sys.stderr)
            return 1
        cfg = json.loads(resp.read().decode())

    for key in ("version", "image", "schema", "options"):
        if key not in cfg:
            print(f"::error::upstream manifest has no '{key}' -- format changed?", file=sys.stderr)
            return 1

    cfg.update(OVERRIDES)
    cfg["options"].update(OPTION_OVERRIDES)

    new = json.dumps(cfg, indent=2) + "\n"
    old = TARGET.read_text(encoding="utf-8") if TARGET.exists() else ""
    if new == old:
        print(f"already in sync at {cfg['version']}")
        return 0

    TARGET.write_text(new, encoding="utf-8")
    print(f"synced to upstream {cfg['version']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
