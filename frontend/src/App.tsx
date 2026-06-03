import { useEffect, useState } from "react";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import EligibilityVerification from "./pages/EligibilityVerification";
import ClaimValidation from "./pages/ClaimValidation";
import RuleExplorer from "./pages/RuleExplorer";
import CodebookSearch from "./pages/CodebookSearch";
import ScalingBenchmarks from "./pages/ScalingBenchmarks";
import { PageKey, pages } from "./pagesConfig";

function App() {
  const [page, setPage] = useState<PageKey>("dashboard");

  useEffect(() => {
    document.title = `Healthcare AI | ${pages.find((item) => item.key === page)?.label ?? "Dashboard"}`;
  }, [page]);

  return (
    <Layout page={page} setPage={setPage}>
      {page === "dashboard" && <Dashboard setPage={setPage} />}
      {page === "eligibility" && <EligibilityVerification />}
      {page === "claims" && <ClaimValidation />}
      {page === "rules" && <RuleExplorer />}
      {page === "codebooks" && <CodebookSearch />}
      {page === "benchmarks" && <ScalingBenchmarks />}
    </Layout>
  );
}

export default App;
