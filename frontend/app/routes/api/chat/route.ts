import { openai } from "@ai-sdk/openai";
import { frontendTools } from "@assistant-ui/react-ai-sdk";
import { convertToModelMessages, type JSONSchema7, streamText, type UIMessage } from "ai";

export async function action({ request }: { request: Request }) {
	const {
		messages,
		system,
		tools,
	}: {
		messages: UIMessage[];
		system?: string;
		tools?: Record<string, { description?: string; parameters: JSONSchema7 }>;
	} = await request.json();

	const result = streamText({
		model: openai("gpt-5.4-nano"),
		messages: await convertToModelMessages(messages),
		tools: {
			...frontendTools(tools ?? {}),
		},
		...(system === undefined ? {} : { system }),
	});

	return result.toUIMessageStreamResponse();
}
