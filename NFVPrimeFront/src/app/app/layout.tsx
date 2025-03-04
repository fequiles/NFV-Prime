"use client";

import { AuthService } from "@/service/auth";
import "./style.css";
import { ReactNode, useEffect } from "react";
import { redirect } from "next/navigation";

interface IProps {
  children: ReactNode;
}

export default function AppLayout({ children }: IProps) {
  useEffect(() => {
    if (!AuthService.Username) {
      redirect("/login");
    }
  }, []);

  return <section id="app">{children}</section>;
}
