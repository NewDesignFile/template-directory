import { useState, useEffect, useCallback } from "react";
import "./CategoryNavItem.css";

export default function CategoryNavItem(props) {
  const { title, category, filter, setFilter } = props;
  const [isActive, setIsActive] = useState(false);
  
  useEffect(() => {
    let subscription = true;

    if (filter === category) {
      setIsActive(true);
    } else {
      setIsActive(false);
    }

    return (() => (subscription = !subscription));
  }, [filter]);

  return <button 
    onClick={() => setFilter(category)}
    className={`nav__item nu-u-text--secondary-alt nu-c-fs-normal nu-u-py-5 nu-u-px-0 nu-u-me-8 nav__item--filter ${isActive ? 'is-active' : ''}`}
    dangerouslySetInnerHTML={{__html: title}}
    >
  </button>
}