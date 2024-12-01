import "./Card.css";

export default function Card(props) {
  const { href, title, body, tag, dateAdded } = props;

  const isNew = () => {
    if (!dateAdded) return false;
    
    const addedDate = new Date(dateAdded);
    const today = new Date();
    const differenceInTime = today.getTime() - addedDate.getTime();
    const differenceInDays = differenceInTime / (1000 * 3600 * 24);
    
    return differenceInDays <= 30;
  };

  return (
    <li className="link-card">
      <a href={href}>
        <strong className="nu-c-h6 nu-u-mt-1 nu-u-mb-1">{title}</strong>
        <p className="nu-c-fs-small nu-u-mt-1 nu-u-mb-1">{body}</p>
        <p className="distribution">
          {isNew() && <span className="tag nu-u-me-2 tag-new" title="Recently added" aria-label="New item">🔥</span>}
          <span className="tag">{tag}</span>
        </p>
      </a>
    </li>
  );
}
