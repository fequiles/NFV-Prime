"use client";

import "./style.css";
import { useEffect } from "react";
import LoadingPage from "../loading";
import { useRouter } from "next/navigation";

interface IProps {
  url: string;
  text?: string;
}

export default function RedirectPage({ url }: IProps) {
  const router = useRouter();

  useEffect(() => {
    // Redireciona para a URL fornecida após a renderização inicial
    router.push(url);
  }, [router, url]);
  return (
    <div id="redirect">
      <LoadingPage />
    </div>
  );
}
