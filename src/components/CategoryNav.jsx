import "./CategoryNav.css";
import data from "../data/tools.json";

import CategoryNavItem from "./CategoryNavItem";

export default function CategoryNav({ filter }) {
	const navItems = [{ title: "All Tools", category: "all" }, ...data.tools];

	return (
		<nav
			className="category-nav"
			tabIndex="-1"
		>
			{navItems.map((c, i) => {
				return (
					<CategoryNavItem
						key={i}
						title={c.title}
						category={c.category}
						filter={filter}
					/>
				);
			})}
		</nav>
	);
}
