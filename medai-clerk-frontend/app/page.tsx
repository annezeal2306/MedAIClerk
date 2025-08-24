import Link from "next/link";

export default function Page() {
  return (
    <section className="py-16 sm:py-24">
      <div className="grid gap-12 lg:grid-cols-2 lg:items-center">
        <div className="space-y-6">
          <h1 className="text-4xl sm:text-5xl font-bold leading-tight">
            AI that drafts <span className="underline decoration-foreground/40">SOAP notes</span> in seconds.
          </h1>
          <p className="text-foreground/80 text-lg">
            Paste patient transcripts or free‑form notes, and MedAI Clerk will structure them into clean, compliant SOAP documentation and suggest ICD‑10 codes.
          </p>
          <div className="flex gap-4">
            <Link href="/soap" className="rounded-xl bg-foreground text-background px-5 py-3 font-medium">Try it now</Link>
            <Link href="/features" className="rounded-xl border px-5 py-3 font-medium">See features</Link>
          </div>
          <ul className="mt-6 grid gap-3 text-sm text-foreground/80">
            <li>• HIPAA‑friendly design patterns</li>
            <li>• Fast, minimalist UI (Next.js 15 + Tailwind 4)</li>
            <li>• Pluggable backend URL</li>
          </ul>
        </div>
        <div className="rounded-2xl border bg-card/40 p-6">
          <pre className="text-xs overflow-auto leading-relaxed">
{`Input: "45 y/o with intermittent chest pain..."
→ SOAP: Subjective, Objective, Assessment, Plan
→ ICD‑10: R07.9 (Chest pain, unspecified)`}
          </pre>
        </div>
      </div>
    </section>
  );
}
