import { RuleMatch } from "../api/client";

export default function RuleMatchCard({ rule }: { rule: RuleMatch }) {
  return (
    <article className="match-card">
      <div className="panel-head compact">
        <div>
          <span className="eyebrow">{rule.rule_id}</span>
          <h3>{rule.title}</h3>
        </div>
        <span className={rule.requires_authorization ? "pill coral-pill" : "pill"}>{rule.requires_authorization ? "Auth" : "No auth"}</span>
      </div>
      <p>{rule.snippet}</p>
      <small>
        {rule.payer} | score {rule.score.toFixed(2)}
      </small>
    </article>
  );
}
