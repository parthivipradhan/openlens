"""
Seed demo data — Chandigarh, India (Phase 2 Expanded).

Creates:
- 5 multi-tier sources (Municipal Corporation, OpenStreetMap, CTU Transit, CPCC, Citizen Collective)
- 5 dataset manifests with provenance, licenses, and coverage
- 5 locality records (Chandigarh sectors and neighbourhoods)
- 30+ curated synthetic evidence records across 9 categories with SHA-256 digests
- 25+ extracted evidence claims with model attribution
- 10+ evidence relations (supports, contradicts, duplicate_of, supersedes)
- 8+ review events forming an audit trail

Run: python scripts/seed_demo_data.py
Or:  make seed
"""

import asyncio
import hashlib
import json
import uuid
from datetime import datetime, timezone

import structlog
from sqlalchemy import select

from localitylens.core.config import settings
from localitylens.core.logging import setup_logging
from localitylens.db.session import AsyncSessionLocal, init_db
from localitylens.db.models import (
    DatasetManifest,
    EvidenceClaim,
    EvidenceRecord,
    EvidenceRelation,
    Locality,
    ReviewEvent,
    Source,
)

setup_logging()
log = structlog.get_logger(__name__)

NOW = datetime.now(timezone.utc)


def compute_digest(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


LOCALITIES = [
    {"name": "Sector 17", "locality_type": "sector", "alternative_names": ["City Centre", "Sector-17"]},
    {"name": "Sector 22", "locality_type": "sector", "alternative_names": ["Sector-22", "Shastri Market Sector"]},
    {"name": "Sector 35", "locality_type": "sector", "alternative_names": ["Sector-35", "Hospitality Zone"]},
    {"name": "Manimajra", "locality_type": "neighbourhood", "alternative_names": ["Mani Majra", "Old Town"]},
    {"name": "Industrial Area Phase 1", "locality_type": "industrial", "alternative_names": ["Phase 1", "Chandigarh Industrial Hub"]},
]

SOURCES = [
    {
        "id": "mcc-notices",
        "name": "Municipal Corporation Chandigarh (MCC)",
        "source_url": "http://mcchandigarh.gov.in/public-notices",
        "source_type": "govt",
        "publisher": "Municipal Corporation of Chandigarh",
        "license": "Government Open Data License - India (GODL)",
        "attribution": "Data published under GODL India by Municipal Corporation Chandigarh",
        "authority_classification": "official_municipal",
        "update_cadence": "daily",
        "status": "active",
    },
    {
        "id": "osm-chandigarh",
        "name": "OpenStreetMap Chandigarh Community",
        "source_url": "https://www.openstreetmap.org/relation/1949572",
        "source_type": "osm",
        "publisher": "OpenStreetMap Contributors",
        "license": "ODbL 1.0",
        "attribution": "© OpenStreetMap contributors, ODbL 1.0",
        "authority_classification": "open_geospatial",
        "update_cadence": "weekly",
        "status": "active",
    },
    {
        "id": "ctu-transit",
        "name": "Chandigarh Transport Undertaking (CTU)",
        "source_url": "https://chdctu.gov.in/routes",
        "source_type": "govt",
        "publisher": "Department of Transport, Chandigarh Administration",
        "license": "Government Open Data License - India (GODL)",
        "attribution": "Chandigarh Transport Undertaking official schedule notices",
        "authority_classification": "official_transport",
        "update_cadence": "weekly",
        "status": "active",
    },
    {
        "id": "cpcc-environment",
        "name": "Chandigarh Pollution Control Committee (CPCC)",
        "source_url": "https://cpcc.chd.gov.in/air-quality-bulletins",
        "source_type": "govt",
        "publisher": "Chandigarh Pollution Control Committee",
        "license": "Government Open Data License - India (GODL)",
        "attribution": "CPCC Continuous Ambient Air Quality Monitoring Network",
        "authority_classification": "official_environmental",
        "update_cadence": "daily",
        "status": "active",
    },
    {
        "id": "chandigarh-citizen-reports",
        "name": "Chandigarh Urban Observation Collective",
        "source_url": "https://example.localitylens.dev/citizen-reports",
        "source_type": "community",
        "publisher": "Independent Urban Watch Chandigarh",
        "license": "CC-BY-4.0",
        "attribution": "Civic observations aggregated with synthetic demo labels",
        "authority_classification": "community_crowdsourced",
        "update_cadence": "realtime",
        "status": "active",
    },
]

MANIFESTS = [
    {
        "dataset_identifier": "mcc-notices-v1",
        "name": "MCC Public Notices & Maintenance Records",
        "publisher": "Municipal Corporation Chandigarh",
        "original_url": "http://mcchandigarh.gov.in",
        "license": "GODL India",
        "attribution": "Municipal Corporation of Chandigarh",
        "geographic_coverage": "Chandigarh Union Territory",
        "temporal_coverage": "2025–2026",
        "imported_fields": ["notice_title", "sector", "work_type", "published_date", "completion_estimate"],
        "transformations": ["Structured extraction via open LLM", "Spatial sector centroid geocoding"],
        "redistribution_permitted": True,
        "known_limitations": [
            "Official notices may not reflect unscheduled field delays.",
            "Sector names reference bounding centroids rather than exact work pinpoints.",
        ],
    },
    {
        "dataset_identifier": "osm-chandigarh-v1",
        "name": "OpenStreetMap Chandigarh Amenities & Green Spaces",
        "publisher": "OpenStreetMap Contributors",
        "original_url": "https://www.openstreetmap.org",
        "license": "ODbL 1.0",
        "attribution": "© OpenStreetMap contributors",
        "geographic_coverage": "Chandigarh Sectors 1 through 60",
        "temporal_coverage": "2024–2026",
        "imported_fields": ["amenity", "leisure", "name", "coordinates", "osm_id"],
        "transformations": ["WGS-84 point extraction", "Category assignment"],
        "redistribution_permitted": True,
        "known_limitations": [
            "Crowdsourced amenities require community verification.",
            "Opening hours and maintenance conditions are not continuously refreshed.",
        ],
    },
    {
        "dataset_identifier": "ctu-transit-v1",
        "name": "CTU Public Bus Routes & Terminus Network",
        "publisher": "Chandigarh Transport Undertaking",
        "original_url": "https://chdctu.gov.in",
        "license": "GODL India",
        "attribution": "Chandigarh Transport Undertaking",
        "geographic_coverage": "Chandigarh Tri-city (Chandigarh, Mohali, Panchkula)",
        "temporal_coverage": "2025–2026",
        "imported_fields": ["route_code", "origin", "destination", "terminal_name", "operational_status"],
        "transformations": ["Route terminal linking", "Transit hub geocoding"],
        "redistribution_permitted": True,
        "known_limitations": [
            "Does not incorporate real-time GPS telemetry delays.",
            "Frequencies vary between peak and non-peak hours.",
        ],
    },
    {
        "dataset_identifier": "cpcc-environment-v1",
        "name": "CPCC Ambient Air Quality & Acoustic Monitoring",
        "publisher": "Chandigarh Pollution Control Committee",
        "original_url": "https://cpcc.chd.gov.in",
        "license": "GODL India",
        "attribution": "CPCC Ambient Air Quality Network",
        "geographic_coverage": "Chandigarh Sectors & Industrial Area",
        "temporal_coverage": "2025–2026",
        "imported_fields": ["station_name", "pollutant", "aqi_value", "measurement_timestamp"],
        "transformations": ["Threshold classification", "Temporal normalization"],
        "redistribution_permitted": True,
        "known_limitations": [
            "Fixed station telemetry does not represent hyper-local street canyons.",
            "Sensor calibration cycles occur quarterly.",
        ],
    },
    {
        "dataset_identifier": "citizen-reports-v1",
        "name": "Chandigarh Citizen Incident Reports (Synthetic Demo)",
        "publisher": "LocalityLens Synthetic Data Generator",
        "original_url": "https://localitylens.dev",
        "license": "CC0-1.0",
        "attribution": "LocalityLens synthetic fixtures",
        "geographic_coverage": "Chandigarh Sectors",
        "temporal_coverage": "2026 (synthetic)",
        "imported_fields": ["headline", "description", "location_text", "reported_date"],
        "transformations": ["Synthetic generation for demonstration and automated testing"],
        "redistribution_permitted": True,
        "known_limitations": [
            "All items in this dataset are synthetic demo fixtures.",
            "Do not represent real-world physical incidents or public grievances.",
        ],
    },
]

# 30 Curated Chandigarh demo records
DEMO_EVIDENCE_RECORDS = [
    {
        "slug": "ev-01",
        "source_id": "mcc-notices",
        "category": "waterlogging",
        "title": "[SYNTHETIC DEMO] Waterlogging mitigation works near Sector 17 underpass",
        "summary": "Municipal engineering branch advisory regarding monsoon drainage retrofitting and temporary pump installation at the Sector 17 underpass junction.",
        "original_location_text": "Sector 17 underpass, Chandigarh",
        "geocoding_precision": "sector",
        "published_at": "2026-08-15T10:00:00+05:30",
        "event_date": "2026-08-14T08:00:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "Work duration is an initial tender estimate."],
        "claim": {
            "claim_text": "High-capacity diesel dewatering pumps installed at Sector 17 underpass to prevent flooding.",
            "supporting_excerpt": "Engineering division deployed two 15 HP submersible pumps at Sector 17 pedestrian subway underpass.",
        },
    },
    {
        "slug": "ev-02",
        "source_id": "chandigarh-citizen-reports",
        "category": "waterlogging",
        "title": "[SYNTHETIC DEMO] Citizen report: Submerged footpath near Sector 17 Bank Square",
        "summary": "Pedestrian observation of severe water accumulation across the walkway connecting Sector 17 Bank Square to the Central Plaza following morning downpour.",
        "original_location_text": "Bank Square, Sector 17, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-08-15T12:30:00+05:30",
        "event_date": "2026-08-15T11:45:00+05:30",
        "review_status": "demo",
        "limitations": ["Synthetic demo fixture.", "Depth measurements are visual estimates without calibrated staff gauges."],
        "claim": {
            "claim_text": "Ankle-deep standing water observed blocking Bank Square pedestrian approach.",
            "supporting_excerpt": "Footpath completely inundated over 40 meters, forcing pedestrians onto vehicular lanes.",
        },
    },
    {
        "slug": "ev-03",
        "source_id": "mcc-notices",
        "category": "waterlogging",
        "title": "[SYNTHETIC DEMO] Drainage overflow near Sector 22 Shastri Market",
        "summary": "Municipal advisory reporting temporary storm water drain backflow near Sector 22 market parking bays following intense storm.",
        "original_location_text": "Shastri Market, Sector 22, Chandigarh",
        "geocoding_precision": "sector",
        "published_at": "2026-07-20T08:30:00+05:30",
        "event_date": "2026-07-20T06:00:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "Cleaning scheduled within 24 hours."],
        "claim": {
            "claim_text": "Storm drain line cleared of solid waste blockage near Sector 22 market rear lane.",
            "supporting_excerpt": "Sanitation quick-response team mobilized to desilt the 600mm stormwater conduit.",
        },
    },
    {
        "slug": "ev-04",
        "source_id": "chandigarh-citizen-reports",
        "category": "waterlogging",
        "title": "[SYNTHETIC DEMO] Citizen observation of chronic water accumulation in Manimajra low pockets",
        "summary": "Crowdsourced report documenting persistent pooling in Govindpura locality of Manimajra following rain events.",
        "original_location_text": "Govindpura, Manimajra, Chandigarh",
        "geocoding_precision": "neighbourhood",
        "published_at": "2026-08-10T07:00:00+05:30",
        "event_date": "2026-08-09T20:00:00+05:30",
        "review_status": "demo",
        "limitations": ["Synthetic demo fixture.", "Topographic depression prone to delayed percolation."],
        "claim": {
            "claim_text": "Residential lane waterlogged for over 18 hours due to inadequate gradient.",
            "supporting_excerpt": "Residents report rainwater enters ground floor entrance ramps during continuous rain.",
        },
    },
    {
        "slug": "ev-05",
        "source_id": "cpcc-environment",
        "category": "air_quality",
        "title": "[SYNTHETIC DEMO] Elevated PM2.5 concentrations near Industrial Area Phase 1",
        "summary": "Continuous ambient monitoring telemetry recording PM2.5 spike reaching 168 µg/m³ during shift transition and diesel freight loading.",
        "original_location_text": "Industrial Area Phase 1, Chandigarh",
        "geocoding_precision": "area",
        "published_at": "2026-09-01T06:00:00+05:30",
        "event_date": "2026-08-31T22:00:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "Micro-climatic inversion factor present."],
        "claim": {
            "claim_text": "Industrial Area ambient PM2.5 exceeded national ambient air quality standard by 2.8x.",
            "supporting_excerpt": "Peak 1-hour average recorded at 168 µg/m³ between 22:00 and 23:00 hrs.",
        },
    },
    {
        "slug": "ev-06",
        "source_id": "chandigarh-citizen-reports",
        "category": "air_quality",
        "title": "[SYNTHETIC DEMO] Citizen report: Visible particulate haze and odour near Phase 1 railway siding",
        "summary": "Resident observation of dense smoke drift across the border between Industrial Area Phase 1 and Sector 29.",
        "original_location_text": "Railway Siding, Industrial Area Phase 1, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-09-01T07:15:00+05:30",
        "event_date": "2026-08-31T23:30:00+05:30",
        "review_status": "demo",
        "limitations": ["Synthetic demo fixture.", "No particulate spectrometer on site."],
        "claim": {
            "claim_text": "Heavy industrial diesel exhaust noted drifting westward into adjoining residential pocket.",
            "supporting_excerpt": "Visual haze and burning fuel smell noted continuously over three hours.",
        },
    },
    {
        "slug": "ev-07",
        "source_id": "cpcc-environment",
        "category": "air_quality",
        "title": "[SYNTHETIC DEMO] Post-monsoon air quality recovery in Sector 17 commercial core",
        "summary": "Monitoring station Sector 17 logs Air Quality Index (AQI) of 42 (Good), reflecting atmospheric cleansing from widespread precipitation.",
        "original_location_text": "Sector 17, Chandigarh",
        "geocoding_precision": "sector",
        "published_at": "2026-08-20T14:00:00+05:30",
        "event_date": "2026-08-20T12:00:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "Temporary meteorological benefit."],
        "claim": {
            "claim_text": "Ambient AQI in Sector 17 improved to 'Good' category with PM2.5 below 20 µg/m³.",
            "supporting_excerpt": "Rain washout effect reduced respirable particulates across central sector radius.",
        },
    },
    {
        "slug": "ev-08",
        "source_id": "mcc-notices",
        "category": "road_closure",
        "title": "[SYNTHETIC DEMO] Scheduled resurfacing on Madhya Marg corridor near Sector 17",
        "summary": "Traffic engineering notice outlining phased overnight lane closures on Madhya Marg between Matka Chowk and Press Chowk.",
        "original_location_text": "Madhya Marg, Sector 17, Chandigarh",
        "geocoding_precision": "road",
        "published_at": "2026-09-10T09:00:00+05:30",
        "event_date": "2026-09-12T21:00:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "Weather dependent scheduling."],
        "claim": {
            "claim_text": "Madhya Marg restricted to single lane in each direction between 21:00 and 06:00.",
            "supporting_excerpt": "Bituminous resurfacing scheduled from 12 Sept to 18 Sept with traffic diversions via Sector 18.",
        },
    },
    {
        "slug": "ev-09",
        "source_id": "chandigarh-citizen-reports",
        "category": "road_closure",
        "title": "[SYNTHETIC DEMO] Citizen dispute: Resurfacing on Madhya Marg unfinished leaving hazardous gravel",
        "summary": "Motorist alert reporting unrolled stone aggregates and absent warning cones on the westbound carriageway of Madhya Marg.",
        "original_location_text": "Press Chowk, Madhya Marg, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-09-15T18:00:00+05:30",
        "event_date": "2026-09-15T16:30:00+05:30",
        "review_status": "disputed",
        "limitations": ["Synthetic demo fixture.", "Active construction zone."],
        "claim": {
            "claim_text": "Loose gravel on uncompacted lane causing two-wheeler skid hazard without warning signs.",
            "supporting_excerpt": "Multiple riders reporting near-miss skids near Press Chowk intersection.",
        },
    },
    {
        "slug": "ev-10",
        "source_id": "mcc-notices",
        "category": "road_closure",
        "title": "[SYNTHETIC DEMO] Emergency sewer pipe replacement near Sector 35 roundabout",
        "summary": "Civil works bulletin announcing diversion of vehicular movement on Himalaya Marg adjoining Sector 35 market for trunk sewer rehabilitation.",
        "original_location_text": "Himalaya Marg, Sector 35, Chandigarh",
        "geocoding_precision": "road",
        "published_at": "2026-08-28T11:00:00+05:30",
        "event_date": "2026-08-29T00:00:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "Excavation depth requires 48-hour cure."],
        "claim": {
            "claim_text": "Himalaya Marg stretch closed for 48 hours for collapsed brick sewer replacement.",
            "supporting_excerpt": "Traffic diverted through inner sector V4 grid road during trenching operations.",
        },
    },
    {
        "slug": "ev-11",
        "source_id": "ctu-transit",
        "category": "public_transport",
        "title": "[SYNTHETIC DEMO] CTU Route 206 electric bus frequency expansion: Manimajra to Sector 17 ISBT",
        "summary": "Transit department update introducing 6 additional low-floor zero-emission buses, dropping peak headway to 10 minutes.",
        "original_location_text": "Manimajra to Sector 17 ISBT, Chandigarh",
        "geocoding_precision": "road",
        "published_at": "2026-06-01T08:00:00+05:30",
        "event_date": "2026-06-05T06:00:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "Charging infrastructure readiness verified."],
        "claim": {
            "claim_text": "Route 206 headway improved from 20 minutes to 10 minutes during morning and evening rush.",
            "supporting_excerpt": "Six 9-meter air-conditioned electric buses deployed to ease corridor crowding.",
        },
    },
    {
        "slug": "ev-12",
        "source_id": "osm-chandigarh",
        "category": "public_transport",
        "title": "[SYNTHETIC DEMO] Inter-State Bus Terminus (ISBT) Sector 17 hub mapping record",
        "summary": "OpenStreetMap geospatial record verifying passenger terminal platforms, ticket concourse, and auto-rickshaw bays at Sector 17 ISBT.",
        "original_location_text": "ISBT Sector 17, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-01-01T00:00:00+05:30",
        "event_date": None,
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "Platform assignments subject to operational shift."],
        "claim": {
            "claim_text": "Sector 17 ISBT features 22 active bus bays and direct underground subway connectivity.",
            "supporting_excerpt": "Mapped node includes accessible ramp, prepaid taxi counter, and digital schedule displays.",
        },
    },
    {
        "slug": "ev-13",
        "source_id": "ctu-transit",
        "category": "public_transport",
        "title": "[SYNTHETIC DEMO] Smart passenger shelter installation at Sector 22 Aroma junction",
        "summary": "Deployment of real-time passenger information display (PIDS) and solar-lit shelter at Sector 22 Aroma Chowk.",
        "original_location_text": "Aroma Chowk, Sector 22, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-05-15T09:00:00+05:30",
        "event_date": "2026-05-14T10:00:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture."],
        "claim": {
            "claim_text": "Real-time bus arrival countdown screen activated at Sector 22 stop.",
            "supporting_excerpt": "PIDS linked to CTU intelligent transit tracking engine providing GPS vehicle time-to-arrival.",
        },
    },
    {
        "slug": "ev-14",
        "source_id": "osm-chandigarh",
        "category": "green_spaces",
        "title": "[SYNTHETIC DEMO] Zakir Hussain Rose Garden public recreation boundary record",
        "summary": "OpenStreetMap leisure polygon record mapping the 30-acre rose garden in Sector 16, comprising over 1,600 rose varieties.",
        "original_location_text": "Rose Garden, Sector 16, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-01-01T00:00:00+05:30",
        "event_date": None,
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "Illuminated walking track timing 05:00-21:00."],
        "claim": {
            "claim_text": "Rose Garden encompasses 30 acres of municipal parkland with wheelchair-accessible pathways.",
            "supporting_excerpt": "Designated public botanical space with paved circulatory trails and perimeter buffer planting.",
        },
    },
    {
        "slug": "ev-15",
        "source_id": "osm-chandigarh",
        "category": "green_spaces",
        "title": "[SYNTHETIC DEMO] Sukhna Lake recreational waterfront and migratory sanctuary",
        "summary": "Geospatial record detailing Sukhna Lake reservoir periphery, jogging promenade, and regulated wetland buffer zone.",
        "original_location_text": "Sukhna Lake, Sector 1, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-01-01T00:00:00+05:30",
        "event_date": None,
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "Silent zone acoustic restrictions enforced."],
        "claim": {
            "claim_text": "3-kilometer asphalt and clay running track along the dam embankment.",
            "supporting_excerpt": "Waterfront recreational belt protected under Shivalik foothill eco-sensitive zoning regulations.",
        },
    },
    {
        "slug": "ev-16",
        "source_id": "osm-chandigarh",
        "category": "green_spaces",
        "title": "[SYNTHETIC DEMO] Japanese Garden Sector 31 public amenity record",
        "summary": "OpenStreetMap leisure record of Japanese Garden Sector 31 featuring pagoda architectural pavilions and underground passage.",
        "original_location_text": "Japanese Garden, Sector 31, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-01-01T00:00:00+05:30",
        "event_date": None,
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture."],
        "claim": {
            "claim_text": "13-acre themed park connected across two phases via an illuminated underground tunnel.",
            "supporting_excerpt": "Features Japanese horticultural styling, water bodies, and meditation pergolas.",
        },
    },
    {
        "slug": "ev-17",
        "source_id": "osm-chandigarh",
        "category": "healthcare",
        "title": "[SYNTHETIC DEMO] Government Multi-Specialty Hospital (GMSH), Sector 16",
        "summary": "Public health infrastructure record for the 500-bed apex municipal civil hospital in Sector 16 providing 24/7 emergency response.",
        "original_location_text": "GMSH Sector 16, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-01-01T00:00:00+05:30",
        "event_date": None,
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "OPD appointment load varies by weekday."],
        "claim": {
            "claim_text": "GMSH Sector 16 provides round-the-clock emergency, trauma, and blood bank facilities.",
            "supporting_excerpt": "Tertiary district healthcare facility with level-2 trauma centre and specialized maternity wing.",
        },
    },
    {
        "slug": "ev-18",
        "source_id": "osm-chandigarh",
        "category": "healthcare",
        "title": "[SYNTHETIC DEMO] Government Medical College and Hospital (GMCH), Sector 32",
        "summary": "State teaching hospital record for GMCH Sector 32 offering multi-specialty cardiac, oncology, and surgical intensive care.",
        "original_location_text": "GMCH Sector 32, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-01-01T00:00:00+05:30",
        "event_date": None,
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture."],
        "claim": {
            "claim_text": "900-bed multi-specialty super-care referral hospital with intensive cardiac and neonatal care.",
            "supporting_excerpt": "Primary government referral medical institution for the northern regional cluster.",
        },
    },
    {
        "slug": "ev-19",
        "source_id": "chandigarh-citizen-reports",
        "category": "healthcare",
        "title": "[SYNTHETIC DEMO] Sector 22 Civil Dispensary queue times and medicine inventory update",
        "summary": "Community feedback review noting prompt morning queue clearance and availability of essential antihypertensive medicines.",
        "original_location_text": "Sector 22 Dispensary, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-08-18T11:00:00+05:30",
        "event_date": "2026-08-18T09:30:00+05:30",
        "review_status": "demo",
        "limitations": ["Synthetic demo fixture.", "Observations reflect single morning sample."],
        "claim": {
            "claim_text": "Average wait time from registration to doctor consultation under 25 minutes.",
            "supporting_excerpt": "Civil dispensary operates smoothly with full stock of primary generic pharmaceuticals.",
        },
    },
    {
        "slug": "ev-20",
        "source_id": "cpcc-environment",
        "category": "noise",
        "title": "[SYNTHETIC DEMO] Night acoustic baseline monitoring — Industrial Area Phase 1",
        "summary": "Ambient sound level survey recording equivalent sound level (Leq) of 68.4 dBA during late shift, within designated industrial zone limits.",
        "original_location_text": "Plot 18, Industrial Area Phase 1, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-07-05T22:00:00+05:30",
        "event_date": "2026-07-05T21:00:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "Microphone positioned 1.5m above grade per ISO 1996."],
        "claim": {
            "claim_text": "Industrial nighttime acoustic measurement recorded 68.4 dBA Leq (standard limit: 70 dBA).",
            "supporting_excerpt": "Readings compliant with Central Pollution Control Board industrial ambient criteria.",
        },
    },
    {
        "slug": "ev-21",
        "source_id": "chandigarh-citizen-reports",
        "category": "noise",
        "title": "[SYNTHETIC DEMO] Resident complaint: High decibel metal fabrication noise at residential border",
        "summary": "Grievance lodged by residents of Sector 29 West regarding sheet metal pressing vibrations audible after 22:00 hrs from Phase 1 fringe.",
        "original_location_text": "Sector 29 West / Phase 1 buffer, Chandigarh",
        "geocoding_precision": "area",
        "published_at": "2026-07-06T08:00:00+05:30",
        "event_date": "2026-07-05T23:15:00+05:30",
        "review_status": "demo",
        "limitations": ["Synthetic demo fixture.", "Recorded via uncalibrated smartphone app (73 dB estimate)."],
        "claim": {
            "claim_text": "Industrial fabrication noise intruding into residential apartments past 23:00 curfew.",
            "supporting_excerpt": "Rhythmic stamping sound exceeding residential nighttime ambient allowance.",
        },
    },
    {
        "slug": "ev-22",
        "source_id": "mcc-notices",
        "category": "infrastructure",
        "title": "[SYNTHETIC DEMO] Municipal scheduled water supply pressure maintenance in Sector 35",
        "summary": "Water supply division notice advising low pressure from Kajauli waterworks during overhead reservoir valve replacement in Sector 35.",
        "original_location_text": "Sector 35, Chandigarh",
        "geocoding_precision": "sector",
        "published_at": "2026-09-20T08:00:00+05:30",
        "event_date": "2026-09-22T04:00:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "Booster pump support available upon request."],
        "claim": {
            "claim_text": "Morning water pressure curtailed to 2.5 bar for scheduled reservoir sluice valve repair.",
            "supporting_excerpt": "Residents advised to store potable water for morning usage between 04:00 and 09:00.",
        },
    },
    {
        "slug": "ev-23",
        "source_id": "mcc-notices",
        "category": "infrastructure",
        "title": "[SYNTHETIC DEMO] Updated completion notice: Sector 35 waterworks valve successfully replaced",
        "summary": "Engineering completion certificate confirming full pressure restoration to Sector 35 water distribution lines ahead of schedule.",
        "original_location_text": "Sector 35, Chandigarh",
        "geocoding_precision": "sector",
        "published_at": "2026-09-22T10:30:00+05:30",
        "event_date": "2026-09-22T08:15:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture."],
        "claim": {
            "claim_text": "Water pressure normalized across all four sub-sectors of Sector 35 by 08:15 hrs.",
            "supporting_excerpt": "Hydrostatic pressure testing completed at 4.2 bar; full supply restored.",
        },
    },
    {
        "slug": "ev-24",
        "source_id": "mcc-notices",
        "category": "infrastructure",
        "title": "[SYNTHETIC DEMO] Smart LED streetlight conversion project along V3 arterial roads — Manimajra",
        "summary": "Public works bulletin detailing retrofitting of 450 sodium vapor streetlights with connected energy-efficient LED luminaires in Manimajra.",
        "original_location_text": "Manimajra, Chandigarh",
        "geocoding_precision": "neighbourhood",
        "published_at": "2026-09-18T10:00:00+05:30",
        "event_date": "2026-09-19T08:00:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture."],
        "claim": {
            "claim_text": "450 automated dimming LED fixtures installed to eliminate dark spots and cut power demand by 55%.",
            "supporting_excerpt": "Centralized control system enables real-time fault reporting and dynamic lux adjustments.",
        },
    },
    {
        "slug": "ev-25",
        "source_id": "osm-chandigarh",
        "category": "education",
        "title": "[SYNTHETIC DEMO] Panjab University historic campus boundary and faculty cluster record",
        "summary": "Geospatial mapping record of Panjab University Sector 14 campus, including AC Joshi Library, administrative blocks, and student hostels.",
        "original_location_text": "Sector 14, Chandigarh",
        "geocoding_precision": "sector",
        "published_at": "2026-01-01T00:00:00+05:30",
        "event_date": None,
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "Visitor vehicular passes required at Gate No. 2."],
        "claim": {
            "claim_text": "Panjab University campus covers 550 acres designed by Pierre Jeanneret with 78 teaching departments.",
            "supporting_excerpt": "Major educational campus landmark situated between Sector 14 and Sector 25.",
        },
    },
    {
        "slug": "ev-26",
        "source_id": "osm-chandigarh",
        "category": "education",
        "title": "[SYNTHETIC DEMO] Government Model Senior Secondary School (GMSSS) Sector 22 record",
        "summary": "Public school facility record for GMSSS Sector 22, detailing secondary classrooms, science laboratories, and athletic grounds.",
        "original_location_text": "GMSSS Sector 22, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-01-01T00:00:00+05:30",
        "event_date": None,
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture."],
        "claim": {
            "claim_text": "Public senior secondary school serving 1,800 students with smart classroom installations.",
            "supporting_excerpt": "Affiliated with Central Board of Secondary Education with full co-educational facilities.",
        },
    },
    {
        "slug": "ev-27",
        "source_id": "mcc-notices",
        "category": "infrastructure",
        "title": "[SYNTHETIC DEMO] Udyog Path road resurfacing completion and quality sign-off",
        "summary": "Municipal civil engineering bulletin marking the completion of asphalt overlay on Udyog Path connecting Sector 17 and Sector 22.",
        "original_location_text": "Udyog Path, Chandigarh",
        "geocoding_precision": "road",
        "published_at": "2026-09-05T16:00:00+05:30",
        "event_date": "2026-09-05T14:00:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture.", "5-year contractor maintenance warranty."],
        "claim": {
            "claim_text": "2.4 km dual carriage corridor resurfaced with dense bituminous macadam.",
            "supporting_excerpt": "Pavement roughness index tested below 2,000 mm/km; road reopened for unrestricted traffic.",
        },
    },
    {
        "slug": "ev-28",
        "source_id": "chandigarh-citizen-reports",
        "category": "infrastructure",
        "title": "[SYNTHETIC DEMO] Citizen observation of deep pothole developing on Udyog Path junction",
        "summary": "Commuter report asserting that a water supply trench cut across Udyog Path has sunk creating a hazardous depression.",
        "original_location_text": "Udyog Path / Sector 22 cut, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-09-08T09:00:00+05:30",
        "event_date": "2026-09-08T07:45:00+05:30",
        "review_status": "disputed",
        "limitations": ["Synthetic demo fixture."],
        "claim": {
            "claim_text": "Trench subsidence creates a 10cm dip across the newly paved fast lane.",
            "supporting_excerpt": "Vehicles braking abruptly near the Sector 22 turn off.",
        },
    },
    {
        "slug": "ev-29",
        "source_id": "chandigarh-citizen-reports",
        "category": "waterlogging",
        "title": "[SYNTHETIC DEMO] Duplicate report: Water stagnation near Sector 17 underpass entrance",
        "summary": "Duplicate citizen submission detailing recurring puddle accumulation outside the Sector 17 pedestrian subway.",
        "original_location_text": "Sector 17 underpass, Chandigarh",
        "geocoding_precision": "sector",
        "published_at": "2026-08-16T08:00:00+05:30",
        "event_date": "2026-08-15T10:00:00+05:30",
        "review_status": "demo",
        "limitations": ["Synthetic demo fixture.", "Flagged as duplicate of ev-01 and ev-02."],
        "claim": {
            "claim_text": "Subway entrance blocked by rainwater pool.",
            "supporting_excerpt": "Water remains present 24 hours after rain stopped.",
        },
    },
    {
        "slug": "ev-30",
        "source_id": "ctu-transit",
        "category": "public_transport",
        "title": "[SYNTHETIC DEMO] Inter-State Bus Terminus (ISBT) Sector 43 southern tri-city services update",
        "summary": "Transport department notice adding direct fast routes between ISBT Sector 43 and Industrial Area Phase 1 via Tribune Chowk.",
        "original_location_text": "ISBT Sector 43, Chandigarh",
        "geocoding_precision": "point",
        "published_at": "2026-07-10T11:00:00+05:30",
        "event_date": "2026-07-15T06:00:00+05:30",
        "review_status": "verified",
        "limitations": ["Synthetic demo fixture."],
        "claim": {
            "claim_text": "Direct worker express service operating at 15-minute intervals between ISBT 43 and Phase 1.",
            "supporting_excerpt": "Designated commuter route to alleviate shift traffic bottlenecks along Purv Marg.",
        },
    },
]


async def seed():
    await init_db()
    async with AsyncSessionLocal() as db:
        log.info("Starting comprehensive seed (Phase 2)...")

        # 1. Sources
        sources_by_id = {}
        for s_data in SOURCES:
            existing = await db.execute(select(Source).where(Source.id == s_data["id"]))
            src = existing.scalar_one_or_none()
            if not src:
                src = Source(**s_data)
                db.add(src)
                log.info("Created source", id=src.id, name=src.name)
            sources_by_id[s_data["id"]] = src

        # 2. Manifests
        for m_data in MANIFESTS:
            existing_m = await db.execute(
                select(DatasetManifest).where(DatasetManifest.dataset_identifier == m_data["dataset_identifier"])
            )
            if not existing_m.scalar_one_or_none():
                manifest = DatasetManifest(id=str(uuid.uuid4()), **m_data)
                db.add(manifest)
                log.info("Created manifest", identifier=m_data["dataset_identifier"])

        # 3. Localities
        for loc_data in LOCALITIES:
            existing_loc = await db.execute(select(Locality).where(Locality.name == loc_data["name"]))
            if not existing_loc.scalar_one_or_none():
                loc = Locality(id=str(uuid.uuid4()), **loc_data)
                db.add(loc)
                log.info("Created locality", name=loc_data["name"])

        await db.flush()

        # 4. Evidence Records & Claims
        records_by_slug = {}
        for ev_data in DEMO_EVIDENCE_RECORDS:
            slug = ev_data["slug"]
            existing_ev = await db.execute(
                select(EvidenceRecord).where(EvidenceRecord.title == ev_data["title"])
            )
            rec = existing_ev.scalar_one_or_none()
            if not rec:
                ev_id = str(uuid.uuid4())

                # Generate deterministic SHA-256 digest
                digest_payload = {
                    "id": ev_id,
                    "title": ev_data["title"],
                    "category": ev_data["category"],
                    "source_id": ev_data["source_id"],
                    "location": ev_data["original_location_text"],
                    "published_at": ev_data["published_at"],
                }
                canonical_digest = compute_digest(digest_payload)

                rec = EvidenceRecord(
                    id=ev_id,
                    source_id=ev_data["source_id"],
                    source_item_id=slug,
                    title=ev_data["title"],
                    summary=ev_data["summary"],
                    category=ev_data["category"],
                    original_location_text=ev_data["original_location_text"],
                    geocoding_precision=ev_data["geocoding_precision"],
                    published_at=datetime.fromisoformat(ev_data["published_at"]),
                    event_date=datetime.fromisoformat(ev_data["event_date"]) if ev_data.get("event_date") else None,
                    retrieved_at=NOW,
                    processed_at=NOW,
                    review_status=ev_data["review_status"],
                    archive_reference=f"urn:localitylens:archive:{slug}",
                    canonical_digest=canonical_digest,
                    limitations=ev_data["limitations"],
                    is_synthetic=True,
                )
                db.add(rec)
                await db.flush()

                # Add Claim
                if "claim" in ev_data:
                    c_info = ev_data["claim"]
                    claim = EvidenceClaim(
                        id=str(uuid.uuid4()),
                        evidence_id=rec.id,
                        claim_text=c_info["claim_text"],
                        supporting_excerpt=c_info["supporting_excerpt"],
                        extraction_model="qwen2.5:7b-instruct",
                        model_revision="sha:9f8a2b3c",
                        schema_version="v1.2.0",
                        review_status=rec.review_status,
                    )
                    db.add(claim)

            records_by_slug[slug] = rec

        await db.flush()

        # 5. Evidence Relations (corroborating, contradicting, duplicate, superseding)
        RELATION_FIXTURES = [
            ("ev-01", "ev-02", "supports"),        # Waterlogging notice corroborated by citizen report
            ("ev-05", "ev-06", "supports"),        # Sensor air quality spike supported by resident odour report
            ("ev-08", "ev-09", "contradicts"),     # Official road resurfacing timeline contradicted by loose gravel dispute
            ("ev-27", "ev-28", "contradicts"),     # Resurfacing sign-off contradicted by trench pothole alert
            ("ev-01", "ev-29", "duplicate_of"),    # ev-29 is duplicate of ev-01 underpass flooding
            ("ev-22", "ev-23", "supersedes"),      # Replacement completion notice supersedes earlier low-pressure advisory
            ("ev-11", "ev-30", "supports"),        # Transit route improvements mutually supporting
            ("ev-20", "ev-21", "contradicts"),     # Official sound compliance vs resident noise grievance
        ]

        for src_slug, tgt_slug, rel_type in RELATION_FIXTURES:
            src_rec = records_by_slug.get(src_slug)
            tgt_rec = records_by_slug.get(tgt_slug)
            if src_rec and tgt_rec:
                existing_rel = await db.execute(
                    select(EvidenceRelation).where(
                        EvidenceRelation.source_evidence_id == src_rec.id,
                        EvidenceRelation.target_evidence_id == tgt_rec.id,
                    )
                )
                if not existing_rel.scalar_one_or_none():
                    relation = EvidenceRelation(
                        id=str(uuid.uuid4()),
                        source_evidence_id=src_rec.id,
                        target_evidence_id=tgt_rec.id,
                        relation_type=rel_type,
                        review_status="active",
                        created_at=NOW,
                    )
                    db.add(relation)
                    log.info("Created relation", type=rel_type, src=src_slug, tgt=tgt_slug)

        # 6. Review Events (Audit Trail)
        REVIEW_FIXTURES = [
            ("ev-01", "verified", "Official municipal engineering division bulletin verified against tender document.", "admin_reviewer"),
            ("ev-02", "flagged_duplicate", "Candidate duplicate of municipal alert ev-01.", "community_bot"),
            ("ev-05", "verified", "Telemetry timestamp correlated with CPCC CAAQMS Sector 17 station.", "admin_reviewer"),
            ("ev-09", "disputed", "Contractor dispute regarding safety cone placement.", "field_inspector"),
            ("ev-22", "status_updated", "Maintenance window completed, status updated.", "admin_reviewer"),
            ("ev-23", "verified", "Hydrostatic sign-off document verified.", "admin_reviewer"),
            ("ev-28", "disputed", "Field team dispatched to inspect trench settling.", "municipal_liaison"),
            ("ev-29", "flagged_duplicate", "Marked as duplicate of ev-01 and ev-02.", "community_moderator"),
        ]

        for slug, action, reason, reviewer in REVIEW_FIXTURES:
            rec = records_by_slug.get(slug)
            if rec:
                existing_rev = await db.execute(
                    select(ReviewEvent).where(
                        ReviewEvent.evidence_id == rec.id,
                        ReviewEvent.action == action,
                    )
                )
                if not existing_rev.scalar_one_or_none():
                    rev = ReviewEvent(
                        id=str(uuid.uuid4()),
                        evidence_id=rec.id,
                        action=action,
                        reason=reason,
                        reviewer=reviewer,
                        previous_values={"review_status": "pending"},
                        created_at=NOW,
                    )
                    db.add(rev)

        await db.commit()
        log.info(
            "Phase 2 seed complete",
            sources=len(SOURCES),
            manifests=len(MANIFESTS),
            records=len(DEMO_EVIDENCE_RECORDS),
        )


if __name__ == "__main__":
    asyncio.run(seed())
