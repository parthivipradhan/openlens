"use client";

import React from "react";
import { EvidenceRecord } from "../lib/types";
import { MapPin, Calendar, ExternalLink, ShieldCheck, FileCheck, AlertTriangle } from "lucide-react";

interface EvidenceTableViewProps {
  records: EvidenceRecord[];
  onSelect: (record: EvidenceRecord) => void;
}

export function EvidenceTableView({ records, onSelect }: EvidenceTableViewProps) {
  return (
    <div className="glass-panel rounded-2xl border border-slate-800/80 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-900/80 text-slate-400 font-semibold uppercase tracking-wider text-[10px] border-b border-slate-800">
            <tr>
              <th className="py-3 px-4">Category</th>
              <th className="py-3 px-4">Title & Details</th>
              <th className="py-3 px-4">Location</th>
              <th className="py-3 px-4">Event Date</th>
              <th className="py-3 px-4">Published</th>
              <th className="py-3 px-4">Source</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-normal">
            {records.map((r) => (
              <tr
                key={r.id}
                onClick={() => onSelect(r)}
                className="hover:bg-slate-900/60 cursor-pointer transition-colors"
              >
                <td className="py-3 px-4 whitespace-nowrap">
                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded uppercase tracking-wider bg-slate-800 text-cyan-300 border border-slate-700">
                    {r.category.replace(/_/g, " ")}
                  </span>
                </td>
                <td className="py-3 px-4 max-w-sm">
                  <div className="font-semibold text-slate-100 line-clamp-1">
                    {r.title.replace(/^\[SYNTHETIC DEMO\]\s*/i, "")}
                  </div>
                  <div className="text-[11px] text-slate-400 line-clamp-1">{r.summary}</div>
                </td>
                <td className="py-3 px-4 whitespace-nowrap text-slate-300">
                  <div className="flex items-center gap-1">
                    <MapPin className="w-3 h-3 text-cyan-400 shrink-0" />
                    <span>{r.original_location_text}</span>
                  </div>
                </td>
                <td className="py-3 px-4 whitespace-nowrap font-mono text-[11px] text-slate-400">
                  {r.event_date ? new Date(r.event_date).toLocaleDateString() : "—"}
                </td>
                <td className="py-3 px-4 whitespace-nowrap font-mono text-[11px] text-slate-400">
                  {r.published_at ? new Date(r.published_at).toLocaleDateString() : "—"}
                </td>
                <td className="py-3 px-4 whitespace-nowrap text-slate-400 text-[11px]">
                  {r.source_name || r.source_id}
                </td>
                <td className="py-3 px-4 whitespace-nowrap">
                  {r.review_status === "verified" ? (
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-emerald-950/80 border border-emerald-800 text-emerald-400">
                      Verified
                    </span>
                  ) : r.review_status === "disputed" ? (
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-rose-950/80 border border-rose-800 text-rose-400">
                      Disputed
                    </span>
                  ) : (
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-800 text-slate-300">
                      Demo
                    </span>
                  )}
                </td>
                <td className="py-3 px-4 text-right whitespace-nowrap">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelect(r);
                    }}
                    className="text-cyan-400 hover:text-cyan-300 font-medium text-xs hover:underline"
                  >
                    Inspect
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
