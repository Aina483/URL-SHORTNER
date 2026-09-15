
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const body = await response.json();
      detail = Array.isArray(body.detail)
        ? body.detail.map((d) => d.msg).join(", ")
        : body.detail || detail;
    } catch {
      // Response had no JSON body; fall back to statusText.
    }
    throw new ApiError(detail, response.status);
  }

  if (response.status === 204) return null;
  return response.json();
}

export function createShortUrl({ originalUrl, customCode }) {
  return request("/urls", {
    method: "POST",
    body: JSON.stringify({
      original_url: originalUrl,
      custom_code: customCode || null,
    }),
  });
}

export function listShortUrls({ limit = 20, offset = 0 } = {}) {
  return request(`/urls?limit=${limit}&offset=${offset}`);
}

export function deleteShortUrl(shortCode) {
  return request(`/urls/${encodeURIComponent(shortCode)}`, { method: "DELETE" });
}

export { ApiError };
