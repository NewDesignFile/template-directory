import "./Card.css";

export default function Card(props) {
  const { href, title, body, tag } = props;

  return (
    <li className="link-card">
      <a href={href}>
        <strong className="nu-c-h6 nu-u-mt-1 nu-u-mb-1">{title}</strong>
        <p className="nu-c-fs-small nu-u-mt-1 nu-u-mb-1">{body}</p>
        <p className="distribution">
          <span className="tag">{tag}</span>
        </p>
      </a>
    </li>
  );
}
