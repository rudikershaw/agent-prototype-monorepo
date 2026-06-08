import type { ChatModelAdapter } from "@assistant-ui/react";
import { getApiUrl } from "~/config";

export const MyChatAdapter: ChatModelAdapter = {
	async *run({ messages, abortSignal }) {
		const apiChatUrl = getApiUrl("chat");
		const plainTextMessages = messages
			.map((msg) => {
				const parts = msg.content
					.map((p) => {
						if (p.type === "text") return p.text;
						if (p.type === "tool-call")
							return `[tool: ${p.toolName}(${JSON.stringify(p.args)}) => ${JSON.stringify(p.result)}]`;
						return `[${p.type}]`;
					})
					.join(" ");
				return `${msg.role.toUpperCase()}: ${parts}`;
			})
			.join("\n\n");

		const response = await fetch(apiChatUrl, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ messages: plainTextMessages }),
			signal: abortSignal,
		});

		if (!response.ok) {
			throw new Error(`Chat API error: ${response.statusText}`);
		}

		if (!response.body) {
			throw new Error("No response body received from chat endpoint.");
		}

		const reader = response.body.getReader();
		const decoder = new TextDecoder();
		let accumulatedText = "";

		try {
			while (true) {
				const { done, value } = await reader.read();
				if (done) break;

				const chunk = decoder.decode(value, { stream: true });
				if (chunk) {
					accumulatedText += chunk;
					yield { content: [{ type: "text", text: accumulatedText }] };
				}
			}
		} finally {
			reader.releaseLock();
		}
	},
};
