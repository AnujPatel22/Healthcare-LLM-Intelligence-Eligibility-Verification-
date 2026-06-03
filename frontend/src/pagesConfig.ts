import { Activity, BookOpen, FileCheck2, Gauge, Search, ShieldCheck } from "lucide-react";

export const pages = [
  { key: "dashboard", label: "Dashboard", icon: Activity },
  { key: "eligibility", label: "Eligibility", icon: ShieldCheck },
  { key: "claims", label: "Claims", icon: FileCheck2 },
  { key: "rules", label: "Rules", icon: Search },
  { key: "codebooks", label: "Codebooks", icon: BookOpen },
  { key: "benchmarks", label: "Scaling", icon: Gauge }
] as const;

export type PageKey = (typeof pages)[number]["key"];
