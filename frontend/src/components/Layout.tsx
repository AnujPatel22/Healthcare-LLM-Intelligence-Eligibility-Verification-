import type React from "react";
import { Cpu } from "lucide-react";
import { PageKey, pages } from "../pagesConfig";

type Props = {
  page: PageKey;
  setPage: (page: PageKey) => void;
  children: React.ReactNode;
};

export default function Layout({ page, setPage, children }: Props) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <Cpu size={24} aria-hidden="true" />
          <div>
            <strong>Healthcare AI</strong>
            <span>Eligibility service</span>
          </div>
        </div>
        <nav className="nav">
          {pages.map((item) => {
            const Icon = item.icon;
            return (
              <button key={item.key} className={page === item.key ? "active" : ""} onClick={() => setPage(item.key)} title={item.label}>
                <Icon size={18} aria-hidden="true" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </aside>
      <main className="main-panel">{children}</main>
    </div>
  );
}
