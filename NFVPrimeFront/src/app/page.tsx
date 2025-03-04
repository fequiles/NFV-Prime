import { Inter } from "next/font/google";
import HomeClient from "./client";

const inter = Inter({ subsets: ["latin"] });

export default function HomePage() {
  return (
    <main>
      <HomeClient />
    </main>
  );
}
