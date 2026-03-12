"use client";

import AppShell from "@/components/app-shell";

export default function NotificationsPage() {
  const items = [
    "القضية COM-2026-1001 لديها جلسة خلال 48 ساعة.",
    "الوكالة NAJ-2026-0002 ستنتهي قريبًا.",
    "الفاتورة INV-2026-0002 متأخرة عن السداد.",
  ];

  return (
    <AppShell active="notifications">
      <div className="card">
        <h2 className="text-xl font-bold mb-4">الإشعارات</h2>
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