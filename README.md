# MyMesh

**MyMesh** is a work-in-progress, Python-based command-line application for managing a personal [Meshtastic](https://meshtastic.org/) node list and collecting device and solar telemetry over a connected Meshtastic radio.

The project is being developed as a hands-on Python learning project. It is functional, but **experimental**: expect rough edges, incomplete features, and changes as development continues.

## What it does today

- **Register and manage a local node list** with friendly names, Meshtastic node IDs, and a `has_solar` setting.
- **Detect duplicate IDs** during registration and display registered nodes.
- **Save node registrations on demand**, save and exit, or exit without saving new changes.
- **Show a node telemetry snapshot** from the connected radio's node database, including available battery voltage, battery status, signal-to-noise ratio (SNR), last-heard time, and other mesh information.
- **Start a live monitoring session** that listens for incoming telemetry until you press Enter.
- **Request power telemetry** from registered nodes marked `has_solar: true` when monitoring starts.
- **Record device and solar measurements** to a local JSON history file, including timestamps and node IDs.

Live monitoring and viewing a snapshot are deliberately separate modes. Historical graphing and a persistent background monitor are planned, but **not implemented yet**.

## Requirements

- **Python 3.12 or newer** (developed using Python 3.13).
- A Meshtastic-compatible device connected over USB serial, with the device and its mesh configured appropriately.
- Python packages: [`meshtastic`](https://pypi.org/project/meshtastic/) and [`PyPubSub`](https://pypi.org/project/PyPubSub/).

The reviewed development environment uses `meshtastic` 2.7.11 and `PyPubSub` 4.0.7. Other versions have not been verified for this checkpoint.

## Getting started

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install meshtastic PyPubSub
python myMesh.py
```

On Windows, activate the virtual environment with `.venv\Scripts\activate` instead.

**Run MyMesh from the project directory.** The current version reads and writes its JSON files relative to the terminal's working directory.

### Menu

| Option | Action |
| --- | --- |
| 1 | Register node(s) |
| 2 | Show registered nodes |
| 3 | Show node telemetry snapshot |
| 4 | Save nodes without exiting |
| 5 | Start monitoring |
| 6 | Save and exit |
| 7 | Exit without saving node-list changes |

Select **5 — Start Monitoring** to keep the radio connected, receive telemetry events, and save incoming measurements. Press **Enter** to end the monitoring session and return to the menu. A monitoring session requires MyMesh to remain running.

## Node configuration and telemetry data

MyMesh creates `nodes.json` when you choose a save option. Each registration has a friendly name, a node ID, and a boolean indicating whether the node has solar telemetry. For example, with **placeholder** IDs:

```json
[
  {
    "name": "Portable Node",
    "ID": "!00000001",
    "has_solar": false
  },
  {
    "name": "Solar Node",
    "ID": "!22222222",
    "has_solar": true
  }
]
```

Incoming measurements are appended to an in-memory list and saved in `telemetry_history.json` as JSON records. Examples of the two record types:

```json
{
  "node_id": "!00000001",
  "timestamp": "2026-11-12T09:30:00-06:00",
  "voltage": 4.1,
  "battery_level": null,
  "type": "device"
}
```

```json
{
  "node_id": "!22222222",
  "timestamp": "2026-11-12T09:30:00-06:00",
  "solar_voltage": 4.4,
  "solar_current": 85.0,
  "solar_mW": 374.0,
  "type": "power"
}
```

Solar measurement handling currently expects voltage and current in **power metrics channel 3** (`ch3Voltage` in volts and `ch3Current` in milliamps), as used by the hardware in this project. Power is calculated in milliwatts (`V × mA = mW`). Other solar monitoring setups may need adjustments.

The Meshtastic battery-level value `101` is stored as JSON `null` rather than as a battery percentage.

Both `nodes.json` and `telemetry_history.json` are excluded by `.gitignore` because they contain personal mesh information. **Do not publish these files without reviewing their contents.**

## Project files

| File | Purpose |
| --- | --- |
| `myMesh.py` | Main CLI, node registration, telemetry snapshots, and monitoring controls |
| `listener_test.py` | Telemetry callback, solar telemetry requests, and JSON history saving (currently imported by the main application) |
| `TODO.md` | Development tasks and known improvements |
| `force_metrics.py`, `radio_test.py`, `telemetry_test.py` | Earlier development and hardware experiments |

## Current limitations and plans

MyMesh is still under development. Known areas for improvement include:

- Handling unresponsive nodes and delayed telemetry requests gracefully.
- Preventing duplicate telemetry records and making history writes safer as data grows.
- Improving concurrent terminal output while telemetry arrives.
- Supporting node deletion and historical telemetry graphs.
- Making file paths independent of the launch directory.
- Adding automated tests and eventually supporting long-running monitoring on a Raspberry Pi.

See [`TODO.md`](TODO.md) for the current task list.

## Authorship and AI disclosure

**The MyMesh application code and other project work were written by the project author.** ChatGPT was used as a learning and code-review assistant during development, but did not write the application code.

**This `README.md` was generated by ChatGPT (OpenAI)** at the author's request, based on a review of the project at this checkpoint.
