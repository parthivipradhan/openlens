import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "LocalityLens — Open Neighbourhood Intelligence",
  description:
    "AI-powered neighbourhood intelligence platform for Chandigarh. Evidence-grounded answers, PostGIS geospatial queries, and TrustLayer cryptographic integrity verification.",
  keywords: ["Chandigarh", "neighbourhood intelligence", "LocalityLens", "geospatial", "evidence explorer"],
  openGraph: {
    title: "LocalityLens — Open Neighbourhood Intelligence",
    description:
      "Evidence-grounded AI assistant, interactive map, and locality comparison for Chandigarh, India.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <body className="min-h-full flex flex-col bg-[#070a12] text-slate-100">
        {/* Skip navigation link for keyboard and screen reader users */}
        <a href="#main-content" className="skip-link">
          Skip to main content
        </a>
        <div id="main-content">
          {children}
        </div>
      </body>
    </html>
  );
}

