import { useCallback, useEffect, useState } from "react";
import ShortenForm from "./components/ShortenForm.jsx";
import UrlList from "./components/UrlList.jsx";
import { createShortUrl, deleteShortUrl, listShortUrls } from "./api/urlService.js";

export default function App() {
  const [urls, setUrls] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [banner, setBanner] = useState(null); // { type: "error" | "success", message }

  const loadUrls = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await listShortUrls({ limit: 50, offset: 0 });
      setUrls(data.items);
    } catch (err) {
      setBanner({ type: "error", message: err.message || "Could not load your links." });
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUrls();
  }, [loadUrls]);

  async function handleCreate({ originalUrl, customCode }) {
    setIsSubmitting(true);
    setBanner(null);
    try {
      const created = await createShortUrl({ originalUrl, customCode });
      // Prepend rather than refetch the whole list — keeps the UI snappy
      // and avoids an extra round trip for the common case.
      setUrls((prev) => [created, ...prev]);
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDelete(shortCode) {
    try {
      await deleteShortUrl(shortCode);
      setUrls((prev) => prev.filter((u) => u.short_code !== shortCode));
    } catch (err) {
      setBanner({ type: "error", message: err.message || "Could not delete that link." });
    }
  }

  return (
    <div className="app">
      <header className="app__header">
        <div className="app__brand">
          <span className="app__brand-mark">snip</span>
          <span className="app__brand-tag">long links, short links</span>
        </div>
      </header>

      <main className="app__main">
        <section className="app__hero">
          <h1 className="app__headline">Shorten a link.</h1>
          <p className="app__subline">Paste a URL, get something you can actually paste in a text.</p>
          <ShortenForm onSubmit={handleCreate} isSubmitting={isSubmitting} />
          {banner && <p className={`app__banner app__banner--${banner.type}`}>{banner.message}</p>}
        </section>

        <section className="app__list-section">
          <div className="app__list-heading">
            <h2>Your links</h2>
            <span className="app__list-count">{urls.length}</span>
          </div>
          <UrlList urls={urls} isLoading={isLoading} onDelete={handleDelete} />
        </section>
      </main>

      <footer className="app__footer">
        <span>Built with React &amp; FastAPI</span>
      </footer>
    </div>
  );
}
