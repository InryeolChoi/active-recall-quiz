"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import type { MouseEvent } from "react";

type Props = {
  fallbackHref: string;
  label?: string;
  className?: string;
};

export function BackLink({ fallbackHref, label = "뒤로가기", className = "button secondary" }: Props) {
  const router = useRouter();

  function handleClick(event: MouseEvent<HTMLAnchorElement>) {
    event.preventDefault();

    if (typeof window !== "undefined" && document.referrer.startsWith(window.location.origin)) {
      router.back();
      return;
    }

    router.push(fallbackHref as never);
  }

  return (
    <Link className={className} href={fallbackHref as never} onClick={handleClick}>
      {label}
    </Link>
  );
}
