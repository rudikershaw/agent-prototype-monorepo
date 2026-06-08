"use client";

import { AssistantRuntimeProvider, useLocalRuntime } from "@assistant-ui/react";
import { Thread } from "~/components/assistant-ui/thread";
import { MyChatAdapter } from "~/utils/chat-model-adapter";

export const Assistant = () => {
	const runtime = useLocalRuntime(MyChatAdapter);

	return (
		<AssistantRuntimeProvider runtime={runtime}>
			<div className="h-[calc(99vh-var(--header-height))]">
				<Thread />
			</div>
		</AssistantRuntimeProvider>
	);
};
