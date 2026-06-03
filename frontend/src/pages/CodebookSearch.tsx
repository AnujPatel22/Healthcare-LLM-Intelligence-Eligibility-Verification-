import { Search } from "lucide-react";
import { useState } from "react";
import { CodebookMatch, api } from "../api/client";
import CodeMatchTable from "../components/CodeMatchTable";

export default function CodebookSearch() {
  const [query, setQuery] = useState("MRI brain 70553");
  const [codeType, setCodeType] = useState("");
  const [matches, setMatches] = useState<CodebookMatch[]>([]);

  async function run() {
    const response = await api.codebookSearch({ query, code_type: codeType || null, top_k: 10 });
    setMatches(response.matches);
  }

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">Codebook intelligence</span>
          <h1>ICD, CPT, and HCPCS matching</h1>
        </div>
      </header>
      <div className="toolbar two">
        <input value={query} onChange={(event) => setQuery(event.target.value)} />
        <select value={codeType} onChange={(event) => setCodeType(event.target.value)}>
          <option value="">All code types</option>
          <option value="ICD">ICD</option>
          <option value="CPT">CPT</option>
          <option value="HCPCS">HCPCS</option>
        </select>
        <button onClick={run}>
          <Search size={18} />
          Search
        </button>
      </div>
      <CodeMatchTable matches={matches} />
    </section>
  );
}
