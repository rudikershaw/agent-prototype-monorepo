const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/";

/**
 * Returns the API base URL.
 * Uses the VITE_API_URL environment variable if available,
 * otherwise falls back to http://localhost:8000/.
 */
export function getApiUrl(path: string = ""): string {
	return `${API_URL}${path}`;
}
