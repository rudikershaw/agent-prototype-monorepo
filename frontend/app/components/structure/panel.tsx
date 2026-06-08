import type React from "react";

export function Panel({ children }: { children: React.ReactNode }) {
	return <div className="min-w-100 min-h-30 rounded-2xl p-6 bg-panel space-y-4">{children}</div>;
}
