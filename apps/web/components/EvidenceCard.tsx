"use client";

import React from "react";
import {
  Calendar,
  Clock,
  MapPin,
  FileCheck,
  AlertTriangle,
  GitCompare,
  Sparkles,
  ExternalLink,
  ShieldCheck,
  Copy,
  Check,
} from "lucide-react";
import { EvidenceRecord } from "../lib/types";

interface EvidenceCardProps {
  record: EvidenceRecord;
  onSelect: (record: EvidenceRecord) => void;
}

export function EvidenceCard({ record, onSelect }: EvidenceCardProps) {
  const [copied, setCopied] = React.useState(false);

  const copyDigest = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (record.canonical_digest) {
      navigator.clipboard.writeText(record.canonical_digest);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const getStatusBadge = () => {
    switch (record.review_status) {
      case "verified":
        return (
          <span className="flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded-full bg-emerald-950/80 border border-emerald-800/80 text-emerald-400">
            <FileCheck className="w-3 h-3" />
            Verified
          </span>
        );
      case "disputed":
        return (
          <span className="flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded-full bg-rose-950/80 border border-rose-800/80 text-rose-400">
            <AlertTriangle className="w-3 h-3" />
            Disputed
          </span>
        );
      case "demo":
      default:
        return (
          <span className="flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded-full bg-cyan-950/80 border border-cyan-800/80 text-cyan-400">
            Demo Fixture
          </span>
        );
    }
  };

  const claimsCount = record.claims?.length || 0;
  const relationsCount = record.relations?.length || 0;
  const contradictionsCount = record.relations?.filter((r) => r.relation_type === "contradicts").length || 0;

  return (
    <div
      onClick={() => onSelect(record)}
      className="glass-panel glass-panel-hover rounded-2xl p-5 cursor-pointer flex flex-col justify-between transition-all group border border-slate-800/80"
    >
      <div>
        {/* Top Badges Row */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-md uppercase tracking-wider bg-slate-800/90 text-cyan-300 border border-slate-700/80">
              {record.category.replace(/_/g, " ")}
            </span>

            {record.is_synthetic && (
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-950/60 border border-amber-800/60 text-amber-300">
                SYNTHETIC
              </span>
            )}
          </div>

          <div>{getStatusBadge()}</div>
        </div>

        {/* Title */}
        <h3 className="text-base font-semibold text-slate-100 group-hover:text-cyan-300 transition-colors line-clamp-2 mb-2 leading-snug">
          {record.title.replace(/^\[SYNTHETIC DEMO\]\s*/i, "")}
        </h3>

        {/* Summary */}
        <p className="text-xs text-slate-400 line-clamp-2 mb-4 leading-relaxed">
          {record.summary}
        </p>
      </div>

      <div className="space-y-3 pt-3 border-t border-slate-800/60">
        {/* Critical Dates & Location Row */}
        <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-400">
          {/* Location */}
          <div className="flex items-center gap-1.5 truncate">
            <MapPin className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
            <span className="truncate" title={record.original_location_text}>
              {record.original_location_text || "Chandigarh"}
            </span>
          </div>

          {/* Event Date vs Published Date explicitly labeled */}
          <div className="flex items-center gap-1.5 truncate justify-end">
            <Calendar className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
            <span className="truncate">
              {record.event_date
                ? `Event: ${new Date(record.event_date).toLocaleDateString()}`
                : record.published_at
                ? `Pub: ${new Date(record.published_at).toLocaleDateString()}`
                : "No date"}
            </span>
          </div>
        </div>

        {/* Precision & Provenance Source */}
        <div className="flex items-center justify-between text-[11px] text-slate-400">
          <div className="flex items-center gap-1 text-slate-400">
            <span className="text-slate-500">Precision:</span>
            <span className="capitalize text-slate-300 font-mono text-[10px] px-1.5 py-0.2 rounded bg-slate-900 border border-slate-800">
              {record.geocoding_precision || "sector"}
            </span>
          </div>

          <div className="truncate max-w-[140px] text-right text-slate-400 text-[11px]">
            {record.source_name || record.source_id}
          </div>
        </div>

        {/* Bottom Metadata Indicators */}
        <div className="flex items-center justify-between pt-2 border-t border-slate-800/40 text-[11px]">
          {/* Claims & Relations counts */}
          <div className="flex items-center gap-2">
            {claimsCount > 0 && (
              <span className="flex items-center gap-1 text-cyan-400 font-mono text-[10px]">
                <Sparkles className="w-3 h-3" />
                {claimsCount} {claimsCount === 1 ? "claim" : "claims"}
              </span>
            )}

            {relationsCount > 0 && (
              <span
                className={`flex items-center gap-1 font-mono text-[10px] ${
                  contradictionsCount > 0 ? "text-rose-400" : "text-emerald-400"
                }`}
              >
                <GitCompare className="w-3 h-3" />
                {relationsCount} {relationsCount === 1 ? "relation" : "relations"}
              </span>
            )}
          </div>

          {/* Canonical Digest copy chip */}
          {record.canonical_digest && (
            <button
              onClick={copyDigest}
              className="flex items-center gap-1 font-mono text-[10px] px-2 py-0.5 rounded bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-slate-800 transition-all"
              title={`SHA-256 Digest: ${record.canonical_digest}`}
            >
              <ShieldCheck className="w-3 h-3 text-emerald-400" />
              <span>{record.canonical_digest.substring(0, 8)}...</span>
              {copied ? <Check className="w-2.5 h-2.5 text-emerald-400" /> : <Copy className="w-2.5 h-2.5" />}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
