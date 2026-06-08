import type { ReactNode } from "react";

interface KeyValueInfoProps {
	label: string;
	value: ReactNode;
}

export function KeyValueInfo({ label, value }: KeyValueInfoProps) {
	return (
		<p className="text-sm font-mono">
			{label}: <span className="truncate">{value}</span>
		</p>
	);
}
