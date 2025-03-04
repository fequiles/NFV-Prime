import "./globals.css";
import { ReactNode } from "react";
import { metadata } from "./metadata";
import LayoutPage from "@/components/layout";

export { metadata };

interface IProps {
  children: ReactNode;
}

export default function RootLayout({ children }: IProps) {
  return (
    <html lang="pt-BR">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" />
        <link
          href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@500&display=swap"
          rel="stylesheet"
        />
      </head>

      <body>
        <LayoutPage>{children}</LayoutPage>
      </body>
    </html>
  );
}
