"use client";

import React, { useEffect, useState, Suspense } from "react";
import { Navbar } from "../components/Navbar";
import { EvidenceFilterBar } from "../components/EvidenceFilterBar";
import { EvidenceCard } from "../components/EvidenceCard";
import { EvidenceTableView } from "../components/EvidenceTableView";
import { EvidenceDetailModal } from "../components/EvidenceDetailModal";
import { SourceRegistryView } from "../components/SourceRegistryView";
import { ManifestsView } from "../components/ManifestsView";
import { InteractiveMap } from "../components/InteractiveMap";
import { AIAssistantView } from "../components/AIAssistantView";
import { LocalityCompareView } from "../components/LocalityCompareView";
import { EvidenceRecord, Source, DatasetManifest } from "../lib/types";
import {
  fetchEvidence,
  fetchSources,
  fetchManifests,
  fetchEvidenceDetail,
  FALLBACK_EVIDENCE,
  FALLBACK_SOURCES,
  FALLBACK_MANIFESTS,
} from "../lib/api";
import { Eye, Shield, Sparkles, AlertCircle } from "lucide-react";

type Tab = "evidence" | "map" | "sources" | "manifests" | "compare" | "assistant";

export default function HomePage() {
  const [currentTab, setCurrentTab] = useState<Tab>("map");
  const [evidenceList, setEvidenceList] = useState<EvidenceRecord[]>(FALLBACK_EVIDENCE);
  const [sourcesList, setSourcesList] = useState<Source[]>(FALLBACK_SOURCES);
  const [manifestsList, setManifestsList] = useState<DatasetManifest[]>(FALLBACK_MANIFESTS);
  const [categories, setCategories] = useState<{ name: string; count: number }[]>([]);
  const [totalCount, setTotalCount] = useState(FALLBACK_EVIDENCE.length);
  const [loading, setLoading] = useState(false);

  // Filters
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedSourceId, setSelectedSourceId] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("");
  const [viewMode, setViewMode] = useState<"grid" | "table">("grid");

  // Selected Detail Modal
  const [selectedRecord, setSelectedRecord] = useState<EvidenceRecord | null>(null);

  // Load initial sources and manifests
  useEffect(() => {
    async function initMetadata() {
      const [srcs, mans] = await Promise.all([fetchSources(), fetchManifests()]);
      setSourcesList(srcs);
      setManifestsList(mans);
    }
    initMetadata();
  }, []);

  // Load evidence on filter change
  useEffect(() => {
    let active = true;
    async function loadData() {
      setLoading(true);
      try {
        const res = await fetchEvidence({
          q: searchQuery || undefined,
          category: selectedCategory || undefined,
          source_id: selectedSourceId || undefined,
          review_status: selectedStatus || undefined,
        });
        if (active) {
          setEvidenceList(res.evidence);
          setTotalCount(res.total);
          setCategories(res.categories);
        }
      } catch (err) {
        console.error("Error loading evidence:", err);
      } finally {
        if (active) setLoading(false);
      }
    }

    loadData();
    return () => {
      active = false;
    };
  }, [searchQuery, selectedCategory, selectedSourceId, selectedStatus]);

  const handleResetFilters = () => {
    setSearchQuery("");
    setSelectedCategory("");
    setSelectedSourceId("");
    setSelectedStatus("");
  };

  const handleSelectRelated = async (relatedId: string) => {
    const detail = await fetchEvidenceDetail(relatedId);
    if (detail) {
      setSelectedRecord(detail);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar
        currentTab={currentTab}
        onTabChange={(tab) => {
          setCurrentTab(tab as Tab);
          window.scrollTo({ top: 0, behavior: "smooth" });
        }}
        evidenceCount={totalCount}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* TAB 1: Evidence Explorer */}
        {currentTab === "evidence" && (
          <div className="space-y-6">
            {/* Header intro banner */}
            <div className="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800/80 relative overflow-hidden">
              <div className="relative z-10 max-w-3xl space-y-3">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-800/60 text-xs font-medium text-cyan-300">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Phase 2 — Neighbourhood Evidence Intelligence</span>
                </div>
                <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
                  Chandigarh Evidence Explorer
                </h1>
                <p className="text-sm text-slate-300 leading-relaxed">
                  Transparent neighbourhood observations, verified municipal notices, and crowdsourced incident records.
                  Every record cryptographically hashed and linked to supporting claims.
                </p>
                <div className="pt-2">
                  <button
                    onClick={() => setCurrentTab("map")}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 hover:from-cyan-400 hover:to-indigo-400 text-slate-950 text-xs font-bold transition-all shadow-lg shadow-cyan-500/20"
                  >
                    <span>🗺️ Open Interactive Map ({evidenceList.length} Geocoded Points)</span>
                    <span>→</span>
                  </button>
                </div>
              </div>
              <div className="absolute -right-20 -bottom-20 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
              <div className="absolute right-40 -top-20 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
            </div>

            {/* Filter Controls */}
            <EvidenceFilterBar
              searchQuery={searchQuery}
              onSearchChange={setSearchQuery}
              selectedCategory={selectedCategory}
              onCategoryChange={setSelectedCategory}
              selectedSourceId={selectedSourceId}
              onSourceChange={setSelectedSourceId}
              selectedStatus={selectedStatus}
              onStatusChange={setSelectedStatus}
              viewMode={viewMode}
              onViewModeChange={setViewMode}
              onReset={handleResetFilters}
              categories={categories}
              sources={sourcesList}
              totalResults={totalCount}
            />

            {/* Content Display */}
            {loading ? (
              <div className="text-center py-24 space-y-3">
                <div className="w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mx-auto" />
                <div className="text-xs text-slate-400">Loading evidence records...</div>
              </div>
            ) : evidenceList.length === 0 ? (
              <div className="glass-panel rounded-3xl p-12 text-center space-y-3 border border-slate-800">
                <AlertCircle className="w-8 h-8 text-amber-400 mx-auto" />
                <h3 className="text-base font-semibold text-white">No evidence records matched your filters</h3>
                <p className="text-xs text-slate-400 max-w-sm mx-auto">
                  Try broadening your search query or selecting a different category.
                </p>
                <button
                  onClick={handleResetFilters}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-900 bg-cyan-400 hover:bg-cyan-300 transition-all mt-2"
                >
                  Clear All Filters
                </button>
              </div>
            ) : viewMode === "grid" ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                {evidenceList.map((record) => (
                  <EvidenceCard
                    key={record.id}
                    record={record}
                    onSelect={(r) => setSelectedRecord(r)}
                  />
                ))}
              </div>
            ) : (
              <EvidenceTableView
                records={evidenceList}
                onSelect={(r) => setSelectedRecord(r)}
              />
            )}
          </div>
        )}

        {/* TAB 2: Interactive Map */}
        {currentTab === "map" && (
          <Suspense fallback={
            <div className="text-center py-24 space-y-3">
              <div className="w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mx-auto" />
              <div className="text-xs text-slate-400">Loading map…</div>
            </div>
          }>
            <InteractiveMap
              evidenceList={evidenceList}
              onSelectRecord={(r) => setSelectedRecord(r)}
              selectedCategory={selectedCategory}
              onCategoryToggle={(cat) => setSelectedCategory(cat === selectedCategory ? "" : cat)}
            />
          </Suspense>
        )}

        {/* TAB 3: AI Assistant */}
        {currentTab === "assistant" && <AIAssistantView />}

        {/* TAB 4: Locality Comparison */}
        {currentTab === "compare" && <LocalityCompareView />}

        {/* TAB 5: Sources Registry */}
        {currentTab === "sources" && (
          <SourceRegistryView
            sources={sourcesList}
            onSelectSource={(sourceId) => {
              setSelectedSourceId(sourceId);
              setCurrentTab("evidence");
            }}
          />
        )}

        {/* TAB 6: Manifests Registry */}
        {currentTab === "manifests" && (
          <ManifestsView manifests={manifestsList} />
        )}
      </main>

      {/* Evidence Detail Modal */}
      <EvidenceDetailModal
        record={selectedRecord}
        onClose={() => setSelectedRecord(null)}
        onSelectRelated={handleSelectRelated}
      />

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-8 text-xs text-slate-500 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-slate-300">LocalityLens</span>
            <span>— Open-Source Neighbourhood Intelligence</span>
          </div>
          <div className="text-slate-500 text-[11px] text-center">
            Evidence Explorer • Interactive Map • AI Assistant • Locality Comparison • TrustLayer Integrity
          </div>
        </div>
      </footer>
    </div>
  );
}
