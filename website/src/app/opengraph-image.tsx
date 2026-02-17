import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "AgentBudget - Real-time cost enforcement for AI agents";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          background: "#09090b",
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          fontFamily: "system-ui, sans-serif",
          position: "relative",
        }}
      >
        {/* Subtle grid background */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundImage:
              "linear-gradient(rgba(139, 92, 246, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(139, 92, 246, 0.05) 1px, transparent 1px)",
            backgroundSize: "40px 40px",
          }}
        />

        {/* Top border accent */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            height: "4px",
            background: "linear-gradient(90deg, #7c3aed, #8b5cf6, #a78bfa)",
          }}
        />

        {/* Logo */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            marginBottom: "24px",
          }}
        >
          <div
            style={{
              width: "48px",
              height: "48px",
              background: "#8b5cf6",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "24px",
              fontWeight: 800,
              color: "white",
            }}
          >
            AB
          </div>
          <span
            style={{
              fontSize: "36px",
              fontWeight: 700,
              color: "#fafafa",
              letterSpacing: "-0.02em",
            }}
          >
            Agent
            <span style={{ color: "#8b5cf6" }}>Budget</span>
          </span>
        </div>

        {/* Tagline */}
        <div
          style={{
            fontSize: "52px",
            fontWeight: 700,
            color: "#fafafa",
            textAlign: "center",
            lineHeight: 1.2,
            maxWidth: "900px",
            marginBottom: "20px",
            letterSpacing: "-0.03em",
          }}
        >
          The ulimit for AI agents
        </div>

        {/* Description */}
        <div
          style={{
            fontSize: "24px",
            color: "#a1a1aa",
            textAlign: "center",
            maxWidth: "700px",
            lineHeight: 1.5,
            marginBottom: "40px",
          }}
        >
          Real-time cost enforcement for AI agent sessions. One line to set a
          budget. Zero infrastructure.
        </div>

        {/* Code snippet */}
        <div
          style={{
            display: "flex",
            background: "#18181b",
            border: "1px solid #27272a",
            padding: "16px 32px",
            fontSize: "22px",
            fontFamily: "monospace",
            gap: "8px",
          }}
        >
          <span style={{ color: "#a78bfa" }}>pip install</span>
          <span style={{ color: "#fafafa" }}>agentbudget</span>
        </div>

        {/* Bottom info */}
        <div
          style={{
            position: "absolute",
            bottom: "32px",
            display: "flex",
            gap: "24px",
            fontSize: "18px",
            color: "#71717a",
          }}
        >
          <span>Open Source</span>
          <span style={{ color: "#3f3f46" }}>|</span>
          <span>Python 3.9+</span>
          <span style={{ color: "#3f3f46" }}>|</span>
          <span>agentbudget.dev</span>
        </div>
      </div>
    ),
    { ...size }
  );
}
