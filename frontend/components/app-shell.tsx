"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import LanguageSwitcher from "@/components/language-switcher";
import { dictionary, getDir, type Lang } from "@/lib/i18n";

type Props = {
  children: React.ReactNode;
  active: "dashboard" | "clients" | "cases" | "invoices" | "documents" | "notifications";
};

export default function AppShell({ children, active }: Props) {
  const [lang, setLang] = useState<Lang>("ar");

  useEffect(() => {
    const saved = localStorage.getItem("burhan-lang") as Lang | null;
    if (saved === "ar" || saved === "en") {
      setLang(saved);
      document.documentElement.lang = saved;
      document.body.classList.remove("rtl", "ltr");
      document.body.classList.add(getDir(saved));
    } else {
      document.documentElement.lang = "ar";
      document.body.classList.add("rtl");
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("burhan-lang", lang);
    document.documentElement.lang = lang;
    document.body.classList.remove("rtl", "ltr");
    document.body.classList.add(getDir(lang));
  }, [lang]);

  const t = useMemo(() => dictionary[lang], [lang]);

  const links = [
    { href: "/", key: "dashboard", label: t.dashboard },
    { href: "/clients", key: "clients", label: t.clients },
    { href: "/cases", key: "cases", label: t.cases },
    { href: "/invoices", key: "invoices", label: t.invoices },
    { href: "/documents", key: "documents", label: t.documents },
    { href: "/notifications", key: "notifications", label: t.notifications },
  ] as const;

  return (
    <div className="min-h-screen grid grid-cols-1 lg:grid-cols-[280px_1fr]">
      <aside className="bg-[var(--sidebar)] text-[var(--sidebar-foreground)] p-6">
        <div className="mb-8">
          <div className="text-2xl font-bold">{t.appName}</div>
          <div className="text-sm text-slate-300 mt-2">{t.subtitle}</div>
        </div>

        <nav className="space-y-2">
          {links.map((item) => (
            <Link
              key={item.key}
              href={item.href}
              className={`sidebar-link ${active === item.key ? "active" : ""}`}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="mt-8 card text-slate-800">
          <div className="font-bold mb-2">{t.quickActions}</div>
          <div className="space-y-2">
            <button className="button-primary w-full">{t.addClient}</button>
            <button className="button-secondary w-full">{t.addCase}</button>
            <button className="button-secondary w-full">{t.addInvoice}</button>
          </div>
        </div>
      </aside>

      <main className="p-5 md:p-8">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold">{t.welcome}</h1>
            <p className="text-slate-500 mt-2">{t.overview}</p>
          </div>

          <div className="flex gap-3 items-center">
            <input className="input max-w-[280px]" placeholder={t.searchPlaceholder} />
            <LanguageSwitcher
              value={lang}
              onChange={setLang}
              labels={{
                language: t.language,
                arabic: t.arabic,
                english: t.english,
              }}
            />
          </div>
        </div>

        <div className="mb-6 rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-900">
          {t.mockNote}
        </div>

        {children}
      </main>
    </div>
  );
}