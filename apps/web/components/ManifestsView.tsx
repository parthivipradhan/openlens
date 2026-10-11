"use client";

import React from "react";
import { FileText, AlertTriangle, CheckCircle, Globe, Shield } from "lucide-react";
import { DatasetManifest } from "../lib/types";

interface ManifestsViewProps {
  manifests: DatasetManifest[];
}

export function ManifestsView({ manifests }: ManifestsViewProps) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <FileText className="w-5 h-5 text-cyan-400" />
          <span>Dataset Manifests & Transparency Registry</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Open data specifications, coverage bounding boxes, transformations, and known limitations.
        </p>
      </div>

      <div className="space-y-4">
        {manifests.map((manifest) => (
          <div
            key={manifest.id || manifest.dataset_identifier}
            className="glass-panel rounded-2xl p-6 border border-slate-800 space-y-4"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
              <div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950/80 border border-cyan-800/60 text-cyan-300">
                  {manifest.dataset_identifier}
                </span>
                <h3 className="text-base font-bold text-white mt-1">{manifest.name}</h3>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-xs font-mono px-2 py-0.5 rounded bg-emerald-950/60 border border-emerald-800/60 text-emerald-400">
                  {manifest.license || "Open"}
                </span>
                {manifest.redistribution_permitted && (
                  <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium">
                    Redistribution Allowed
                  </span>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
              <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800/80">
                <span className="text-slate-500 block text-[11px]">Publisher</span>
                <span className="text-slate-200 font-medium">{manifest.publisher || "Official"}</span>
              </div>
              <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800/80">
                <span className="text-slate-500 block text-[11px]">Geographic Coverage</span>
                <span className="text-slate-200 font-medium">{manifest.geographic_coverage || "Chandigarh UT"}</span>
              </div>
              <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800/80">
                <span className="text-slate-500 block text-[11px]">Temporal Coverage</span>
                <span className="text-slate-200 font-medium">{manifest.temporal_coverage || "2025–2026"}</span>
              </div>
            </div>

            {/* Imported fields & transformations */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <span className="text-slate-400 font-semibold block mb-1.5">Imported Schema Fields</span>
                <div className="flex flex-wrap gap-1.5">
                  {manifest.imported_fields?.map((field, idx) => (
                    <span key={idx} className="font-mono text-[10px] px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">
                      {field}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <span className="text-slate-400 font-semibold block mb-1.5">Transformations & Pipelines</span>
                <div className="flex flex-wrap gap-1.5">
                  {manifest.transformations?.map((trans, idx) => (
                    <span key={idx} className="text-[10px] px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">
                      {trans}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Known Limitations */}
            {manifest.known_limitations && manifest.known_limitations.length > 0 && (
              <div className="pt-2 border-t border-slate-800/60">
                <span className="text-xs font-semibold text-amber-300 flex items-center gap-1.5 mb-2">
                  <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                  <span>Documented Limitations</span>
                </span>
                <ul className="space-y-1">
                  {manifest.known_limitations.map((lim, idx) => (
                    <li key={idx} className="text-xs text-amber-200/80 flex items-start gap-1.5">
                      <span className="text-amber-500">•</span>
                      <span>{lim}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
