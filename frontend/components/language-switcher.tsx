"use client";

import { useEffect, useState } from "react";
import type { Lang } from "@/lib/i18n";

type Props = {
  value: Lang;
  onChange: (lang: Lang) => void;
  labels: {
    language: string;
    arabic: string;
    english: string;
  };
};

export default function LanguageSwitcher({ value, onChange, labels }: Props) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div className="flex items-center gap-3">
      <span className="text-sm text-slate-500">{labels.language}</span>
      <select
        className="select max-w-[160px]"
        value={value}
        onChange={(e) => onChange(e.target.value as Lang)}
      >
        <option value="ar">{labels.arabic}</option>
        <option value="en">{labels.english}</option>
      </select>
    </div>
  );
}