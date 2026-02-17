"use client";

import { useEffect, useState, useRef } from "react";

interface LogEntry {
  time: string;
  tag: string;
  tagColor: string;
  message: string;
  highlight?: string;
}

const logEntries: LogEntry[] = [
  { time: "14:23:01", tag: "INFO", tagColor: "text-accent", message: "Session started \u00b7 budget:", highlight: "$5.00" },
  { time: "14:23:02", tag: "LLM", tagColor: "text-accent-bright", message: "gpt-4o \u00b7 847 tokens \u00b7 cost:", highlight: "$0.0029" },
  { time: "14:23:03", tag: "TOOL", tagColor: "text-accent-bright", message: "serp_api \u00b7 cost:", highlight: "$0.01" },
  { time: "14:23:05", tag: "LLM", tagColor: "text-accent-bright", message: "gpt-4o \u00b7 2,104 tokens \u00b7 cost:", highlight: "$0.0073" },
  { time: "14:23:06", tag: "COST", tagColor: "text-accent-bright", message: "Running total: $0.0202 \u00b7 remaining:", highlight: "$4.98" },
  { time: "14:23:08", tag: "LLM", tagColor: "text-accent-bright", message: "gpt-4o-mini \u00b7 512 tokens \u00b7 cost:", highlight: "$0.0004" },
  { time: "14:24:51", tag: "WARN", tagColor: "text-accent-bright", message: "Soft limit reached \u00b7 90% budget used \u00b7", highlight: "$4.52 spent" },
  { time: "14:25:12", tag: "INFO", tagColor: "text-accent", message: "Session ended \u00b7 total: $4.71 \u00b7 23 calls \u00b7", highlight: "14.2s" },
];

export function ActivityLog() {
  const [visibleLines, setVisibleLines] = useState(0);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          // Animate lines in one by one
          let i = 0;
          const interval = setInterval(() => {
            i++;
            setVisibleLines(i);
            if (i >= logEntries.length) clearInterval(interval);
          }, 200);
          observer.disconnect();
        }
      },
      { threshold: 0.3 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <section className="border-x border-t border-border">
      <div className="mx-auto max-w-[1200px] px-6 py-20">
        <p className="mb-3 font-mono text-[11px] font-medium uppercase tracking-widest text-accent-bright">
          Live Monitoring
        </p>
        <h2 className="mb-3 text-3xl font-bold tracking-tight sm:text-4xl">
          See exactly what your agent spends.
        </h2>
        <p className="mb-10 max-w-md text-[15px] text-muted-foreground">
          Every LLM call, tool call, and cost event is logged in real time with a structured report.
        </p>

        <div ref={ref} className="overflow-hidden border border-border">
          {/* Title bar */}
          <div className="flex items-center gap-2 border-b border-border bg-surface px-4 py-3">
            <div className="h-3 w-3 rounded-full bg-[#ff5f57]" />
            <div className="h-3 w-3 rounded-full bg-[#febc2e]" />
            <div className="h-3 w-3 rounded-full bg-[#28c840]" />
            <span className="ml-auto font-mono text-[11px] text-muted">
              agentbudget &middot; session_7f3a
            </span>
          </div>

          {/* Log body */}
          <div className="bg-code-bg p-5 font-mono text-[12.5px] leading-8">
            {logEntries.map((entry, i) => (
              <div
                key={i}
                className="flex gap-3 transition-all duration-300"
                style={{
                  opacity: i < visibleLines ? 1 : 0,
                  transform: i < visibleLines ? "translateY(0)" : "translateY(4px)",
                }}
              >
                <span className="text-muted whitespace-nowrap">{entry.time}</span>
                <span className={`font-semibold ${entry.tagColor}`} style={{ minWidth: "3.5rem" }}>
                  {entry.tag}
                </span>
                <span className="text-muted-foreground">
                  {entry.message}{" "}
                  {entry.highlight && (
                    <span className="font-medium text-foreground">{entry.highlight}</span>
                  )}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
