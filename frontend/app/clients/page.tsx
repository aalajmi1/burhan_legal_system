"use client";

import AppShell from "@/components/app-shell";
import { dictionary, type Lang } from "@/lib/i18n";
import { useEffect, useMemo, useState } from "react";

export default function ClientsPage() {
  const [lang, setLang] = useState<Lang>("ar");

  useEffect(() => {
    const saved = localStorage.getItem("burhan-lang") as Lang | null;
    if (saved === "ar" || saved === "en") setLang(saved);
  }, []);

  const t = useMemo(() => dictionary[lang], [lang]);

  const clients = [
    { name: "فهد العتيبي", identity: "1023456789", city: "الرياض", cases: 2 },
    { name: "مها الشهري", identity: "2234567890", city: "جدة", cases: 1 },
    { name: "شركة عبدالله للتجارة", identity: "1019876543", city: "الدمام", cases: 1 },
  ];

  return (
    <AppShell active="clients">
      <div className="card">
        <h2 className="text-xl font-bold mb-4">{t.clients}</h2>
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>{t.client}</th>
                <th>ID</th>
                <th>City</th>
                <th>{t.cases}</th>
              </tr>
            </thead>
            <tbody>
              {clients.map((item) => (
                <tr key={item.identity}>
                  <td>{item.name}</td>
                  <td>{item.identity}</td>
                  <td>{item.city}</td>
                  <td>{item.cases}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}