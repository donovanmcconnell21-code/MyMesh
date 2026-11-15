# MyMesh TODOs

- [x] Verify listener cleanup — Run menu option 3 twice and confirm both attempts work.
- [x] Fix stale node registrations — listener_test.py loads nodes.json on import, so newly registered nodes aren't immediately recognized by its callback.
- [x] Fix failed-connection cleanup — Handle a disconnected Meshtastic device without crashing
- [ ] Improve telemetry output — Prevent the listener and node report from printing over each other.
- [ ] Handle delayed telemetry responses — Avoid closing the radio before a slower node responds.
- [x] Clean up registration output — Don't show red duplicate warnings when there are zero duplicates.
- [ ] Improve historical telemetry storage — Handle timestamps, duplicate measurements, and reliable JSON saving.
- [ ] Build historical telemetry graphs — Show solar generation, battery voltage, and other measurements over time.
- [x] Save node registrations - Add a manual Save Nodes option
- [ ] Add a delete node option
- [x] Separate monitoring, current telemetry, and historical telemetry views
- [ ] Clean up float presicion
- [x] Handle telemetry request timeouts without stopping monitoring.
- [x] Prevent duplicate telemetry records.
- [ ] Protect telemetry history from incomplete JSON writes.
- [ ] Make file paths independent of working directory.
- [ ] Add README.md and Python dependency list.
- [ ] Add automated tests using simulated telemetry packets.
- [ ] except Exception is acceptable for this exercise, but eventually we'll narrow it to the specific Meshtastic exceptions we expect.
- [x] Limit in-memory duplicate detection to recent packets.
- [x] Verify atomic telemetry-history saving.
  - Back up telemetry_history.json.
  - Confirm new measurements are saved.
  - Confirm telemetry_history.json.tmp disappears after a successful save.
- [ ] Handle missing radio connections in standalone listener_test.py.
  - Check radio.devPath before requesting telemetry.
  - Skip requests when no serial device is connected.
  - Exit cleanly without calling close() on an uninitialized connection.
- [x] Handle incoming telemetry packets missing a fromId.
## Future Enhancements

- [ ] Add Bluetooth LE connection support to MyMesh.
- [ ] Allow users to select USB, BLE, or TCP connections.
- [ ] Investigate node configuration management through Python.
- [ ] Design reusable configuration profiles for different node types.
- [ ] Support exporting, backing up, and applying node configurations.
- [ ] figure out how to get a node to broadcast a dad joke each morning from icanhazdadjoke
- [ ] add a "search settings" feature