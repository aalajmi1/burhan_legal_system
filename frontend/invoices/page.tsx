"use client";

import AppShell from "@/components/app-shell";
import { dictionary, type Lang } from "@/lib/i18n";
import { useEffect, useMemo, useState } from "react";

export default function InvoicesPage() {
  const [lang, setLang] = useState<Lang>("ar");

  useEffect(() => {
    const saved = localStorage.getItem("burhan-lang") as Lang | null;
    if (saved === "ar" || saved === "en") setLang(saved);
  }, []);

  const t = useMemo(() => dictionary[lang], [lang]);

  const invoices = [
    { number: "INV-2026-0001", amount: "6,612.50 SAR", dueDate: "2026-03-20", status: "Issued" },
    { number: "INV-2026-0002", amount: "4,542.50 SAR", dueDate: "2026-03-07", status: "Overdue" },
  ];

  return (
    <AppShell active="invoices">
      <div className="card">
        <h2 className="text-xl font-bold mb-4">{t.invoices}</h2>
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>{t.invoiceNumber}</th>
                <th>{t.amount}</th>
                <th>{t.dueDate}</th>
                <th>{t.status}</th>
              </tr>
            </thead>
            <tbody>
              {invoices.map((item) => (
                <tr key={item.number}>
                  <td>{item.number}</td>
                  <td>{item.amount}</td>
                  <td>{item.dueDate}</td>
                  <td>{item.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}