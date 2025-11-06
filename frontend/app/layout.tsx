import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "New Jira Client",
  description: "A modern Jira client with smooth UI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
