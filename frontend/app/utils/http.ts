import { getApiUrl } from "~/config";

/**
 * A wrapper around fetch that automatically handles response validation
 * and JSON parsing.
 */
export async function apiFetchJson<T>(url: string, options?: RequestInit): Promise<T> {
	const response = await fetch(getApiUrl(url), options);

	if (!response.ok) {
		// Try to parse error message from JSON, otherwise use status text
		const errorData = await response.json().catch(() => ({}));
		const errorMessage = errorData.message ?? `HTTP error! status: ${response.status}`;
		throw new Error(errorMessage);
	}

	return response.json() as Promise<T>;
}
