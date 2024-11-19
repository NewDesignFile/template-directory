import { useEffect, useState } from "react";
import CategoryNav from "./CategoryNav";
import CardsContainer from "./CardsContainer";

export default function Dashboard({ category }) {
  const [currentCategory, setCurrentCategory] = useState(category);

  useEffect(() => {
    setCurrentCategory(category);
  }, [category]);

  return (
    <>
      <CategoryNav filter={category} />
      <CardsContainer filter={category} />
    </>
  );
}
