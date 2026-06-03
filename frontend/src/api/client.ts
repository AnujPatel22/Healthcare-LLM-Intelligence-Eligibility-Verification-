const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export type Benchmark = {
  queries_per_day_target: number;
  p50_latency_ms: number;
  p95_latency_ms: number;
  cache_hit_rate: number;
  rule_match_accuracy: number;
  horizontal_replicas: number;
  cpu_profile: string;
  memory_profile: string;
  is_synthetic: boolean;
  notes: string;
};

export type Analytics = {
  patients: number;
  eligibility_records: number;
  claims: number;
  payer_rules: number;
  codebook_entries: number;
  benchmark: Benchmark;
  validation_mix: Record<string, number>;
};

export type Claim = {
  claim_id: string;
  patient_ref: string;
  payer: string;
  member_ref: string;
  service_type: string;
  icd_codes: string[];
  cpt_codes: string[];
  hcpcs_codes: string[];
  diagnosis: string;
  procedure: string;
  place_of_service: string;
  provider_type: string;
  authorization_ref: string | null;
};

export type RuleMatch = {
  rule_id: string;
  payer: string;
  title: string;
  snippet: string;
  score: number;
  requires_authorization: boolean;
};

export type CodebookMatch = {
  code: string;
  code_type: string;
  description: string;
  service_type: string;
  compatibility: string;
  risk_weight: number;
};

export type ClaimValidation = {
  claim_id: string;
  status: string;
  risk_score: number;
  risk_level: string;
  rule_match_accuracy: number;
  latency_ms: number;
  missing_requirements: string[];
  matched_rules: RuleMatch[];
  codebook_matches: CodebookMatch[];
  recommended_fixes: string[];
  explanation: string;
};

export type EligibilityResult = {
  patient_ref: string;
  payer: string;
  coverage_status: string;
  plan_type: string;
  deductible_remaining: number;
  copay: number;
  prior_authorization_required: boolean;
  confidence: number;
  recommended_next_step: string;
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
    ...init
  });
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  analytics: () => request<Analytics>("/analytics/summary"),
  claims: () => request<Claim[]>("/claims"),
  validateClaim: (claimId: string) => request<ClaimValidation>(`/claims/${claimId}/validate`, { method: "POST" }),
  eligibilityRecords: () => request<Array<Record<string, string>>>("/eligibility/records"),
  verifyEligibility: (payload: Record<string, string>) =>
    request<EligibilityResult>("/eligibility/verify", { method: "POST", body: JSON.stringify(payload) }),
  ragSearch: (payload: Record<string, string | number | null>) =>
    request<{ query: string; matches: RuleMatch[]; synthetic_disclaimer: string }>("/rag/search", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  codebookSearch: (payload: Record<string, string | number | null>) =>
    request<{ query: string; matches: CodebookMatch[] }>("/codebooks/search", { method: "POST", body: JSON.stringify(payload) }),
  benchmark: () => request<Benchmark>("/benchmarks/summary"),
  runBenchmark: () => request<Benchmark>("/benchmarks/run-simulation", { method: "POST" })
};
