import "./style.css";
import { Card } from "antd";
import { ReactNode } from "react";

interface IProps {
  children: ReactNode;
}

export default function AuthLayout({ children }: IProps) {
  return (
    <section id="auth" className="auth-container">
      <Card>{children}</Card>
    </section>
  );
}
