"use client";

import React, { useState } from "react";
import {
  X,
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
  History,
  Send,
  HelpCircle,
  Link as LinkIcon,
} from "lucide-react";
import { EvidenceRecord } from "../lib/types";
import { submitEvidenceReview } from "../lib/api";

interface EvidenceDetailModalProps {
  record: EvidenceRecord | null;
  onClose: () => void;
  onSelectRelated?: (evidenceId: string) => void;
}

export function EvidenceDetailModal({ record, onClose, onSelectRelated }: EvidenceDetailModalProps) {
  const [activeTab, setActiveTab] = useState<"provenance" | "claims" | "relations" | "history" | "trust">("provenance");
  const [copiedDigest, setCopiedDigest] = useState(false);
  const [reviewAction, setReviewAction] = useState("verified");
  const [reviewReason, setReviewReason] = useState("");
  const [reviewerName, setReviewerName] = useState("Community Reviewer");
  const [submittingReview, setSubmittingReview] = useState(false);
  const [reviewSuccessMsg, setReviewSuccessMsg] = useState("");

  if (!record) return null;

  const handleCopyDigest = () => {
    if (record.canonical_digest) {
      navigator.clipboard.writeText(record.canonical_digest);
      setCopiedDigest(true);
      setTimeout(() => setCopiedDigest(false), 2000);
    }
  };

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewReason.trim()) return;

    setSubmittingReview(true);
    try {
      const res = await submitEvidenceReview(record.id, {
        action: reviewAction,
        reason: reviewReason,
        reviewer: reviewerName,
        new_review_status: reviewAction === "verified" ? "verified" : reviewAction === "disputed" ? "disputed" : undefined,
      });
      setReviewSuccessMsg("Review logged successfully into audit trail!");
      record.review_status = (res.current_status || record.review_status) as any;
      setTimeout(() => setReviewSuccessMsg(""), 3500);
      setReviewReason("");
    } catch (err) {
      console.error("Failed to submit review:", err);
    } finally {
      setSubmittingReview(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 animate-in fade-in duration-200">
      <div className="relative w-full max-w-4xl glass-panel rounded-3xl border border-slate-700/80 shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="p-6 border-b border-slate-800/80 flex items-start justify-between gap-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-xs font-semibold px-2.5 py-0.5 rounded-md uppercase tracking-wider bg-slate-800 text-cyan-300 border border-slate-700">
                {record.category.replace(/_/g, " ")}
              </span>

              {record.is_synthetic && (
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-950/60 border border-amber-800/60 text-amber-300">
                  SYNTHETIC DEMO
                </span>
              )}

              <span className="text-xs px-2 py-0.5 rounded-full capitalize font-medium bg-slate-900 border border-slate-700 text-slate-300">
                Status: {record.review_status}
              </span>
            </div>

            <h2 className="text-xl sm:text-2xl font-bold text-white leading-tight">
              {record.title.replace(/^\[SYNTHETIC DEMO\]\s*/i, "")}
            </h2>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-slate-800/80 px-6 bg-slate-900/40 overflow-x-auto scrollbar-none">
          <button
            onClick={() => setActiveTab("provenance")}
            className={`py-3 px-4 text-xs font-medium border-b-2 whitespace-nowrap transition-all ${
              activeTab === "provenance"
                ? "border-cyan-400 text-cyan-300"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            Provenance & Dates
          </button>
          <button
            onClick={() => setActiveTab("claims")}
            className={`py-3 px-4 text-xs font-medium border-b-2 whitespace-nowrap transition-all ${
              activeTab === "claims"
                ? "border-cyan-400 text-cyan-300"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            AI Claims ({record.claims?.length || 0})
          </button>
          <button
            onClick={() => setActiveTab("relations")}
            className={`py-3 px-4 text-xs font-medium border-b-2 whitespace-nowrap transition-all ${
              activeTab === "relations"
                ? "border-cyan-400 text-cyan-300"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            Relations ({record.relations?.length || 0})
          </button>
          <button
            onClick={() => setActiveTab("history")}
            className={`py-3 px-4 text-xs font-medium border-b-2 whitespace-nowrap transition-all ${
              activeTab === "history"
                ? "border-cyan-400 text-cyan-300"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            Audit History ({record.review_history?.length || 0})
          </button>
          <button
            onClick={() => setActiveTab("trust")}
            className={`py-3 px-4 text-xs font-medium border-b-2 whitespace-nowrap transition-all ${
              activeTab === "trust"
                ? "border-cyan-400 text-cyan-300"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            TrustLayer Digest
          </button>
        </div>

        {/* Modal Scrollable Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1 text-sm text-slate-300">
          {/* TAB 1: Provenance & Dates */}
          {activeTab === "provenance" && (
            <div className="space-y-6">
              {/* Summary */}
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Summary</h4>
                <p className="text-slate-200 leading-relaxed bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                  {record.summary || "No textual summary provided."}
                </p>
              </div>

              {/* Critical Dates Timeline (Strict separation per Rule 6) */}
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
                  Chronological Provenance Timestamps
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                  <div className="bg-slate-900/80 p-3.5 rounded-xl border border-slate-800">
                    <div className="text-[11px] text-indigo-400 flex items-center gap-1.5 font-medium mb-1">
                      <Calendar className="w-3.5 h-3.5" />
                      <span>Event Date</span>
                    </div>
                    <div className="text-xs font-mono text-slate-200">
                      {record.event_date ? new Date(record.event_date).toLocaleString() : "Not established"}
                    </div>
                    <div className="text-[10px] text-slate-500 mt-1">When physical incident occurred</div>
                  </div>

                  <div className="bg-slate-900/80 p-3.5 rounded-xl border border-slate-800">
                    <div className="text-[11px] text-cyan-400 flex items-center gap-1.5 font-medium mb-1">
                      <Clock className="w-3.5 h-3.5" />
                      <span>Published At</span>
                    </div>
                    <div className="text-xs font-mono text-slate-200">
                      {record.published_at ? new Date(record.published_at).toLocaleString() : "Unknown"}
                    </div>
                    <div className="text-[10px] text-slate-500 mt-1">Published by source system</div>
                  </div>

                  <div className="bg-slate-900/80 p-3.5 rounded-xl border border-slate-800">
                    <div className="text-[11px] text-emerald-400 flex items-center gap-1.5 font-medium mb-1">
                      <Clock className="w-3.5 h-3.5" />
                      <span>Retrieved At</span>
                    </div>
                    <div className="text-xs font-mono text-slate-200">
                      {record.retrieved_at ? new Date(record.retrieved_at).toLocaleString() : "Pending"}
                    </div>
                    <div className="text-[10px] text-slate-500 mt-1">Ingested into LocalityLens</div>
                  </div>

                  <div className="bg-slate-900/80 p-3.5 rounded-xl border border-slate-800">
                    <div className="text-[11px] text-purple-400 flex items-center gap-1.5 font-medium mb-1">
                      <Clock className="w-3.5 h-3.5" />
                      <span>Processed At</span>
                    </div>
                    <div className="text-xs font-mono text-slate-200">
                      {record.processed_at ? new Date(record.processed_at).toLocaleString() : "Pending"}
                    </div>
                    <div className="text-[10px] text-slate-500 mt-1">Normalized & canonicalised</div>
                  </div>
                </div>
              </div>

              {/* Spatial Location Details (Rule 7) */}
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
                  Geospatial Attribution
                </h4>
                <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-400">Original Location Text:</span>
                    <span className="text-xs font-semibold text-slate-200">{record.original_location_text}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-400">Geocoding Precision Tier:</span>
                    <span className="text-xs font-mono uppercase text-cyan-400 px-2 py-0.5 rounded bg-cyan-950/60 border border-cyan-800/60">
                      {record.geocoding_precision || "sector"}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-400">Spatial Geometry:</span>
                    <span className="text-xs font-mono text-slate-400">SRID:4326 (PostGIS)</span>
                  </div>
                </div>
              </div>

              {/* Source Details */}
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Source Registry</h4>
                <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-400">Source:</span>
                    <span className="text-xs font-semibold text-slate-200">{record.source_name || record.source_id}</span>
                  </div>
                  {record.source?.publisher && (
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-slate-400">Publisher:</span>
                      <span className="text-xs text-slate-300">{record.source.publisher}</span>
                    </div>
                  )}
                  {record.source?.license && (
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-slate-400">License:</span>
                      <span className="text-xs font-mono text-emerald-400">{record.source.license}</span>
                    </div>
                  )}
                  {record.source?.authority_classification && (
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-slate-400">Authority Classification:</span>
                      <span className="text-xs text-cyan-400 font-mono">{record.source.authority_classification}</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Known Limitations */}
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                  <span>Documented Limitations & Uncertainty Factors</span>
                </h4>
                <ul className="space-y-1.5">
                  {record.limitations?.map((lim, idx) => (
                    <li key={idx} className="text-xs text-amber-200/90 bg-amber-950/30 border border-amber-900/40 p-2.5 rounded-lg flex items-start gap-2">
                      <span className="text-amber-400 shrink-0">•</span>
                      <span>{lim}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* TAB 2: AI Extracted Claims */}
          {activeTab === "claims" && (
            <div className="space-y-4">
              <div className="bg-slate-900/40 border border-slate-800 p-3 rounded-xl text-xs text-slate-400 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-cyan-400 shrink-0" />
                <span>
                  Claims extracted via open-weight model with verbatim quotes and model provenance attribution.
                </span>
              </div>

              {record.claims && record.claims.length > 0 ? (
                record.claims.map((claim) => (
                  <div key={claim.id} className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-mono px-2 py-0.5 rounded bg-cyan-950/60 border border-cyan-800/60 text-cyan-300">
                        Claim {claim.id.substring(0, 8)}
                      </span>
                      <span className="text-xs px-2 py-0.5 rounded-full capitalize bg-slate-800 text-slate-300">
                        {claim.review_status}
                      </span>
                    </div>

                    <div className="text-sm font-semibold text-slate-100">
                      "{claim.claim_text}"
                    </div>

                    {claim.supporting_excerpt && (
                      <div className="bg-slate-950 p-3 rounded-xl border border-slate-800/80">
                        <span className="text-[10px] text-slate-500 uppercase tracking-wider block mb-1">
                          Supporting Excerpt
                        </span>
                        <p className="text-xs italic text-slate-300 font-serif">
                          "{claim.supporting_excerpt}"
                        </p>
                      </div>
                    )}

                    <div className="pt-2 border-t border-slate-800 flex items-center justify-between text-[11px] text-slate-400 font-mono">
                      <span>Model: {claim.extraction_model || "qwen2.5:7b-instruct"}</span>
                      <span>Revision: {claim.model_revision || "sha:9f8a2b3c"}</span>
                      <span>Schema: {claim.schema_version || "v1.2.0"}</span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-slate-500 text-xs">
                  No extracted claims attached to this evidence record.
                </div>
              )}
            </div>
          )}

          {/* TAB 3: Evidence Relations */}
          {activeTab === "relations" && (
            <div className="space-y-4">
              <div className="bg-slate-900/40 border border-slate-800 p-3 rounded-xl text-xs text-slate-400 flex items-center gap-2">
                <GitCompare className="w-4 h-4 text-cyan-400 shrink-0" />
                <span>
                  Semantic graph relations tracking corroboration, contradictions, duplicates, and superseded notices.
                </span>
              </div>

              {record.relations && record.relations.length > 0 ? (
                record.relations.map((rel, idx) => {
                  const isContradiction = rel.relation_type === "contradicts";
                  const isDuplicate = rel.relation_type === "duplicate_of";
                  const isSupersedes = rel.relation_type === "supersedes";

                  return (
                    <div
                      key={idx}
                      className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
                    >
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span
                            className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold uppercase ${
                              isContradiction
                                ? "bg-rose-950 text-rose-300 border border-rose-800"
                                : isDuplicate
                                ? "bg-amber-950 text-amber-300 border border-amber-800"
                                : isSupersedes
                                ? "bg-purple-950 text-purple-300 border border-purple-800"
                                : "bg-emerald-950 text-emerald-300 border border-emerald-800"
                            }`}
                          >
                            {rel.relation_type}
                          </span>
                          <span className="text-[10px] text-slate-500 uppercase font-mono">
                            Direction: {rel.direction}
                          </span>
                        </div>
                        <div className="text-xs font-semibold text-slate-200">
                          {rel.related_title || `Evidence ID: ${rel.related_evidence_id}`}
                        </div>
                      </div>

                      {rel.related_evidence_id && onSelectRelated && (
                        <button
                          onClick={() => onSelectRelated(rel.related_evidence_id!)}
                          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-cyan-400 bg-cyan-950/60 border border-cyan-800/60 hover:bg-cyan-900/60 transition-all shrink-0"
                        >
                          <span>Inspect Related</span>
                          <ExternalLink className="w-3 h-3" />
                        </button>
                      )}
                    </div>
                  );
                })
              ) : (
                <div className="text-center py-8 text-slate-500 text-xs">
                  No explicit relations linked to this record yet.
                </div>
              )}
            </div>
          )}

          {/* TAB 4: Audit & Review History */}
          {activeTab === "history" && (
            <div className="space-y-6">
              {/* Review Timeline */}
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5">
                  <History className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Review Events & Audit Trail</span>
                </h4>

                {record.review_history && record.review_history.length > 0 ? (
                  <div className="space-y-3">
                    {record.review_history.map((rev) => (
                      <div key={rev.id} className="bg-slate-900/60 border border-slate-800 rounded-xl p-3.5 space-y-1.5">
                        <div className="flex items-center justify-between text-xs">
                          <span className="font-semibold text-cyan-300 uppercase tracking-wide">
                            {rev.action}
                          </span>
                          <span className="text-[11px] text-slate-500 font-mono">
                            {rev.created_at ? new Date(rev.created_at).toLocaleString() : ""}
                          </span>
                        </div>
                        <p className="text-xs text-slate-300">{rev.reason}</p>
                        <div className="text-[10px] text-slate-500 font-mono">
                          Reviewer: {rev.reviewer || "anonymous"}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-slate-500 text-xs italic bg-slate-900/40 p-3 rounded-lg">
                    No community reviews recorded yet. Submit one below.
                  </div>
                )}
              </div>

              {/* Interactive Submit Review Form */}
              <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 space-y-4">
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-200">
                  Submit Review or Flag Correction
                </h4>

                {reviewSuccessMsg && (
                  <div className="p-3 rounded-lg bg-emerald-950/80 border border-emerald-800/80 text-emerald-300 text-xs flex items-center gap-2">
                    <Check className="w-4 h-4 text-emerald-400" />
                    <span>{reviewSuccessMsg}</span>
                  </div>
                )}

                <form onSubmit={handleSubmitReview} className="space-y-3">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div>
                      <label className="text-[11px] text-slate-400 block mb-1">Action Type</label>
                      <select
                        value={reviewAction}
                        onChange={(e) => setReviewAction(e.target.value)}
                        className="w-full glass-input text-xs px-3 py-2 rounded-lg"
                      >
                        <option value="verified">Verify Record</option>
                        <option value="disputed">Dispute Findings</option>
                        <option value="flagged_duplicate">Flag as Duplicate</option>
                        <option value="corrected_category">Correct Category</option>
                      </select>
                    </div>

                    <div>
                      <label className="text-[11px] text-slate-400 block mb-1">Reviewer Name</label>
                      <input
                        type="text"
                        value={reviewerName}
                        onChange={(e) => setReviewerName(e.target.value)}
                        className="w-full glass-input text-xs px-3 py-2 rounded-lg"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="text-[11px] text-slate-400 block mb-1">Audit Reason / Justification</label>
                    <textarea
                      rows={2}
                      value={reviewReason}
                      onChange={(e) => setReviewReason(e.target.value)}
                      placeholder="Provide evidence or rationale for this review action..."
                      className="w-full glass-input text-xs p-3 rounded-lg"
                      required
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={submittingReview}
                    className="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold text-slate-900 bg-cyan-400 hover:bg-cyan-300 transition-all disabled:opacity-50"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>{submittingReview ? "Submitting..." : "Submit Review Event"}</span>
                  </button>
                </form>
              </div>
            </div>
          )}

          {/* TAB 5: TrustLayer Digest */}
          {activeTab === "trust" && (
            <div className="space-y-5">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-2xl space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
                    <ShieldCheck className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-slate-100">Canonical SHA-256 Digest</div>
                    <div className="text-xs text-slate-400">Deterministic payload digest computed on ingestion</div>
                  </div>
                </div>

                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-cyan-300 break-all select-all flex items-center justify-between gap-3">
                  <span>{record.canonical_digest || "Pending generation"}</span>
                  <button
                    onClick={handleCopyDigest}
                    className="p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-all shrink-0"
                    title="Copy SHA-256 Digest"
                  >
                    {copiedDigest ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                  </button>
                </div>

                <div className="text-xs text-slate-400 leading-relaxed space-y-2">
                  <p>
                    • This digest cryptographically binds the title, normalized location text, category, and source ID.
                  </p>
                  <p>
                    • In Phase 6, digests are grouped into Merkle trees and anchored to public blockchain testnets.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
