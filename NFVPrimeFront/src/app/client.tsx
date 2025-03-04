"use client";

import { redirect } from "next/navigation";
import { useEffect } from "react";

export default function HomeClient() {
  useEffect(() => {
    redirect(`/login`);
  }, []);

  return <></>;
}
