"use client";

import AppShell from "@/components/app-shell";

export default function DocumentsPage() {
  const docs = [
    { title: "نسخة العقد التجاري", type: "Contract", caseNo: "COM-2026-1001" },
    { title: "مذكرة المطالبة العمالية", type: "Legal Memo", caseNo: "LAB-2026-2001" },
  ];

  return (
    <AppShell active="documents">
      <div className="card">
        <h2 className="text-xl font-bold mb-4">المستندات</h2>
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>العنوان</th>
                <th>النوع</th>
                <th>القضية</th>
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