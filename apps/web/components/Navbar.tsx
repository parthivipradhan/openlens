"use client";

import React from "react";
import { Eye, Database, FileText, ShieldCheck, MapPin } from "lucide-react";

interface NavbarProps {
  currentTab: "evidence" | "map" | "sources" | "manifests" | "compare" | "assistant";
  onTabChange: (tab: "evidence" | "map" | "sources" | "manifests" | "compare" | "assistant") => void;
  evidenceCount?: number;
}

export function Navbar({ currentTab, onTabChange, evidenceCount = 30 }: NavbarProps) {
  return (
    <header className="sticky top-0 z-40 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & City */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2.5 cursor-pointer" onClick={() => onTabChange("evidence")}>
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
                <Eye className="w-5 h-5 text-white" />
              </div>
              <div>
                <span className="text-lg font-bold tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
                  LocalityLens
                </span>
                <span className="hidden sm:inline-block ml-2 text-xs font-semibold px-2 py-0.5 rounded-full bg-cyan-950/80 border border-cyan-800/60 text-cyan-400">
                  Chandigarh Lens
                </span>
              </div>
            </div>

            <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-900 border border-slate-800 text-xs text-slate-300">
              <MapPin className="w-3.5 h-3.5 text-rose-400" />
              <span>Chandigarh, India</span>
            </div>
          </div>

          {/* Navigation tabs */}
          <nav className="flex items-center space-x-1 sm:space-x-1.5 overflow-x-auto">
            <button
              onClick={() => onTabChange("map")}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                currentTab === "map"
                  ? "bg-cyan-500/15 text-cyan-300 border border-cyan-500/40 shadow-lg shadow-cyan-500/10"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}
            >
              <MapPin className="w-3.5 h-3.5 text-cyan-400" />
              <span>Interactive Map</span>
              <span className="text-[9px] px-1.5 py-0.5 rounded-full bg-cyan-950/80 text-cyan-300 border border-cyan-800/50 uppercase tracking-wider font-mono">
                Live
              </span>
            </button>

            <button
              onClick={() => onTabChange("evidence")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                currentTab === "evidence"
                  ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}
            >
              <Eye className="w-3.5 h-3.5" />
              <span>Evidence</span>
              <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-slate-800 text-slate-300 font-mono">
                {evidenceCount}
              </span>
            </button>

            <button
              onClick={() => onTabChange("compare")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                currentTab === "compare"
                  ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}
            >
              <span>⚖️ Compare</span>
            </button>

            <button
              onClick={() => onTabChange("assistant")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                currentTab === "assistant"
                  ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}
            >
              <span>🤖 AI Assistant</span>
            </button>

            <button
              onClick={() => onTabChange("sources")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                currentTab === "sources"
                  ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}
            >
              <Database className="w-3.5 h-3.5" />
              <span>Sources</span>
            </button>

            <button
              onClick={() => onTabChange("manifests")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                currentTab === "manifests"
                  ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}
            >
              <FileText className="w-3.5 h-3.5" />
              <span>Manifests</span>
            </button>
          </nav>

          {/* Integrity badge */}
          <div className="hidden lg:flex items-center gap-2 text-xs text-emerald-400 bg-emerald-950/40 border border-emerald-800/40 px-3 py-1 rounded-full">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>SHA-256 Provenance Tracked</span>
          </div>
        </div>
      </div>
    </header>
  );
}
