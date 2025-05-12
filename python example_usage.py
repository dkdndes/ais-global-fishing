
Features
---------

* Search or SQL-like *where* queries (`search_vessels`)
* Bulk identity lookup (`get_vessels_bulk`)
* Track & trajectory helpers (`get_track`, `get_segments`)
* Behavioural events (`get_events`, `get_encounters` …)
* Port visits, trips, risk scores
* Graceful handling of missing endpoints (HEAD pre-check)
* Fully documented & typed; ready for **async** conversion later

> The library purposely keeps a 1-to-1 mapping with the HTTP API.  
> There is **no hidden caching or implicit pagination** – what you see in the
> JSON is what the server returned.

