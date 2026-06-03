import { BarChart3, FileCheck2, Gauge, ShieldCheck } from "lucide-react";
import { useEffect, useState } from "react";
import { Analytics, api } from "../api/client";
import MetricCard from "../components/MetricCard";
import { PageKey } from "../pagesConfig";

export default function Dashboard({ setPage }: { setPage: (page: PageKey) => void }) {
  const [summary, setSummary] = useState<Analytics | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.analytics().then(setSummary).catch((err) => setError(err.message));
  }, []);

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">Synthetic healthcare intelligence</span>
          <h1>Eligibility, claim readiness, and payer rule retrieval</h1>
        </div>
        <span className="disclaimer">Synthetic data only</span>
      </header>
      {error && <div className="error-banner">API unavailable: {error}</div>}
      <div className="metrics-grid">
        <MetricCard label="Claims" value={summary ? String(summary.claims) : "..."} tone="teal" />
        <MetricCard label="Payer rules" value={summary ? String(summary.payer_rules) : "..."} tone="coral" />
        <MetricCard label="Codebook entries" value={summary ? String(summary.codebook_entries) : "..."} tone="violet" />
        <MetricCard label="p95 cached path" value={summary ? `${summary.benchmark.p95_latency_ms}ms` : "..."} tone="amber" />
      </div>
      <div className="action-grid">
        <button onClick={() => setPage("eligibility")}>
          <ShieldCheck size={20} />
          Verify eligibility
        </button>
        <button onClick={() => setPage("claims")}>
          <FileCheck2 size={20} />
          Validate claim
        </button>
        <button onClick={() => setPage("rules")}>
          <BarChart3 size={20} />
          Explore rules
        </button>
        <button onClick={() => setPage("benchmarks")}>
          <Gauge size={20} />
          Review scaling
        </button>
      </div>
      <section className="result-panel">
        <div className="panel-head">
          <div>
            <span className="eyebrow">Benchmark story</span>
            <h2>{summary ? `${summary.benchmark.queries_per_day_target.toLocaleString()}+ synthetic queries/day target` : "Loading benchmark"}</h2>
          </div>
          <span className="pill">Mock LLM default</span>
        </div>
        <p>
          Fast validation and cached retrieval are modeled separately from slower explanation generation. All performance metrics in this MVP are
          synthetic demo metrics unless a real load test is run.
        </p>
      </section>
    </section>
  );
}
