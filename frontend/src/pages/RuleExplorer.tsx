import { Search } from "lucide-react";
import { useState } from "react";
import { RuleMatch, api } from "../api/client";
import RuleMatchCard from "../components/RuleMatchCard";

export default function RuleExplorer() {
  const [query, setQuery] = useState("MRI prior authorization 70553");
  const [payer, setPayer] = useState("Apex Health Plan");
  const [matches, setMatches] = useState<RuleMatch[]>([]);

  async function run() {
    const response = await api.ragSearch({ query, payer: payer || null, top_k: 5 });
    setMatches(response.matches);
  }

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">RAG rule explorer</span>
          <h1>Payer policy retrieval</h1>
        </div>
      </header>
      <div className="toolbar two">
        <input value={query} onChange={(event) => setQuery(event.target.value)} />
        <select value={payer} onChange={(event) => setPayer(event.target.value)}>
          <option>Apex Health Plan</option>
          <option>NovaCare Advantage</option>
          <option>Pioneer Mutual</option>
          <option>Summit Senior Care</option>
        </select>
        <button onClick={run}>
          <Search size={18} />
          Search
        </button>
      </div>
      <div className="match-grid">
        {matches.map((rule) => (
          <RuleMatchCard key={rule.rule_id} rule={rule} />
        ))}
      </div>
    </section>
  );
}
