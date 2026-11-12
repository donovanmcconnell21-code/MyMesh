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
- [ ] Separate monitoring, current telemetry, and historical telemetry views