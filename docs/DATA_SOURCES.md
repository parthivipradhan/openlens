# Data Sources — LocalityLens Chandigarh

All data sources used by LocalityLens are documented here.
Sources are also registered in the `sources` database table and tracked via `dataset_manifests`.

---

## Government / Municipal

| Source | Publisher | Type | License | Coverage |
|---|---|---|---|---|
| Chandigarh Municipal Corporation | MC Chandigarh | Government | Open (Public Sector) | Chandigarh UT |
| Punjab Pollution Control Board | PPCB | Government | Open | Air quality reports |
| Chandigarh Smart City | CSCLC | Government | Open | Infrastructure data |

## OpenStreetMap

| Source | Publisher | Type | License | Coverage |
|---|---|---|---|---|
| OpenStreetMap Overpass API | OpenStreetMap contributors | OSM | ODbL | All Chandigarh sectors |

OSM data is used for:
- Park and green space locations
- Bus stop and public transport stops
- Hospital and healthcare facility locations
- Road network for closure context

Attribution: © OpenStreetMap contributors

## Community / News

| Source | Publisher | Type | License | Notes |
|---|---|---|---|---|
| Tribune India | Tribune Trust | News | Fair use (excerpts only) | Incident reports |

## Demo / Synthetic Data

| Source | Publisher | Type | Notes |
|---|---|---|---|
| LocalityLens Demo Dataset | LocalityLens project | Synthetic | `is_synthetic=true` on all records. Not real observations. For UI development only. |

---

## Data Integrity Rules

1. `event_date`, `published_at`, `retrieved_at`, `processed_at` are always stored separately.
2. `original_location_text` is preserved unchanged alongside geocoded geometry.
3. Missing values are never replaced with zero or fabricated.
4. Synthetic/demo records always have `is_synthetic=True`.
5. All sources must have a `DatasetManifest` entry.

---

## Adding a New Source

1. Register the source in the database via the API or seed script.
2. Create a `DatasetManifest` entry with redistribution_permitted, license, and known_limitations.
3. Confirm the source URL passes SSRF validation (`validate_source_url`).
4. Set appropriate `authority_classification` (primary/secondary/tertiary).
