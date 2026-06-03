import { EligibilityResult } from "../api/client";

export default function EligibilityCard({ result }: { result: EligibilityResult | null }) {
  if (!result) {
    return <div className="empty-state">Run an eligibility check to view coverage, copay, deductible, and authorization requirements.</div>;
  }
  return (
    <section className="result-panel">
      <div className="panel-head">
        <div>
          <span className="eyebrow">{result.patient_ref}</span>
          <h2>{result.coverage_status.toUpperCase()}</h2>
        </div>
        <span className="pill">{Math.round(result.confidence * 100)}% confidence</span>
      </div>
      <div className="detail-grid">
        <span>Payer</span>
        <strong>{result.payer}</strong>
        <span>Plan</span>
        <strong>{result.plan_type}</strong>
        <span>Deductible</span>
        <strong>${result.deductible_remaining.toFixed(2)}</strong>
        <span>Copay</span>
        <strong>${result.copay.toFixed(2)}</strong>
        <span>Prior auth</span>
        <strong>{result.prior_authorization_required ? "Required" : "Not required"}</strong>
      </div>
      <p>{result.recommended_next_step}</p>
    </section>
  );
}
