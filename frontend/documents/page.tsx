"use client";

import AppShell from "@/components/app-shell";
import { dictionary, type Lang } from "@/lib/i18n";
import { useEffect, useMemo, useState } from "react";

export default function DocumentsPage() {
  const [lang, setLang] = useState<Lang>("ar");

  useEffect(() => {
    const saved = localStorage.getItem("burhan-lang") as Lang | null;
    if (saved === "ar" || saved === "en") setLang(saved);
  }, []);

  const t = useMemo(() => dictionary[lang], [lang]);

  const docs = [
    { title: "نسخة العقد التجاري", type: "Contract", caseNo: "COM-2026-1001" },
    { title: "مذكرة المطالبة العمالية", type: "Legal Memo", caseNo: "LAB-2026-2001" },
  ];

  return (
    <AppShell active="documents">
      <div className="card">
        <h2 className="text-xl font-bold mb-4">{t.documents}</h2>
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>{t.documentTitle}</th>
                <th>{t.type}</th>
                <th>{t.relatedCase}</th>
              </tr>
            </thead>
            <tbody>
              {docs.map((item, index) => (
                <tr key={index}>
                  <td>{item.title}</td>
                  <td>{item.type}</td>
                  <td>{item.caseNo}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}