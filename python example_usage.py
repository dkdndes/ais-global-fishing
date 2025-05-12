"""
Documentation placeholder that was erroneously saved with a *.py* extension.

Features
--------

* Search or SQL-like *where* queries (`search_vessels`)
* Bulk identity lookup (`get_vessels_bulk`)
* Track & trajectory helpers (`get_track`, `get_segments`)
* Behavioural events (`get_events`, `get_encounters` ...)
* Port visits, trips, risk scores
* Graceful handling of missing endpoints (HEAD pre-check)
* Fully documented & typed; ready for async conversion later

The library keeps a strict 1-to-1 mapping with the HTTP API: there is no
hidden caching or implicit pagination – what you see in the JSON is
exactly what the server returned.
"""
