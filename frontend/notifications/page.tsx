"use client";

import AppShell from "@/components/app-shell";
import { dictionary, type Lang } from "@/lib/i18n";
import { useEffect, useMemo, useState } from "react";

export default function NotificationsPage() {
  const [lang, setLang] = useState<Lang>("ar");

  useEffect(() => {
    const saved = localStorage.getItem("burhan-lang") as Lang | null;
    if (saved === "ar" || saved === "en") setLang(saved);
  }, []);

  const t = useMemo(() => dictionary[lang], [lang]);

  const items =
    lang === "ar"
      ? [
          "القضية COM-2026-1001 لديها جلسة خلال 48 ساعة.",
          "الوكالة NAJ-2026-0002 ستنتهي قريبًا.",
          "الفاتورة INV-2026-0002 متأخرة عن السداد.",
        ]
      : [
          "Case COM-2026-1001 has a session within 48 hours.",
          "POA NAJ-2026-0002 is expiring soon.",
          "Invoice INV-2026-0002 is overdue.",
        ];

  return (
    <AppShell active="notifications">
      <div className="card">
        <h2 className="text-xl font-bold mb-4">{t.notifications}</h2>
        <div className="space-y-3">
          {items.map((item, index) => (
            <div key={index} className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              {item}
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}