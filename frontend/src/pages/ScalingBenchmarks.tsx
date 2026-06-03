import { RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";
import { Benchmark, api } from "../api/client";
import MetricCard from "../components/MetricCard";
import ScalingPanel from "../components/ScalingPanel";

export default function ScalingBenchmarks() {
  const [benchmark, setBenchmark] = useState<Benchmark | null>(null);

  useEffect(() => {
    api.benchmark().then(setBenchmark);
  }, []);

  async function run() {
    setBenchmark(await api.runBenchmark());
  }

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">Scaling benchmarks</span>
          <h1>Horizontal and vertical readiness</h1>
        </div>
        <button onClick={run}>
          <RefreshCw size={18} />
          Simulate
        </button>
      </header>
      <div className="metrics-grid">
        <MetricCard label="Target volume" value={benchmark ? `${benchmark.queries_per_day_target.toLocaleString()}+` : "..."} tone="teal" />
        <MetricCard label="p50" value={benchmark ? `${benchmark.p50_latency_ms}ms` : "..."} tone="violet" />
        <MetricCard label="p95" value={benchmark ? `${benchmark.p95_latency_ms}ms` : "..."} tone="coral" />
        <MetricCard label="Cache hits" value={benchmark ? `${Math.round(benchmark.cache_hit_rate * 100)}%` : "..."} tone="amber" />
      </div>
      <ScalingPanel benchmark={benchmark} />
    </section>
  );
}
