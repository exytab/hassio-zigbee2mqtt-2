# Zigbee2MQTT 2

A second Zigbee2MQTT instance for Home Assistant, for a second coordinator.

Home Assistant allows only one installed copy of any add-on slug. Upstream ships
`zigbee2mqtt` (stable, versioned) and `zigbee2mqtt_edge` (dev branch, version string
permanently `edge`, so Supervisor never re-pulls it and it silently freezes at whatever
image was current on install day).

This add-on is the **stock upstream stable add-on** under a different slug, so a second
coordinator can run the same pinned, versioned release as the first.

Differences from upstream `zigbee2mqtt`:

| Field | Upstream | Here |
|---|---|---|
| `slug` | `zigbee2mqtt` | `zigbee2mqtt_2` |
| `name` | Zigbee2MQTT | Zigbee2MQTT 2 |
| `ports` | publishes host `8485/tcp` | not published (the first instance owns it) |
| `options.data_path` | `/config/zigbee2mqtt` | `/config/zigbee2mqtt_2` |

`image` and `version` are untouched: Supervisor pulls the official
`ghcr.io/zigbee2mqtt/zigbee2mqtt-{arch}:2.14.1-1`. Nothing is built locally and no
Zigbee2MQTT code is forked.

## Updating

Bump `version` in `zigbee2mqtt_2/config.json` to the tag upstream ships, and Home
Assistant will offer the update as normal.
