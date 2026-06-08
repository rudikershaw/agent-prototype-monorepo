import type React from "react";

export function Label({ children }: { children: React.ReactNode }) {
	return (
		<p className="text-label-text bg-label px-3 py-[2px] w-fit rounded-sm text-[12px] font-bold uppercase">
			{children}
		</p>
	);
}
