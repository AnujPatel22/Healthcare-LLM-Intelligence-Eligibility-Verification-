from typing import Any


class BenchmarkEngine:
    def baseline(self, row: Any | None = None) -> dict[str, Any]:
        if row:
            return {
                "queries_per_day_target": row.queries_per_day_target,
                "p50_latency_ms": row.p50_latency_ms,
                "p95_latency_ms": row.p95_latency_ms,
                "cache_hit_rate": row.cache_hit_rate,
                "rule_match_accuracy": row.rule_match_accuracy,
                "horizontal_replicas": row.horizontal_replicas,
                "cpu_profile": row.cpu_profile,
                "memory_profile": row.memory_profile,
                "is_synthetic": row.is_synthetic,
                "notes": row.notes,
            }
        return {
            "queries_per_day_target": 20000,
            "p50_latency_ms": 92,
            "p95_latency_ms": 176,
            "cache_hit_rate": 0.82,
            "rule_match_accuracy": 0.94,
            "horizontal_replicas": 3,
            "cpu_profile": "2 vCPU API containers with autoscaling target at 60 percent CPU",
            "memory_profile": "4 GB PostgreSQL baseline with room for vector index growth",
            "is_synthetic": True,
            "notes": "Synthetic local benchmark target for portfolio demo; not a production performance claim.",
        }

    def run_simulation(self, requested_queries: int = 20000) -> dict[str, Any]:
        replicas = 2 if requested_queries < 15000 else 3 if requested_queries <= 30000 else 5
        p50 = 86 + replicas * 3
        p95 = 154 + replicas * 9
        return {
            "queries_per_day_target": requested_queries,
            "p50_latency_ms": p50,
            "p95_latency_ms": p95,
            "cache_hit_rate": 0.82,
            "rule_match_accuracy": 0.94,
            "horizontal_replicas": replicas,
            "cpu_profile": f"{replicas} stateless API replicas, 2 vCPU each",
            "memory_profile": "PostgreSQL memory increased before widening vector top-k.",
            "is_synthetic": True,
            "notes": "Simulated cached validation path only; external LLM latency is excluded.",
        }
