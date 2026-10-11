"use client";

import React, { useState } from "react";
import { Database, ExternalLink, ShieldCheck, Clock, CheckCircle2, Search } from "lucide-react";
import { Source } from "../lib/types";

interface SourceRegistryViewProps {
  sources: Source[];
  onSelectSource?: (sourceId: string) => void;
}

export function SourceRegistryView({ sources, onSelectSource }: SourceRegistryViewProps) {
  const [search, setSearch] = useState("");

  const filtered = sources.filter(
    (s) =>
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      (s.publisher && s.publisher.toLowerCase().includes(search.toLowerCase())) ||
      s.source_type.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* View Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Database className="w-5 h-5 text-cyan-400" />
            <span>Source Registry & Freshness Directory</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Registered multi-tier data publishers, licenses, update schedules, and authority tiers.
          </p>
        </div>

        <div className="relative max-w-xs">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search sources..."
            className="w-full pl-9 pr-3 py-1.5 rounded-lg text-xs glass-input"
          />
        </div>
      </div>

      {/* Sources Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((source) => (
          <div
            key={source.id}
            className="glass-panel glass-panel-hover rounded-2xl p-5 border border-slate-800/80 space-y-4 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between gap-2">
                <span className="text-[10px] font-mono px-2 py-0.5 rounded uppercase font-semibold bg-cyan-950/80 border border-cyan-800/60 text-cyan-300">
                  {source.source_type}
                </span>

                <div className="flex items-center gap-1.5 text-xs text-emerald-400">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span className="capitalize">{source.status}</span>
                </div>
              </div>

              <div>
                <h3 className="text-base font-semibold text-white">{source.name}</h3>
                {source.publisher && (
                  <div className="text-xs text-slate-400 mt-0.5">Publisher: {source.publisher}</div>
                )}
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px] bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                <div>
                  <span className="text-slate-500 block">Authority Tier</span>
                  <span className="text-slate-200 font-mono text-[10px]">{source.authority_classification || "standard"}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Cadence</span>
                  <span className="text-slate-200 font-mono text-[10px] capitalize">{source.update_cadence || "daily"}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">License</span>
                  <span className="text-emerald-400 font-mono text-[10px]">{source.license || "Open"}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Evidence Records</span>
                  <span className="text-cyan-400 font-mono text-[10px]">{source.evidence_count || 0} loaded</span>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between pt-3 border-t border-slate-800/60 text-xs">
              <a
                href={source.source_url}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-1 text-slate-400 hover:text-cyan-300 transition-colors"
              >
                <span>Visit Source</span>
                <ExternalLink className="w-3 h-3" />
              </a>

              {onSelectSource && (
                <button
                  onClick={() => onSelectSource(source.id)}
                  className="px-3 py-1 rounded-lg text-xs font-medium text-cyan-400 bg-cyan-950/60 border border-cyan-800/60 hover:bg-cyan-900/60 transition-all"
                >
                  Filter Evidence
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
