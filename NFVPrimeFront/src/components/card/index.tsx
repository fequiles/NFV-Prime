import { ReactNode } from "react";
import "./style.css";

interface IProps {
  children: ReactNode;
  className?: string;
}

export default function Card({ children, className }: IProps) {
  return <div className={`card-container ${className}`}>{children}</div>;
}
