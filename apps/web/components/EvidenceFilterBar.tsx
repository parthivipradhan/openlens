"use client";

import React from "react";
import { Search, Filter, LayoutGrid, List, RotateCcw } from "lucide-react";
import { Source } from "../lib/types";

interface EvidenceFilterBarProps {
  searchQuery: string;
  onSearchChange: (q: string) => void;
  selectedCategory: string;
  onCategoryChange: (cat: string) => void;
  selectedSourceId: string;
  onSourceChange: (sourceId: string) => void;
  selectedStatus: string;
  onStatusChange: (status: string) => void;
  viewMode: "grid" | "table";
  onViewModeChange: (mode: "grid" | "table") => void;
  onReset: () => void;
  categories: { name: string; count: number }[];
  sources: Source[];
  totalResults: number;
}

const CATEGORY_META: Record<string, { label: string; color: string }> = {
  waterlogging: { label: "Waterlogging", color: "text-cyan-400 bg-cyan-950/60 border-cyan-800/60" },
  air_quality: { label: "Air Quality", color: "text-purple-400 bg-purple-950/60 border-purple-800/60" },
  road_closure: { label: "Road Works", color: "text-amber-400 bg-amber-950/60 border-amber-800/60" },
  public_transport: { label: "Public Transport", color: "text-emerald-400 bg-emerald-950/60 border-emerald-800/60" },
  green_spaces: { label: "Green Spaces", color: "text-green-400 bg-green-950/60 border-green-800/60" },
  healthcare: { label: "Healthcare", color: "text-rose-400 bg-rose-950/60 border-rose-800/60" },
  noise: { label: "Acoustics & Noise", color: "text-red-400 bg-red-950/60 border-red-800/60" },
  infrastructure: { label: "Infrastructure", color: "text-blue-400 bg-blue-950/60 border-blue-800/60" },
  education: { label: "Education", color: "text-indigo-400 bg-indigo-950/60 border-indigo-800/60" },
};

export function EvidenceFilterBar({
  searchQuery,
  onSearchChange,
  selectedCategory,
  onCategoryChange,
  selectedSourceId,
  onSourceChange,
  selectedStatus,
  onStatusChange,
  viewMode,
  onViewModeChange,
  onReset,
  categories,
  sources,
  totalResults,
}: EvidenceFilterBarProps) {
  const isFiltered = Boolean(searchQuery || selectedCategory || selectedSourceId || selectedStatus);

  return (
    <div className="space-y-4 mb-6">
      {/* Top Search & Controls Row */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
        {/* Search Bar */}
        <div className="relative flex-1 max-w-lg">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search evidence titles, excerpts, sector locations..."
            className="w-full pl-10 pr-4 py-2 rounded-xl text-sm glass-input transition-all"
          />
        </div>

        {/* Filters & View Toggles */}
        <div className="flex items-center gap-2 flex-wrap">
          {/* Source Dropdown */}
          <select
            value={selectedSourceId}
            onChange={(e) => onSourceChange(e.target.value)}
            className="glass-input text-xs px-3 py-2 rounded-lg text-slate-200 border border-slate-700/60"
          >
            <option value="">All Sources ({sources.length})</option>
            {sources.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>

          {/* Status Dropdown */}
          <select
            value={selectedStatus}
            onChange={(e) => onStatusChange(e.target.value)}
            className="glass-input text-xs px-3 py-2 rounded-lg text-slate-200 border border-slate-700/60"
          >
            <option value="">All Statuses</option>
            <option value="verified">Verified</option>
            <option value="disputed">Disputed</option>
            <option value="demo">Demo</option>
            <option value="pending">Pending</option>
          </select>

          {/* Reset button if active filters */}
          {isFiltered && (
            <button
              onClick={onReset}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-300 hover:text-white bg-slate-800/80 hover:bg-slate-700 border border-slate-700/60 transition-all"
              title="Reset all filters"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset</span>
            </button>
          )}

          {/* Layout Grid / Table Switcher */}
          <div className="flex items-center rounded-lg bg-slate-900 border border-slate-800 p-0.5">
            <button
              onClick={() => onViewModeChange("grid")}
              className={`p-1.5 rounded-md text-xs transition-all ${
                viewMode === "grid" ? "bg-slate-800 text-cyan-400 shadow-sm" : "text-slate-400 hover:text-slate-200"
              }`}
              title="Grid Card View"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
            <button
              onClick={() => onViewModeChange("table")}
              className={`p-1.5 rounded-md text-xs transition-all ${
                viewMode === "table" ? "bg-slate-800 text-cyan-400 shadow-sm" : "text-slate-400 hover:text-slate-200"
              }`}
              title="Table View"
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Category Pills Row */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none">
        <button
          onClick={() => onCategoryChange("")}
          className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition-all border ${
            selectedCategory === ""
              ? "bg-slate-100 text-slate-900 border-white shadow-sm font-semibold"
              : "bg-slate-900/60 text-slate-400 border-slate-800 hover:text-slate-200 hover:border-slate-700"
          }`}
        >
          <span>All Categories</span>
          <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-slate-800 text-slate-300 font-mono">
            {totalResults}
          </span>
        </button>

        {categories.map((cat) => {
          const meta = CATEGORY_META[cat.name] || {
            label: cat.name.replace(/_/g, " "),
            color: "text-slate-300 bg-slate-900 border-slate-700",
          };
          const isSelected = selectedCategory === cat.name;

          return (
            <button
              key={cat.name}
              onClick={() => onCategoryChange(isSelected ? "" : cat.name)}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition-all border ${
                isSelected
                  ? `${meta.color} font-semibold ring-2 ring-cyan-500/40 shadow-sm`
                  : "bg-slate-900/60 text-slate-400 border-slate-800 hover:text-slate-200 hover:border-slate-700"
              }`}
            >
              <span>{meta.label}</span>
              <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-slate-800/80 text-slate-300 font-mono">
                {cat.count}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
