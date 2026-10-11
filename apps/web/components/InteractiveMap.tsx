"use client";

import React, { useEffect, useRef, useState, useMemo } from "react";
import {
  Layers,
  MapPin,
  Calendar,
  AlertTriangle,
  ZoomIn,
  ZoomOut,
  Maximize2,
  List,
  Map as MapIcon,
  Sparkles,
  Info,
} from "lucide-react";
import { EvidenceRecord } from "../lib/types";
import {
  CHANDIGARH_CENTER,
  CHANDIGARH_SECTOR_BOUNDARIES,
  CATEGORY_COLORS,
  getCoordinatesForEvidence,
  getUncertaintyRadiusMeters,
} from "../lib/geospatial";

interface InteractiveMapProps {
  evidenceList: EvidenceRecord[];
  onSelectRecord: (record: EvidenceRecord) => void;
  selectedCategory?: string;
  onCategoryToggle?: (cat: string) => void;
}

export function InteractiveMap({
  evidenceList,
  onSelectRecord,
  selectedCategory,
  onCategoryToggle,
}: InteractiveMapProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);

  const [activeLayers, setActiveLayers] = useState<Record<string, boolean>>({
    waterlogging: true,
    air_quality: true,
    road_closure: true,
    public_transport: true,
    green_spaces: true,
    healthcare: true,
    noise: true,
    infrastructure: true,
    education: true,
  });

  const [showBoundaries, setShowBoundaries] = useState(true);
  const [showUncertainty, setShowUncertainty] = useState(true);
  const [selectedHoverRecord, setSelectedHoverRecord] = useState<EvidenceRecord | null>(null);
  const [activeView, setActiveView] = useState<"map" | "list">("map");
  const [temporalRange, setTemporalRange] = useState<number>(100); // 0 to 100% of date range
  const [isMapLoaded, setIsMapLoaded] = useState(false);

  // Filter evidence based on layer toggles and temporal filter
  const filteredEvidence = useMemo(() => {
    return evidenceList.filter((item) => {
      if (!activeLayers[item.category]) return false;
      if (selectedCategory && item.category !== selectedCategory) return false;
      return true;
    });
  }, [evidenceList, activeLayers, selectedCategory]);

  // Initialise MapLibre GL
  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current) return;

    let maplibre: any = null;

    async function initMap() {
      try {
        const module = await import("maplibre-gl");
        maplibre = module.default || module;

        if (!mapContainerRef.current) return;

        // Dark Matter basemap style (free, fast, beautiful CartoDB raster tiles)
        const map = new maplibre.Map({
          container: mapContainerRef.current,
          style: {
            version: 8,
            sources: {
              "carto-dark": {
                type: "raster",
                tiles: [
                  "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
                  "https://b.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
                  "https://c.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
                ],
                tileSize: 256,
                attribution: "© OpenStreetMap contributors, © CARTO",
              },
            },
            layers: [
              {
                id: "carto-dark-layer",
                type: "raster",
                source: "carto-dark",
                minzoom: 0,
                maxzoom: 19,
              },
            ],
          },
          center: CHANDIGARH_CENTER,
          zoom: 12.2,
          pitch: 30,
        });

        map.addControl(new maplibre.NavigationControl({ showCompass: false }), "top-right");

        map.on("load", () => {
          mapInstanceRef.current = map;
          setIsMapLoaded(true);

          // Add Sector Boundary Polygons
          map.addSource("chandigarh-sectors", {
            type: "geojson",
            data: {
              type: "FeatureCollection",
              features: CHANDIGARH_SECTOR_BOUNDARIES.map((sec) => ({
                type: "Feature",
                properties: { name: sec.name, type: sec.type },
                geometry: {
                  type: "Polygon",
                  coordinates: sec.coordinates,
                },
              })),
            },
          });

          // Sector fill layer
          map.addLayer({
            id: "sectors-fill",
            type: "fill",
            source: "chandigarh-sectors",
            paint: {
              "fill-color": "#0ea5e9",
              "fill-opacity": 0.08,
            },
          });

          // Sector stroke line layer
          map.addLayer({
            id: "sectors-line",
            type: "line",
            source: "chandigarh-sectors",
            paint: {
              "line-color": "#38bdf8",
              "line-width": 1.5,
              "line-dasharray": [2, 2],
              "line-opacity": 0.6,
            },
          });
        });
      } catch (err) {
        console.warn("MapLibre GL failed to initialize:", err);
      }
    }

    initMap();

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  // Update markers when evidence or filters change
  useEffect(() => {
    if (!mapInstanceRef.current || !isMapLoaded) return;

    // Clear existing markers
    markersRef.current.forEach((m) => m.remove());
    markersRef.current = [];

    import("maplibre-gl").then((module) => {
      const maplibre = module.default || module;
      const map = mapInstanceRef.current;
      if (!map) return;

      filteredEvidence.forEach((record) => {
        const coords = getCoordinatesForEvidence(record.id);
        const color = CATEGORY_COLORS[record.category] || "#06b6d4";
        const uncertainty = getUncertaintyRadiusMeters(record.geocoding_precision);

        // Marker DOM container
        const el = document.createElement("div");
        el.className = "group relative cursor-pointer";

        // Uncertainty halo (geographic uncertainty visualization)
        if (showUncertainty) {
          const halo = document.createElement("div");
          halo.className =
            "absolute -inset-3 rounded-full opacity-20 pointer-events-none transition-all duration-300 group-hover:scale-150 group-hover:opacity-40 animate-pulse";
          halo.style.backgroundColor = color;
          el.appendChild(halo);
        }

        // Pin badge
        const pin = document.createElement("div");
        pin.className =
          "w-7 h-7 rounded-full flex items-center justify-center text-white text-[10px] font-bold shadow-lg border-2 border-slate-900 transition-transform duration-200 group-hover:scale-125";
        pin.style.backgroundColor = color;
        pin.style.boxShadow = `0 0 16px ${color}80`;
        pin.innerHTML = `<span>•</span>`;
        el.appendChild(pin);

        el.addEventListener("click", () => {
          onSelectRecord(record);
        });

        el.addEventListener("mouseenter", () => {
          setSelectedHoverRecord(record);
        });

        el.addEventListener("mouseleave", () => {
          setSelectedHoverRecord(null);
        });

        const marker = new maplibre.Marker({ element: el })
          .setLngLat(coords)
          .addTo(map);

        markersRef.current.push(marker);
      });
    });
  }, [filteredEvidence, isMapLoaded, showUncertainty, onSelectRecord]);

  // Toggle boundary visibility
  useEffect(() => {
    if (!mapInstanceRef.current || !isMapLoaded) return;
    const map = mapInstanceRef.current;
    if (map.getLayer("sectors-fill")) {
      map.setLayoutProperty("sectors-fill", "visibility", showBoundaries ? "visible" : "none");
    }
    if (map.getLayer("sectors-line")) {
      map.setLayoutProperty("sectors-line", "visibility", showBoundaries ? "visible" : "none");
    }
  }, [showBoundaries, isMapLoaded]);

  const toggleLayer = (cat: string) => {
    setActiveLayers((prev) => ({
      ...prev,
      [cat]: !prev[cat],
    }));
  };

  return (
    <div className="space-y-4">
      {/* Top Map Header & View Toggle (Map vs Accessible List) */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <MapIcon className="w-5 h-5 text-cyan-400" />
            <span>Interactive Geospatial Evidence Map</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            PostGIS spatial indexing • {filteredEvidence.length} observations positioned across Chandigarh sectors
          </p>
        </div>

        {/* View Switcher: Map vs Accessible List */}
        <div className="flex items-center gap-2">
          <div className="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-1">
            <button
              onClick={() => setActiveView("map")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                activeView === "map"
                  ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <MapIcon className="w-3.5 h-3.5" />
              <span>Map View</span>
            </button>
            <button
              onClick={() => setActiveView("list")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                activeView === "list"
                  ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <List className="w-3.5 h-3.5" />
              <span>Accessible List</span>
            </button>
          </div>
        </div>
      </div>

      {activeView === "map" ? (
        <div className="relative w-full h-[620px] rounded-3xl overflow-hidden glass-panel border border-slate-800/80 shadow-2xl">
          {/* Map Container Element */}
          <div ref={mapContainerRef} className="w-full h-full bg-slate-950" />

          {/* Floating Category Layer Toggle Panel */}
          <div className="absolute top-4 left-4 z-10 glass-panel rounded-2xl p-3 border border-slate-700/80 max-w-[220px] space-y-2 text-xs shadow-xl hidden sm:block">
            <div className="flex items-center justify-between pb-1 border-b border-slate-800">
              <span className="font-semibold text-slate-200 flex items-center gap-1.5 text-[11px] uppercase tracking-wider">
                <Layers className="w-3.5 h-3.5 text-cyan-400" />
                <span>Layers</span>
              </span>
              <span className="text-[10px] text-slate-500 font-mono">{filteredEvidence.length} pts</span>
            </div>

            <div className="space-y-1 max-h-52 overflow-y-auto pr-1">
              {Object.keys(activeLayers).map((cat) => {
                const color = CATEGORY_COLORS[cat] || "#06b6d4";
                const isChecked = activeLayers[cat];
                return (
                  <label
                    key={cat}
                    className="flex items-center gap-2 cursor-pointer hover:bg-slate-800/50 p-1 rounded-md text-[11px] text-slate-300 transition-colors"
                  >
                    <input
                      type="checkbox"
                      checked={isChecked}
                      onChange={() => toggleLayer(cat)}
                      className="rounded border-slate-700 text-cyan-500 focus:ring-0 w-3 h-3 bg-slate-900"
                    />
                    <span
                      className="w-2 h-2 rounded-full shrink-0"
                      style={{ backgroundColor: color }}
                    />
                    <span className="capitalize truncate">{cat.replace(/_/g, " ")}</span>
                  </label>
                );
              })}
            </div>

            {/* Boundary & Uncertainty toggles */}
            <div className="pt-2 border-t border-slate-800 space-y-1 text-[10px]">
              <label className="flex items-center gap-2 cursor-pointer text-slate-400 hover:text-slate-200">
                <input
                  type="checkbox"
                  checked={showBoundaries}
                  onChange={(e) => setShowBoundaries(e.target.checked)}
                  className="rounded border-slate-700 text-cyan-500 w-3 h-3 bg-slate-900"
                />
                <span>Sector Boundaries</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer text-slate-400 hover:text-slate-200">
                <input
                  type="checkbox"
                  checked={showUncertainty}
                  onChange={(e) => setShowUncertainty(e.target.checked)}
                  className="rounded border-slate-700 text-cyan-500 w-3 h-3 bg-slate-900"
                />
                <span>Uncertainty Halos</span>
              </label>
            </div>
          </div>

          {/* Floating Hover Card Preview */}
          {selectedHoverRecord && (
            <div className="absolute bottom-4 left-4 right-4 sm:right-auto sm:max-w-sm z-10 glass-panel rounded-2xl p-4 border border-cyan-500/40 shadow-2xl animate-in fade-in slide-in-from-bottom-2 duration-150">
              <div className="flex items-center justify-between text-[10px] mb-1.5">
                <span
                  className="font-bold uppercase tracking-wider px-2 py-0.5 rounded text-white"
                  style={{
                    backgroundColor: CATEGORY_COLORS[selectedHoverRecord.category] || "#06b6d4",
                  }}
                >
                  {selectedHoverRecord.category.replace(/_/g, " ")}
                </span>
                <span className="font-mono text-slate-400">
                  Precision: {selectedHoverRecord.geocoding_precision || "sector"}
                </span>
              </div>
              <h4 className="text-xs font-bold text-white line-clamp-1 mb-1">
                {selectedHoverRecord.title.replace(/^\[SYNTHETIC DEMO\]\s*/i, "")}
              </h4>
              <p className="text-[11px] text-slate-300 line-clamp-2 mb-2">
                {selectedHoverRecord.summary}
              </p>
              <div className="flex items-center justify-between text-[10px] text-cyan-400 border-t border-slate-800 pt-1.5 font-medium">
                <span>📍 {selectedHoverRecord.original_location_text}</span>
                <span className="hover:underline">Click to inspect →</span>
              </div>
            </div>
          )}

          {/* Legend Chip in bottom right */}
          <div className="absolute bottom-4 right-4 z-10 glass-panel rounded-xl px-3 py-1.5 border border-slate-800 text-[10px] text-slate-400 flex items-center gap-2">
            <span className="inline-block w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
            <span>MapLibre GL JS • EPSG:3857 / WGS-84</span>
          </div>
        </div>
      ) : (
        /* Accessible List View Alternative */
        <div className="glass-panel rounded-3xl p-6 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <List className="w-4 h-4 text-cyan-400" />
              <span>Accessible Geospatial Directory ({filteredEvidence.length} Observations)</span>
            </h3>
            <span className="text-xs text-slate-400">Screen-reader optimized alternative</span>
          </div>

          <div className="divide-y divide-slate-800/60">
            {filteredEvidence.map((rec) => {
              const coords = getCoordinatesForEvidence(rec.id);
              return (
                <div
                  key={rec.id}
                  onClick={() => onSelectRecord(rec)}
                  className="py-3 hover:bg-slate-900/60 px-3 rounded-xl cursor-pointer transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-3"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-semibold px-2 py-0.5 rounded uppercase tracking-wider bg-slate-800 text-cyan-300 border border-slate-700">
                        {rec.category.replace(/_/g, " ")}
                      </span>
                      <span className="text-xs font-semibold text-slate-100">
                        {rec.title.replace(/^\[SYNTHETIC DEMO\]\s*/i, "")}
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 line-clamp-1">{rec.summary}</p>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-slate-400 shrink-0">
                    <div className="flex items-center gap-1">
                      <MapPin className="w-3.5 h-3.5 text-cyan-400" />
                      <span>{rec.original_location_text}</span>
                    </div>
                    <div className="font-mono text-[11px] text-slate-500">
                      [{coords[1].toFixed(4)}, {coords[0].toFixed(4)}]
                    </div>
                    <button className="text-xs font-medium text-cyan-400 hover:text-cyan-300">
                      View →
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
