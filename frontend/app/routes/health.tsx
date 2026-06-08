import { HealthStatusPanel } from "~/components/health/health-status";

export function meta() {
	return [
		{ title: "Health Status" },
		{ name: "description", content: "Check the health status of the application." },
	];
}

export default function Home() {
	return <HealthStatusPanel />;
}
