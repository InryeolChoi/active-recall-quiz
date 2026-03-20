import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "정처기 실기 암기 도우미",
  description: "Markdown 기반 학습 자료로 학습, 시험, 채점을 돕는 웹 앱"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
