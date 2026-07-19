#!/usr/bin/env bash
# GSM runtime env render — same contract as LiNKbot-core/ops/render-runtime-env-from-gsm.sh
set -euo pipefail

usage() {
  cat <<USAGE
Usage: $0 <dev|prod> [--output <path>]
USAGE
}

[[ $# -ge 1 && $# -le 3 ]] || { usage; exit 1; }

ENVIRONMENT="$1"
shift
[[ "$ENVIRONMENT" == "dev" || "$ENVIRONMENT" == "prod" ]] || { echo "Environment must be dev or prod"; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BASE_ENV_FILE="$ROOT_DIR/deploy/${ENVIRONMENT}/.env"
[[ -f "$BASE_ENV_FILE" ]] || BASE_ENV_FILE="$ROOT_DIR/deploy/.env.example"

OUTPUT_FILE="$ROOT_DIR/deploy/${ENVIRONMENT}/.env.runtime"
if [[ $# -gt 0 ]]; then
  [[ "$1" == "--output" && $# -eq 2 ]] || { usage; exit 1; }
  OUTPUT_FILE="$2"
fi

command -v gcloud >/dev/null 2>&1 || { echo "gcloud CLI required"; exit 1; }

declare -A kv
while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
  [[ "$line" != *=* ]] && continue
  key="${line%%=*}"
  value="${line#*=}"
  key="${key//[$'\t\r\n ']/}"
  kv["$key"]="$value"
done < "$BASE_ENV_FILE"

PROJECT_ID="${GCP_PROJECT_ID:-${GOOGLE_CLOUD_PROJECT:-${kv[GCP_PROJECT_ID]:-}}}"
[[ -n "$PROJECT_ID" ]] || { echo "Set GCP_PROJECT_ID in deploy env"; exit 1; }

mkdir -p "$(dirname "$OUTPUT_FILE")"
: >"$OUTPUT_FILE"

for key in "${!kv[@]}"; do
  value="${kv[$key]}"
  if [[ "$key" == *_SECRET_NAME ]]; then
    secret_name="$value"
    target_key="${key%_SECRET_NAME}"
    resolved="$(gcloud secrets versions access latest --secret="$secret_name" --project="$PROJECT_ID" 2>/dev/null || true)"
    if [[ -n "$resolved" ]]; then
      printf '%s=%s\n' "$target_key" "$resolved" >>"$OUTPUT_FILE"
    fi
  else
    printf '%s=%s\n' "$key" "$value" >>"$OUTPUT_FILE"
  fi
done

echo "Wrote $OUTPUT_FILE"
