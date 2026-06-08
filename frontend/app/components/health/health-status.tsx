import { useQuery } from "@tanstack/react-query";
import { apiFetchJson } from "../../utils/http";
import { KeyValueInfo } from "../structure/key-value-info";
import { Label } from "../structure/label";
import { Page } from "../structure/page";
import { Panel } from "../structure/panel";

interface HealthStatus {
	status: string;
	user_agent: string | null;
	api_env: string;
}

export function HealthStatusPanel() {
	const { data, isLoading, error } = useQuery<HealthStatus>({
		queryKey: ["health-status"],
		queryFn: () => apiFetchJson<HealthStatus>(""),
	});

	return (
		<Page>
			<Panel>
				<Label>API Health Status</Label>
				<div className="text-text font-semibold">
					{isLoading ? (
						<span className="animate-pulse">Loading...</span>
					) : error ? (
						<span className="text-red-500">Error: {(error as Error).message}</span>
					) : data ? (
						<div className="space-y-2">
							<KeyValueInfo label="Status" value={<span className="uppercase">{data.status}</span>} />
							<KeyValueInfo
								label="Environment"
								value={<span className="uppercase">{data.api_env}</span>}
							/>
							<KeyValueInfo
								label="User Agent"
								value={<span className="whitespace-pre-wrap">{data.user_agent}</span>}
							/>
						</div>
					) : (
						<span>Unknown</span>
					)}
				</div>
			</Panel>
		</Page>
	);
}
