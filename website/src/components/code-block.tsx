"use client";

import { useState } from "react";

function escapeHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function highlightCode(code: string, lang: "python" | "json" | "bash"): string {
  if (lang === "bash") {
    return code
      .split("\n")
      .map((line) => {
        const escaped = escapeHtml(line);
        // Highlight command keywords
        return escaped
          .replace(/^(pip|npm|npx)\b/, '<span style="color:#d2a8ff">$1</span>')
          .replace(/\b(install)\b/, '<span style="color:#79c0ff">$1</span>')
          .replace(/\[([^\]]+)\]/, '<span style="color:#a5d6ff">[$1]</span>');
      })
      .join("\n");
  }

  if (lang === "json") {
    return code
      .split("\n")
      .map((line) => {
        let escaped = escapeHtml(line);
        // Strings (keys and values)
        escaped = escaped.replace(/"([^"]*)"(\s*:)/g, '<span style="color:#79c0ff">"$1"</span>$2');
        escaped = escaped.replace(/:\s*"([^"]*)"/g, ': <span style="color:#a5d6ff">"$1"</span>');
        // Numbers
        escaped = escaped.replace(/:\s*(\d+\.?\d*)/g, ': <span style="color:#ffa657">$1</span>');
        // null, true, false
        escaped = escaped.replace(/\b(null|true|false)\b/g, '<span style="color:#ff7b72">$1</span>');
        // Comments
        escaped = escaped.replace(/(\/\/.*)$/, '<span style="color:#484f58">$1</span>');
        return escaped;
      })
      .join("\n");
  }

  // Python
  const keywords = [
    "import", "from", "def", "async", "await", "with", "as", "return",
    "class", "for", "in", "if", "else", "elif", "try", "except", "raise",
    "while", "True", "False", "None", "not", "and", "or", "is", "lambda",
  ];

  return code
    .split("\n")
    .map((line) => {
      // Separate comment from code
      let mainPart = escapeHtml(line);
      let commentPart = "";

      const hashIdx = line.indexOf("#");
      if (hashIdx !== -1) {
        const before = line.substring(0, hashIdx);
        const singleQ = (before.match(/'/g) || []).length;
        const doubleQ = (before.match(/"/g) || []).length;
        if (singleQ % 2 === 0 && doubleQ % 2 === 0) {
          mainPart = escapeHtml(line.substring(0, hashIdx));
          commentPart = `<span style="color:#484f58">${escapeHtml(line.substring(hashIdx))}</span>`;
        }
      }

      // Strings (double and single quoted)
      mainPart = mainPart.replace(
        /(&quot;[^&]*?&quot;|&#x27;[^&]*?&#x27;|"[^"]*?"|'[^']*?')/g,
        '<span style="color:#a5d6ff">$1</span>'
      );

      // Decorators
      mainPart = mainPart.replace(
        /(@\w+)/g,
        '<span style="color:#d2a8ff">$1</span>'
      );

      // Keywords
      for (const kw of keywords) {
        const re = new RegExp(`\\b(${kw})\\b`, "g");
        mainPart = mainPart.replace(re, '<span style="color:#ff7b72">$1</span>');
      }

      // Numbers (standalone)
      mainPart = mainPart.replace(
        /\b(\d+\.?\d*)\b/g,
        '<span style="color:#ffa657">$1</span>'
      );

      // Function calls (word followed by parenthesis)
      mainPart = mainPart.replace(
        /(\w+)\(/g,
        '<span style="color:#d2a8ff">$1</span>('
      );

      // Built-in functions
      mainPart = mainPart.replace(
        /\b(print|len|range|str|int|float|dict|list|type)\b/g,
        '<span style="color:#79c0ff">$1</span>'
      );

      return mainPart + commentPart;
    })
    .join("\n");
}

interface CodeBlockProps {
  children: string;
  lang?: "python" | "json" | "bash";
}

export function CodeBlock({ children, lang = "python" }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(children);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="group relative mb-5 overflow-hidden rounded-lg border border-border bg-code-bg">
      {/* Copy button */}
      <button
        onClick={handleCopy}
        className="absolute right-3 top-3 flex items-center gap-1.5 rounded-md border border-border bg-surface/80 px-2 py-1 text-[11px] font-medium text-muted opacity-0 backdrop-blur-sm transition-all hover:border-border-bright hover:text-muted-foreground group-hover:opacity-100"
      >
        {copied ? (
          <>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M20 6L9 17l-5-5" />
            </svg>
            Copied
          </>
        ) : (
          <>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="9" y="9" width="13" height="13" rx="2" />
              <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" />
            </svg>
            Copy
          </>
        )}
      </button>

      <pre className="overflow-x-auto p-5 font-mono text-[13px] leading-7">
        <code dangerouslySetInnerHTML={{ __html: highlightCode(children, lang) }} />
      </pre>
    </div>
  );
}
