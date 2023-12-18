import Card from "./Card";
import "./CardsContainer.css";

import data from "../data/tools.json"

export default function CardsContainer(props) {
  const { filter } = props;

  return <section>
    <ul role="list" className="link-card-grid">
      {data.tools
        .filter(item => {
          if (filter === "all" || filter === item.category) {
            return item;
          }
        })
        .flatMap(item => item.content)
        .sort((a, b) => {
          return a.title < b.title ? -1 : 1;
        })
        .map(({url, title, body, tag}, i) => {
          return <Card
            key={i}
            href={url}
            title={title}
            body={body}
            tag={tag}
          />
        })
      }
    </ul>
  </section>
}