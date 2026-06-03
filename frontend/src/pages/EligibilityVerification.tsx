import { Play } from "lucide-react";
import { useEffect, useState } from "react";
import { EligibilityResult, api } from "../api/client";
import EligibilityCard from "../components/EligibilityCard";

export default function EligibilityVerification() {
  const [records, setRecords] = useState<Array<Record<string, string>>>([]);
  const [selected, setSelected] = useState("");
  const [result, setResult] = useState<EligibilityResult | null>(null);

  useEffect(() => {
    api.eligibilityRecords().then((rows) => {
      setRecords(rows);
      setSelected(rows[0] ? `${rows[0].patient_ref}|${rows[0].payer}|${rows[0].member_ref}|${rows[0].service_type}` : "");
    });
  }, []);

  async function run() {
    const [patient_ref, payer, member_ref, service_type] = selected.split("|");
    const response = await api.verifyEligibility({
      patient_ref,
      payer,
      member_ref,
      service_type,
      date_of_service: "2026-06-01"
    });
    setResult(response);
  }

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">Eligibility verification</span>
          <h1>Coverage and authorization check</h1>
        </div>
      </header>
      <div className="toolbar">
        <select value={selected} onChange={(event) => setSelected(event.target.value)}>
          {records.map((record) => (
            <option key={`${record.patient_ref}-${record.service_type}`} value={`${record.patient_ref}|${record.payer}|${record.member_ref}|${record.service_type}`}>
              {record.patient_ref} | {record.payer} | {record.service_type}
            </option>
          ))}
        </select>
        <button onClick={run}>
          <Play size={18} />
          Run check
        </button>
      </div>
      <EligibilityCard result={result} />
    </section>
  );
}
