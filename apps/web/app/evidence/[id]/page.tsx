"use client";

import React, { Suspense, useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { fetchEvidenceDetail } from "../../../lib/api";
import { EvidenceRecord } from "../../../lib/types";
import { EvidenceDetailModal } from "../../../components/EvidenceDetailModal";
import { ArrowLeft, Loader2 } from "lucide-react";

function EvidenceDetailContent() {
  const params = useParams();
  const router = useRouter();
  const id = params?.id as string;
  const [record, setRecord] = useState<EvidenceRecord | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchEvidenceDetail(id).then((rec) => {
        setRecord(rec);
        setLoading(false);
      });
    }
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400">
        <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
      </div>
    );
  }

  if (!record) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-6 text-center space-y-4">
        <h2 className="text-xl font-bold text-white">Evidence Record Not Found</h2>
        <p className="text-xs text-slate-400 max-w-sm">
          No record matching identifier "{id}" was located.
        </p>
        <button
          onClick={() => router.push("/")}
          className="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold text-slate-900 bg-cyan-400 hover:bg-cyan-300"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Return to Evidence Explorer</span>
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 p-6 flex items-center justify-center">
      <EvidenceDetailModal
        record={record}
        onClose={() => router.push("/")}
        onSelectRelated={(relId) => router.push(`/evidence/${relId}`)}
      />
    </div>
  );
}

export default function EvidenceDetailPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400">
          <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
        </div>
      }
    >
      <EvidenceDetailContent />
    </Suspense>
  );
}
