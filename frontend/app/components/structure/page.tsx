import type React from "react";

export function Page({ children }: { children: React.ReactNode }) {
	return (
		<main className="flex justify-center px-10 max-w-6xl mx-auto">
			<div className="space-y-6 w-full px-4">{children}</div>
		</main>
	);
}
