import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";

export const metadata: Metadata = {
  title: "MedAI Clerk",
  description: "Generate SOAP notes and ICD-10 codes with AI",
  metadataBase: new URL("http://localhost:3000"),
};

function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b bg-background/70 backdrop-blur">
      <nav className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between">
        <Link href="/" className="text-xl font-semibold">MedAI Clerk</Link>
        <div className="flex items-center gap-6 text-sm">
          <Link href="/features" className="hover:underline">Features</Link>
          <Link href="/about" className="hover:underline">About</Link>
          <Link href="/contact" className="hover:underline">Contact</Link>
          <Link href="/soap" className="rounded-xl border px-3 py-1.5 hover:bg-foreground/5">Try App</Link>
        </div>
      </nav>
    </header>
  );
}

function Footer() {
  return (
    <footer className="border-t mt-16">
      <div className="mx-auto max-w-6xl px-4 py-8 text-sm text-foreground/70">
        <p>© {new Date().getFullYear()} MedAI Clerk. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-background text-foreground">
        <Navbar />
        <main className="mx-auto max-w-6xl px-4">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
