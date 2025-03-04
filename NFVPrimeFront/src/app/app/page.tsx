import "./style.css";
import { metadata } from "./metadata";

import AppClient from "./client";

export { metadata };

export default function AppPage() {
  return <AppClient />;
}
