import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Burhan Legal System",
  description: "Smart legal office management frontend",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ar">
      <body>{children}</body>
    </html>
  );
}