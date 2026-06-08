import { Welcome } from "../components/welcome/welcome";

export function meta() {
	return [
		{ title: "Owkin Technical Demonstration" },
		{ name: "description", content: "Welcome to this technical demonstration!" },
	];
}

export default function Home() {
	return <Welcome />;
}
