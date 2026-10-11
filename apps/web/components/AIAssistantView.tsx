"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  Sparkles,
  Send,
  AlertTriangle,
  BookOpen,
  Info,
  Loader2,
  Mic,
  RefreshCw,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

interface Citation {
  id: string;
}

interface Message {
  role: "user" | "assistant";
  content: string;
  citations?: string[];
  limitations?: string[];
  isMock?: boolean;
  insufficientEvidence?: boolean;
  retrievedCount?: number;
  isLoading?: boolean;
  model?: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const SUGGESTED_QUESTIONS = [
  "What are the waterlogging issues in Sector 17?",
  "How is air quality in Manimajra compared to Sector 35?",
  "Which localities have the most healthcare facilities?",
  "Tell me about road conditions in Industrial Area Phase 1.",
  "What green spaces are documented in Chandigarh?",
];

export function AIAssistantView() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [expandedLimitations, setExpandedLimitations] = useState<Set<number>>(new Set());
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (question: string) => {
    if (!question.trim() || isLoading) return;

    const userMsg: Message = { role: "user", content: question };
    const loadingMsg: Message = { role: "assistant", content: "", isLoading: true };

    setMessages((prev) => [...prev, userMsg, loadingMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/v1/assistant/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Unknown error" }));
        setMessages((prev) => [
          ...prev.slice(0, -1),
          {
            role: "assistant",
            content: `Error: ${err.detail || "Request failed"}`,
            limitations: ["The AI service is temporarily unavailable."],
          },
        ]);
        return;
      }

      const data = await res.json();
      setMessages((prev) => [
        ...prev.slice(0, -1),
        {
          role: "assistant",
          content: data.answer,
          citations: data.citations || [],
          limitations: data.limitations || [],
          isMock: data.mock,
          insufficientEvidence: data.insufficient_evidence,
          retrievedCount: data.retrieved_count,
          model: data.model,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev.slice(0, -1),
        {
          role: "assistant",
          content: "Network error: Could not reach the LocalityLens API. Please check that the backend is running.",
          limitations: ["Backend API not reachable."],
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleLimitations = (index: number) => {
    setExpandedLimitations((prev) => {
      const next = new Set(prev);
      if (next.has(index)) next.delete(index);
      else next.add(index);
      return next;
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800/80 relative overflow-hidden">
        <div className="relative z-10 max-w-3xl space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-violet-950/80 border border-violet-800/60 text-xs font-medium text-violet-300">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Phase 4 — Open-Weight AI Assistant</span>
          </div>
          <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
            Neighbourhood Intelligence Assistant
          </h1>
          <p className="text-sm text-slate-300 leading-relaxed">
            Ask questions about Chandigarh localities. Every answer is grounded in verified
            evidence records — with citations, limitations, and full transparency.
          </p>
          <div className="flex flex-wrap gap-2 pt-1">
            {[
              { icon: "🔍", text: "RAG-powered retrieval" },
              { icon: "📎", text: "Evidence citations" },
              { icon: "⚠️", text: "Insufficient-evidence abstention" },
              { icon: "🛡️", text: "Prompt-injection protected" },
            ].map((b) => (
              <span
                key={b.text}
                className="inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full bg-slate-900 border border-slate-800 text-slate-400"
              >
                <span>{b.icon}</span>
                <span>{b.text}</span>
              </span>
            ))}
          </div>
        </div>
        <div className="absolute -right-20 -bottom-20 w-80 h-80 bg-violet-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute right-40 -top-20 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
      </div>

      {/* Chat Window */}
      <div className="glass-panel rounded-3xl border border-slate-800/80 overflow-hidden flex flex-col" style={{ minHeight: "520px" }}>
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4" style={{ maxHeight: "500px" }}>
          {messages.length === 0 && (
            <div className="py-8 space-y-6">
              <div className="text-center space-y-2">
                <div className="w-12 h-12 rounded-2xl bg-violet-500/10 border border-violet-500/30 flex items-center justify-center mx-auto">
                  <Sparkles className="w-6 h-6 text-violet-400" />
                </div>
                <p className="text-sm font-medium text-slate-300">Start by asking a question about Chandigarh</p>
                <p className="text-xs text-slate-500">Answers are grounded in the LocalityLens evidence database</p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {SUGGESTED_QUESTIONS.map((q) => (
                  <button
                    key={q}
                    onClick={() => sendMessage(q)}
                    className="text-left p-3 rounded-xl border border-slate-800 hover:border-violet-500/40 hover:bg-violet-500/5 text-xs text-slate-300 transition-all group"
                  >
                    <span className="text-violet-400 mr-1.5 group-hover:mr-2 transition-all">→</span>
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
              {msg.role === "assistant" && (
                <div className="w-8 h-8 rounded-xl bg-violet-500/10 border border-violet-500/30 flex items-center justify-center shrink-0 mt-0.5">
                  <Sparkles className="w-4 h-4 text-violet-400" />
                </div>
              )}

              <div className={`max-w-2xl space-y-2 ${msg.role === "user" ? "items-end" : "items-start"} flex flex-col`}>
                {/* Bubble */}
                <div
                  className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                    msg.role === "user"
                      ? "bg-violet-600/20 border border-violet-500/30 text-slate-100 rounded-tr-sm"
                      : "bg-slate-900/80 border border-slate-800 text-slate-200 rounded-tl-sm"
                  }`}
                >
                  {msg.isLoading ? (
                    <div className="flex items-center gap-2 text-slate-400">
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      <span className="text-xs">Retrieving evidence and generating answer…</span>
                    </div>
                  ) : (
                    msg.content
                  )}
                </div>

                {/* Insufficient evidence badge */}
                {msg.insufficientEvidence && (
                  <div className="flex items-start gap-2 px-3 py-2 rounded-xl bg-amber-950/40 border border-amber-800/50 text-xs text-amber-300 max-w-md">
                    <AlertTriangle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                    <span>Insufficient evidence — the database does not have enough records to answer this question. No information was fabricated.</span>
                  </div>
                )}

                {/* Mock mode badge */}
                {msg.isMock && !msg.isLoading && (
                  <div className="flex items-center gap-1.5 text-[10px] text-slate-500 px-2">
                    <Info className="w-3 h-3" />
                    <span>Mock mode (AI_MOCK_MODE=true) — configure Ollama for real AI answers</span>
                  </div>
                )}

                {/* Citations */}
                {msg.citations && msg.citations.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 px-1">
                    {msg.citations.map((cid) => (
                      <span
                        key={cid}
                        className="inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-full bg-cyan-950/60 border border-cyan-800/50 text-cyan-400 font-mono"
                      >
                        <BookOpen className="w-2.5 h-2.5" />
                        {cid}
                      </span>
                    ))}
                    {msg.retrievedCount !== undefined && (
                      <span className="text-[10px] text-slate-500 self-center ml-1">
                        from {msg.retrievedCount} retrieved records
                      </span>
                    )}
                  </div>
                )}

                {/* Limitations (collapsible) */}
                {msg.limitations && msg.limitations.length > 0 && !msg.isLoading && (
                  <div className="w-full px-1">
                    <button
                      onClick={() => toggleLimitations(i)}
                      className="flex items-center gap-1 text-[10px] text-slate-500 hover:text-slate-300 transition-colors"
                    >
                      {expandedLimitations.has(i) ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                      <span>{msg.limitations.length} limitation{msg.limitations.length > 1 ? "s" : ""}</span>
                    </button>
                    {expandedLimitations.has(i) && (
                      <ul className="mt-1 space-y-0.5 pl-3 border-l border-slate-800">
                        {msg.limitations.map((lim, j) => (
                          <li key={j} className="text-[10px] text-slate-500">
                            • {lim}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>

        {/* Input bar */}
        <div className="border-t border-slate-800 p-4 bg-slate-950/50">
          <div className="flex gap-3 items-end">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendMessage(input);
                }
              }}
              placeholder="Ask about Chandigarh localities… (Enter to send)"
              rows={2}
              className="flex-1 resize-none bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-violet-500/60 focus:ring-1 focus:ring-violet-500/30 transition-all"
              aria-label="Ask the LocalityLens AI assistant"
            />
            <button
              id="assistant-send-btn"
              onClick={() => sendMessage(input)}
              disabled={isLoading || !input.trim()}
              className="w-10 h-10 rounded-xl bg-violet-600 hover:bg-violet-500 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center transition-all shadow-lg shadow-violet-500/20 shrink-0"
              aria-label="Send message"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 text-white animate-spin" />
              ) : (
                <Send className="w-4 h-4 text-white" />
              )}
            </button>
          </div>
          <p className="text-[10px] text-slate-600 mt-2 text-center">
            Answers are grounded in evidence records only. AI will not fabricate missing data.
          </p>
        </div>
      </div>
    </div>
  );
}
