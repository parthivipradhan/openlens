"use client";

import React, { useEffect, useState } from "react";
import {
  BarChart2,
  AlertTriangle,
  Info,
  Sliders,
  Trophy,
  ArrowRight,
  Loader2,
  RefreshCw,
} from "lucide-react";
import { CHANDIGARH_SECTOR_BOUNDARIES, CATEGORY_COLORS } from "../lib/geospatial";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Dimension display labels and icons
const DIMENSIONS: Record<string, { label: string; icon: string; polarity: number }> = {
  waterlogging:    { label: "Waterlogging",     icon: "💧", polarity: -1 },
  air_quality:     { label: "Air Quality",      icon: "🌫️", polarity: -1 },
  noise:           { label: "Noise",            icon: "🔊", polarity: -1 },
  road_closure:    { label: "Road Closures",    icon: "🚧", polarity: -1 },
  public_transport:{ label: "Public Transport", icon: "🚌", polarity: 1  },
  green_spaces:    { label: "Green Spaces",     icon: "🌳", polarity: 1  },
  healthcare:      { label: "Healthcare",       icon: "🏥", polarity: 1  },
  education:       { label: "Education",        icon: "🎓", polarity: 1  },
  infrastructure:  { label: "Infrastructure",   icon: "🏗️", polarity: 1  },
};

const LOCALITY_OPTIONS = CHANDIGARH_SECTOR_BOUNDARIES.map((s) => ({
  id: s.id,
  name: s.name,
}));

interface LocalityInfo {
  id: string;
  name: string;
  locality_type?: string;
}

interface ComparisonResult {
  localities: Record<string, LocalityInfo>;
  comparison: {
    weights_applied: Record<string, number>;
    dimensions: string[];
    raw_evidence_counts: Record<string, Record<string, number>>;
    dimension_scores: Record<string, Record<string, number>>;
    composite_scores: Record<string, number>;
    ranking: string[];
    missing_data_warnings: string[];
  };
  methodology: string;
}

const DEFAULT_WEIGHTS: Record<string, number> = {
  waterlogging: 0.15,
  air_quality: 0.12,
  noise: 0.08,
  road_closure: 0.10,
  public_transport: 0.15,
  green_spaces: 0.12,
  healthcare: 0.12,
  education: 0.10,
  infrastructure: 0.06,
};

export function LocalityCompareView() {
  const [selectedIds, setSelectedIds] = useState<string[]>([
    LOCALITY_OPTIONS[0]?.id || "",
    LOCALITY_OPTIONS[1]?.id || "",
  ]);
  const [weights, setWeights] = useState<Record<string, number>>({ ...DEFAULT_WEIGHTS });
  const [result, setResult] = useState<ComparisonResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showWeights, setShowWeights] = useState(false);

  const handleSelectLocality = (index: number, id: string) => {
    setSelectedIds((prev) => {
      const next = [...prev];
      next[index] = id;
      return next;
    });
    setResult(null);
  };

  const handleWeightChange = (dim: string, value: number) => {
    setWeights((prev) => ({ ...prev, [dim]: value }));
  };

  const runComparison = async () => {
    const ids = selectedIds.filter(Boolean);
    if (ids.length < 2) {
      setError("Please select at least 2 localities to compare.");
      return;
    }
    if (new Set(ids).size !== ids.length) {
      setError("Please select distinct localities.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch(`${API_BASE}/api/v1/compare`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ locality_ids: ids, weights }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Unknown error" }));
        setError(err.detail || "Comparison failed.");
        return;
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError("Network error: Could not reach the LocalityLens API.");
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 70) return "text-emerald-400";
    if (score >= 45) return "text-amber-400";
    return "text-rose-400";
  };

  const getScoreBarColor = (score: number) => {
    if (score >= 70) return "bg-emerald-500";
    if (score >= 45) return "bg-amber-500";
    return "bg-rose-500";
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800/80 relative overflow-hidden">
        <div className="relative z-10 max-w-3xl space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-950/80 border border-emerald-800/60 text-xs font-medium text-emerald-300">
            <BarChart2 className="w-3.5 h-3.5" />
            <span>Phase 5 — Locality Comparison Engine</span>
          </div>
          <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
            Compare Chandigarh Localities
          </h1>
          <p className="text-sm text-slate-300 leading-relaxed">
            Deterministic, evidence-grounded scoring. Adjust dimension weights to reflect your priorities.
            All intermediate values are shown for full transparency — no hidden weights.
          </p>
        </div>
        <div className="absolute -right-20 -bottom-20 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
      </div>

      {/* Controls */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-800/80 space-y-5">
        {/* Locality Pickers */}
        <div>
          <h3 className="text-sm font-semibold text-slate-200 mb-3 flex items-center gap-2">
            <BarChart2 className="w-4 h-4 text-emerald-400" />
            Select Localities to Compare
          </h3>
          <div className="flex flex-wrap gap-3">
            {[0, 1].map((i) => (
              <select
                key={i}
                value={selectedIds[i] || ""}
                onChange={(e) => handleSelectLocality(i, e.target.value)}
                className="bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-emerald-500/60 transition-all min-w-[180px]"
                aria-label={`Select locality ${i + 1}`}
                id={`locality-select-${i}`}
              >
                <option value="">— Select locality {i + 1} —</option>
                {LOCALITY_OPTIONS.map((loc) => (
                  <option key={loc.id} value={loc.id}>
                    {loc.name}
                  </option>
                ))}
              </select>
            ))}
          </div>
        </div>

        {/* Weight Sliders */}
        <div>
          <button
            onClick={() => setShowWeights(!showWeights)}
            className="flex items-center gap-2 text-xs font-medium text-slate-400 hover:text-slate-200 transition-colors"
            id="toggle-weights-btn"
          >
            <Sliders className="w-3.5 h-3.5 text-emerald-400" />
            <span>{showWeights ? "Hide" : "Customize"} dimension weights</span>
          </button>

          {showWeights && (
            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(DIMENSIONS).map(([dim, meta]) => (
                <div key={dim} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-300 flex items-center gap-1">
                      <span>{meta.icon}</span>
                      <span>{meta.label}</span>
                      <span className="text-[9px] text-slate-500 ml-1">
                        {meta.polarity === -1 ? "(lower = better)" : "(higher = better)"}
                      </span>
                    </span>
                    <span className="font-mono text-emerald-400">{(weights[dim] * 100).toFixed(0)}%</span>
                  </div>
                  <input
                    type="range"
                    min={0}
                    max={0.5}
                    step={0.01}
                    value={weights[dim]}
                    onChange={(e) => handleWeightChange(dim, parseFloat(e.target.value))}
                    className="w-full h-1.5 bg-slate-800 rounded-full appearance-none cursor-pointer accent-emerald-500"
                    aria-label={`Weight for ${meta.label}`}
                    id={`weight-${dim}`}
                  />
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Run Button */}
        <div className="flex items-center gap-3">
          <button
            id="run-comparison-btn"
            onClick={runComparison}
            disabled={loading}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-sm font-semibold text-white transition-all shadow-lg shadow-emerald-500/20"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <BarChart2 className="w-4 h-4" />}
            <span>{loading ? "Analysing…" : "Run Comparison"}</span>
          </button>
          {result && (
            <button
              onClick={() => setResult(null)}
              className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-slate-200 transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Reset
            </button>
          )}
        </div>

        {error && (
          <div className="flex items-start gap-2 px-4 py-3 rounded-xl bg-rose-950/40 border border-rose-800/50 text-xs text-rose-300">
            <AlertTriangle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-5">
          {/* Missing data warnings */}
          {result.comparison.missing_data_warnings.length > 0 && (
            <div className="glass-panel rounded-2xl p-4 border border-amber-800/50 bg-amber-950/20 space-y-1.5">
              <div className="flex items-center gap-2 text-xs font-semibold text-amber-300">
                <AlertTriangle className="w-3.5 h-3.5" />
                Missing Data Warnings
              </div>
              {result.comparison.missing_data_warnings.map((w, i) => (
                <p key={i} className="text-[11px] text-amber-400/80 pl-5">• {w}</p>
              ))}
            </div>
          )}

          {/* Composite score cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {result.comparison.ranking.map((lid, rank) => {
              const loc = result.localities[lid];
              const score = result.comparison.composite_scores[lid];
              return (
                <div
                  key={lid}
                  className={`glass-panel rounded-2xl p-5 border transition-all ${
                    rank === 0
                      ? "border-emerald-500/40 bg-emerald-950/10"
                      : "border-slate-800"
                  }`}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      {rank === 0 && (
                        <div className="inline-flex items-center gap-1 text-[10px] text-emerald-300 bg-emerald-950/60 border border-emerald-800/50 px-2 py-0.5 rounded-full mb-1.5">
                          <Trophy className="w-2.5 h-2.5" />
                          Top Ranked
                        </div>
                      )}
                      <h3 className="text-base font-bold text-white">{loc?.name || lid}</h3>
                      <p className="text-xs text-slate-400">{loc?.locality_type || "sector"}</p>
                    </div>
                    <div className={`text-3xl font-black font-mono ${getScoreColor(score)}`}>
                      {score.toFixed(0)}
                    </div>
                  </div>

                  {/* Dimension bars */}
                  <div className="space-y-2">
                    {result.comparison.dimensions.map((dim) => {
                      const dimScore = result.comparison.dimension_scores[lid]?.[dim] ?? 0;
                      const meta = DIMENSIONS[dim];
                      return (
                        <div key={dim} className="flex items-center gap-2 text-[11px]">
                          <span className="w-4 shrink-0 text-center">{meta?.icon}</span>
                          <div className="flex-1 bg-slate-900 rounded-full h-1.5 overflow-hidden">
                            <div
                              className={`h-full rounded-full transition-all ${getScoreBarColor(dimScore)}`}
                              style={{ width: `${dimScore}%` }}
                            />
                          </div>
                          <span className="w-8 text-right font-mono text-slate-400">
                            {dimScore.toFixed(0)}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Methodology note */}
          <div className="flex items-start gap-2 px-4 py-3 rounded-xl bg-slate-900/60 border border-slate-800 text-[11px] text-slate-400">
            <Info className="w-3.5 h-3.5 shrink-0 mt-0.5 text-cyan-400" />
            <span>{result.methodology}</span>
          </div>
        </div>
      )}
    </div>
  );
}
