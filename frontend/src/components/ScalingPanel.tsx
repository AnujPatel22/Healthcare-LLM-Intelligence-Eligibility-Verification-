import { Benchmark } from "../api/client";

export default function ScalingPanel({ benchmark }: { benchmark: Benchmark | null }) {
  if (!benchmark) {
    return <div className="empty-state">Benchmark metrics are loading.</div>;
  }
  return (
    <section className="result-panel scaling-panel">
      <div className="panel-head">
        <div>
          <span className="eyebrow">Synthetic benchmark</span>
          <h2>{benchmark.queries_per_day_target.toLocaleString()} queries/day</h2>
        </div>
        <span className="pill">{benchmark.horizontal_replicas} replicas</span>
      </div>
      <div className="detail-grid">
        <span>p50 latency</span>
        <strong>{benchmark.p50_latency_ms}ms</strong>
        <span>p95 latency</span>
        <strong>{benchmark.p95_latency_ms}ms</strong>
        <span>Cache hit rate</span>
        <strong>{Math.round(benchmark.cache_hit_rate * 100)}%</strong>
        <span>Rule accuracy</span>
        <strong>{Math.round(benchmark.rule_match_accuracy * 100)}%</strong>
      </div>
      <p>{benchmark.cpu_profile}</p>
      <p>{benchmark.memory_profile}</p>
      <small>{benchmark.notes}</small>
    </section>
  );
}
