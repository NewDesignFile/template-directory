import CategoryNav from "./CategoryNav";
import CardsContainer from "./CardsContainer";

export default function Dashboard({ category }) {
	return (
		<>
			<CategoryNav filter={category} />
			<CardsContainer filter={category} />
		</>
	);
}
