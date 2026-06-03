import { CodebookMatch } from "../api/client";

export default function CodeMatchTable({ matches }: { matches: CodebookMatch[] }) {
  if (!matches.length) {
    return <div className="empty-state">No codebook matches loaded.</div>;
  }
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Code</th>
            <th>Type</th>
            <th>Description</th>
            <th>Compatibility</th>
            <th>Risk</th>
          </tr>
        </thead>
        <tbody>
          {matches.map((match) => (
            <tr key={`${match.code}-${match.compatibility}`}>
              <td>{match.code}</td>
              <td>{match.code_type}</td>
              <td>{match.description}</td>
              <td>{match.compatibility}</td>
              <td>{match.risk_weight}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
