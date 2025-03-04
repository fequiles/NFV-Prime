import "./style.css";

interface IProps {
  error: any | Error;
}

export default function ErrorPage({ error }: IProps) {
  console.error("error", error);

  return (
    <div className="container-error">
      <picture>
        <img src="/images/error.svg" />
      </picture>

      <span>{error?.message}</span>
    </div>
  );
}
