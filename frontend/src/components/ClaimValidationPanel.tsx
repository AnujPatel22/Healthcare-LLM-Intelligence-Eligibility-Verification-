import { ClaimValidation } from "../api/client";
import CodeMatchTable from "./CodeMatchTable";
import RuleMatchCard from "./RuleMatchCard";

export default function ClaimValidationPanel({ result }: { result: ClaimValidation | null }) {
  if (!result) {
    return <div className="empty-state">Select a synthetic claim and run validation to see risk, rule matches, fixes, and explanation.</div>;
  }
  return (
    <section className="result-panel">
      <div className="panel-head">
        <div>
          <span className="eyebrow">{result.claim_id}</span>
          <h2>{result.status.replace("_", " ").toUpperCase()}</h2>
        </div>
        <span className="risk-score">{result.risk_score}</span>
      </div>
      <div className="metric-row">
        <span>Risk: {result.risk_level}</span>
        <span>Latency: {result.latency_ms}ms</span>
        <span>Rule accuracy: {Math.round(result.rule_match_accuracy * 100)}%</span>
      </div>
      <h3>Missing Requirements</h3>
      <ul className="clean-list">
        {(result.missing_requirements.length ? result.missing_requirements : ["No missing requirements"]).map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
      <h3>Recommended Fixes</h3>
      <ul className="clean-list">
        {result.recommended_fixes.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
      <h3>Matched Rules</h3>
      <div className="match-grid">
        {result.matched_rules.map((rule) => (
          <RuleMatchCard key={rule.rule_id} rule={rule} />
        ))}
      </div>
      <h3>Codebook Matches</h3>
      <CodeMatchTable matches={result.codebook_matches} />
      <h3>Explanation</h3>
      <p className="explanation">{result.explanation}</p>
    </section>
  );
}
