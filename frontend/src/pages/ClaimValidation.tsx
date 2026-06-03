import { Play } from "lucide-react";
import { useEffect, useState } from "react";
import { Claim, ClaimValidation as Validation, api } from "../api/client";
import ClaimValidationPanel from "../components/ClaimValidationPanel";

export default function ClaimValidation() {
  const [claims, setClaims] = useState<Claim[]>([]);
  const [selected, setSelected] = useState("");
  const [result, setResult] = useState<Validation | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.claims().then((rows) => {
      setClaims(rows);
      setSelected(rows[0]?.claim_id ?? "");
    });
  }, []);

  async function run() {
    setLoading(true);
    try {
      setResult(await api.validateClaim(selected));
    } finally {
      setLoading(false);
    }
  }

  const claim = claims.find((item) => item.claim_id === selected);

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">Claim validation</span>
          <h1>Rule-grounded claim readiness</h1>
        </div>
      </header>
      <div className="toolbar">
        <select value={selected} onChange={(event) => setSelected(event.target.value)}>
          {claims.map((item) => (
            <option key={item.claim_id} value={item.claim_id}>
              {item.claim_id} | {item.payer} | {item.service_type}
            </option>
          ))}
        </select>
        <button onClick={run} disabled={!selected || loading}>
          <Play size={18} />
          {loading ? "Validating" : "Validate"}
        </button>
      </div>
      {claim && (
        <section className="claim-strip">
          <span>{claim.patient_ref}</span>
          <span>{claim.icd_codes.concat(claim.cpt_codes, claim.hcpcs_codes).join(", ")}</span>
          <span>{claim.procedure}</span>
        </section>
      )}
      <ClaimValidationPanel result={result} />
    </section>
  );
}
