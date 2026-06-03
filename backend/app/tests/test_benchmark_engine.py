from app.services.benchmark_engine import BenchmarkEngine


def test_benchmark_simulation_supports_target_story() -> None:
    result = BenchmarkEngine().run_simulation(20000)
    assert result["queries_per_day_target"] >= 20000
    assert result["p95_latency_ms"] < 200
    assert result["rule_match_accuracy"] == 0.94
    assert result["is_synthetic"] is True
