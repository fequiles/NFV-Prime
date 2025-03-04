import "./style.css";
import { ReactNode } from "react";
import { Space } from "antd";

interface IProps {
  title: string;
  children?: ReactNode;
}

export default function NoContent({ title, children }: IProps) {
  return (
    <Space direction="vertical" className="container-no-content" wrap>
      <picture>
        <img src="/images/no-content.svg" alt={"Não encontrado"} />
      </picture>

      <span>{title}</span>

      {children}
    </Space>
  );
}
