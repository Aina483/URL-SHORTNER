import UrlCard from "./URLCard.jsx";

export default function UrlList({ urls, isLoading, onDelete }) {
  if (isLoading) {
    return <p className="url-list__status">Loading your links…</p>;
  }

  if (urls.length === 0) {
    return (
      <div className="url-list__empty">
        <p>No links yet.</p>
        <p className="url-list__empty-sub">Paste a URL above to create your first short link.</p>
      </div>
    );
  }

  return (
    <ul className="url-list">
      {urls.map((url) => (
        <UrlCard key={url.short_code} url={url} onDelete={onDelete} />
      ))}
    </ul>
  );
}
