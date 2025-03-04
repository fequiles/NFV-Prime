import "./style.css";
import { metadata } from "./metadata";
import AuthLoginClient from "./client";

export { metadata };

export default function AuthLoginPage() {
  return <AuthLoginClient />;
}
