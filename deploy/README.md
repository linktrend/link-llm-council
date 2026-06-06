# link-llm-council — production deploy (DigitalOcean)

API-only stack for Wave 3 — no Vite UI on the VPS.

## VPS path

| Host | Path | Compose project |
|------|------|-----------------|
| linkdroplet-00 | `/opt/linktrend/link-llm-council` | `link-llm-council` |

## Bootstrap

```bash
cd /opt/linktrend/link-llm-council
./ops/render-runtime-env-from-gsm.sh prod --output /opt/linktrend/runtime/link-llm-council/prod.env.runtime
docker compose -f docker-compose.deploy.yml build
docker compose -f docker-compose.deploy.yml up -d --remove-orphans
```

## Health

- `GET https://llm-council.linktrend.internal/healthz` → `{"status":"ok"}`
- `POST https://llm-council.linktrend.internal/deliberate` — governed gate deliberation (LinkSkills `cap.llm_council.deliberation`)

## LiNKaios / LinkSkills wiring

Set on the linkaios runtime env (linkskills + bot-runtime reach council on `linktrend-network`):

```text
LLM_COUNCIL_BASE_URL=http://llm-council-api:8001
LLM_COUNCIL_MODE=live
```

Do not use `localhost` from inside LiNKaios containers.
