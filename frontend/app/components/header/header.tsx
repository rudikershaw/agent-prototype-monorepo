import logoDark from "./logo-dark.svg";
import logoLight from "./logo-light.svg";

export function Header() {
	return (
		<header className="h-[var(--header-height)] py-4 px-10 gap-10">
			<img src={logoLight} alt="Owkin" className="block h-full dark:hidden" />
			<img src={logoDark} alt="Owkin" className="hidden h-full dark:block" />
		</header>
	);
}
