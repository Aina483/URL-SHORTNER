import { useState } from "react";

function formatDate(isoString) {
  return new Date(isoString).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export default function UrlCard({ url, onDelete }) {
  const [copied, setCopied] = useState(false);
  const [deleting, setDeleting] = useState(false);

  async function handleCopy() {
    await navigator.clipboard.writeText(url.short_url);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  async function handleDelete() {
    setDeleting(true);
    try {
      await onDelete(url.short_code);
    } finally {
      setDeleting(false);
    }
  }

  return (
    <li className="url-card">
      <div className="url-card__main">
        <a
          className="url-card__short"
          href={url.short_url}
          target="_blank"
          rel="noopener noreferrer"
        >
          {url.short_url.replace(/^https?:\/\//, "")}
        </a>
        <p className="url-card__original" title={url.original_url}>
          {url.original_url}
        </p>
      </div>

      <div className="url-card__meta">
        <span className="url-card__clicks">
          {url.click_count} {url.click_count === 1 ? "click" : "clicks"}
        </span>
        <span className="url-card__date">{formatDate(url.created_at)}</span>
      </div>

      <div className="url-card__actions">
        <button className="url-card__button" onClick={handleCopy}>
          {copied ? "Copied" : "Copy"}
        </button>
        <button
          className="url-card__button url-card__button--danger"
          onClick={handleDelete}
          disabled={deleting}
        >
          {deleting ? "…" : "Delete"}
        </button>
      </div>
    </li>
  );
}
