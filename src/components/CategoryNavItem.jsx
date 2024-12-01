import { navigate } from "astro:transitions/client";
import { useState, useEffect, useRef } from "react";
import data from "../data/tools.json";
import "./CategoryNavItem.css";

export default function CategoryNavItem(props) {
  const buttonRef = useRef(null);
  const { title, category, filter } = props;
  const [isActive, setIsActive] = useState(false);

  const handleNavigation = (e) => {
    e.preventDefault();
    navigate(`/categories/${category}`, {
      history: "push",
      state: { category },
    });
  };

  const getCategoryCount = () => {
    if (category === "all") {
      return data.tools.reduce((acc, item) => acc + item.content.length, 0);
    }

    const navItemData = data.tools.filter((item) => item.category === category);
    return navItemData[0]?.content.length;
  };

  useEffect(() => {
    let subscription = true;

    if (filter === category) {
      setIsActive(true);
    } else {
      setIsActive(false);
    }

    return () => (subscription = !subscription);
  }, [filter]);

  useEffect(() => {
    let subscription = true;
    const activeButton = buttonRef.current.classList.contains("is-active");

    if (activeButton) {
      buttonRef.current.scrollIntoView({
        behavior: "instant",
        block: "nearest",
        inline: "center",
      });
    }

    return () => (subscription = !subscription);
  }, [isActive]);

  return (
    <button
      ref={buttonRef}
      onClick={handleNavigation}
      className={`nav__item nu-u-text--secondary-alt nu-c-fs-normal nu-u-py-5 nu-u-px-0 nu-u-me-8 nav__item--filter ${
        isActive ? "is-active" : ""
      }`}
      aria-label={`Navigate to ${title} category with ${getCategoryCount()} items`}
      dangerouslySetInnerHTML={{
        __html: `${title} (${getCategoryCount()})`,
      }}
    ></button>
  );
}
