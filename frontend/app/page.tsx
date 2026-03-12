"use client";

import AppShell from "@/components/app-shell";
import { dictionary, type Lang } from "@/lib/i18n";
import { useEffect, useMemo, useState } from "react";

export default function HomePage() {
  const [lang, setLang] = useState<Lang>("ar");

  useEffect(() => {
    const saved = localStorage.getItem("burhan-lang") as Lang | null;
    if (saved === "ar" || saved === "en") setLang(saved);
  }, []);

  const t = useMemo(() => dictionary[lang], [lang]);

  const cases = [
    { number: "COM-2026-1001", title: "إخلال بعقد تجاري", client: "فهد العتيبي", status: t.inProgress, priority: t.important },
    { number: "LAB-2026-2001", title: "مطالبة برواتب ومستحقات", client: "مها الشهري", status: t.waitingSession, priority: t.urgent },
    { number: "ENF-2026-4001", title: "تنفيذ حكم نهائي", client: "فهد العتيبي", status: t.enforcement, priority: t.important },
  ];

  const notifications = [
    "القضية COM-2026-1001 لديها جلسة خلال 48 ساعة.",
    "الفاتورة INV-2026-0002 متأخرة عن السداد.",
    "الوكالة NAJ-2026-0002 ستنتهي قريبًا.",
  ];

  return (
    <AppShell active="dashboard">
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
        <div className="stat-card">
          <div className="text-sm text-slate-500">{t.activeCases}</div>
          <div className="text-3xl font-bold mt-2">24</div>
        </div>
        <div className="stat-card">
          <div className="text-sm text-slate-500">{t.todaySessions}</div>
          <div className="text-3xl font-bold mt-2">5</div>
        </div>
        <div className="stat-card">
          <div className="text-sm text-slate-500">{t.overdueInvoices}</div>
          <div className="text-3xl font-bold mt-2">3</div>
        </div>
        <div className="stat-card">
          <div className="text-sm text-slate-500">{t.activeClients}</div>
          <div className="text-3xl font-bold mt-2">18</div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-[1.5fr_1fr] gap-6">
        <section className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold">{t.recentCases}</h2>
          </div>

          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>{t.caseNumber}</th>
                  <th>{t.title}</th>
                  <th>{t.client}</th>
                  <th>{t.status}</th>
                  <th>{t.priority}</th>
                </tr>
              </thead>
              <tbody>
                {cases.map((item) => (
                  <tr key={item.number}>
                    <td>{item.number}</td>
                    <td>{item.title}</td>
                    <td>{item.client}</td>
                    <td>{item.status}</td>
                    <td>
                      <span
                        className={`badge ${
                          item.priority === t.urgent
                            ? "badge-urgent"
                            : item.priority === t.important
                            ? "badge-important"
                            : "badge-normal"
                        }`}
                      >
                        {item.priority}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="card">
          <h2 className="text-xl font-bold mb-4">{t.latestNotifications}</h2>
          <div className="space-y-3">
            {notifications.map((note, index) => (
              <div key={index} className="rounded-xl border border-slate-200 p-4 bg-slate-50">
                {note}
              </div>
            ))}
          </div>
        </section>
      </div>
    </AppShell>
  );
}