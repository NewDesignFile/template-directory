import "./CategoryNav.css";
import data from "../data/tools.json";

import CategoryNavItem from "./CategoryNavItem";

export default function CategoryNav({ filter, setFilter }) {
  const navItems = [
    {title: "🔥 All", category: "all"}, 
    ...data.tools
  ];

  return <nav className="category-nav">
    {navItems.map((c, i) => {
      return <CategoryNavItem 
        key={i}
        title={c.title} 
        category={c.category} 
        filter={filter}
        setFilter={setFilter}
      />
    })}
  </nav>
}