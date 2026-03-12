"use client";

import AppShell from "@/components/app-shell";
import { dictionary, type Lang } from "@/lib/i18n";
import { useEffect, useMemo, useState } from "react";

export default function CasesPage() {
  const [lang, setLang] = useState<Lang>("ar");

  useEffect(() => {
    const saved = localStorage.getItem("burhan-lang") as Lang | null;
    if (saved === "ar" || saved === "en") setLang(saved);
  }, []);

  const t = useMemo(() => dictionary[lang], [lang]);

  const items = [
    { number: "COM-2026-1001", title: "إخلال بعقد تجاري", status: t.inProgress, priority: t.important },
    { number: "LAB-2026-2001", title: "مطالبة برواتب ومستحقات", status: t.waitingSession, priority: t.urgent },
    { number: "CIV-2026-3001", title: "مطالبة بتعويض عن أضرار عقار", status: t.waitingJudgment, priority: t.normal },
  ];

  return (
    <AppShell active="cases">
      <div className="card">
        <h2 className="text-xl font-bold mb-4">{t.cases}</h2>
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>{t.caseNumber}</th>
                <th>{t.title}</th>
                <th>{t.status}</th>
                <th>{t.priority}</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.number}>
                  <td>{item.number}</td>
                  <td>{item.title}</td>
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
      </div>
    </AppShell>
  );
}