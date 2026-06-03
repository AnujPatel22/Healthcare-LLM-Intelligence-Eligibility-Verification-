#!/usr/bin/env bash
set -euo pipefail

curl -s http://localhost:8000/health
curl -s http://localhost:8000/analytics/summary
curl -s -X POST http://localhost:8000/eligibility/verify \
  -H "Content-Type: application/json" \
  -d '{"patient_ref":"SYN-PAT-1001","payer":"Apex Health Plan","member_ref":"SYN-MEM-9001","service_type":"MRI Imaging","date_of_service":"2026-06-01"}'
curl -s -X POST http://localhost:8000/claims/CLM-7001/validate
curl -s -X POST http://localhost:8000/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query":"MRI prior authorization 70553","payer":"Apex Health Plan","top_k":5}'
