# Ekko Codebase - Comprehensive Analysis & Modernization Plan
**Date:** May 4, 2026  
**Scope:** Full backend/frontend analysis, Azure STT migration, production-ready cleanup

---

## Executive Summary

### Current State
- **Architecture:** Clean Architecture implemented with strict layer boundaries
- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 async, SQLite + aiosqlite
- **Frontend:** React 19, Vite 6, shadcn/ui, TypeScript
- **STT:** Currently using Faster Whisper (local model) — **NEEDS REPLACEMENT**
- **AI:** CrewAI HMAS multi-agent system, OpenAI LLM integration
- **Testing:** 129 unit tests, structure exists for integration/e2e/property tests
- **Code Quality:** 120 Python source files, 2 minor lint issues, 2 type issues

### Critical Issues Identified
1. ❌ **STT Implementation** — Using Faster Whisper instead of Azure Speech Services
2. ⚠️ **Test Coverage** — Unit tests only, missing integration/e2e/property tests
3. ⚠️ **Type Safety** — 2 type checker errors in app_factory.py and settings/base.py
4. ⚠️ **Code Quality** — 2 whitespace lint errors
5. ⚠️ **Documentation** — OpenAPI config exists but not wired into app

### Recommended Actions
1. **IMMEDIATE** — Migrate to Azure Speech Services SDK for live STT
2. **HIGH PRIORITY** — Fix type safety and linting issues
3. **HIGH PRIORITY** — Add integration tests for STT, audio pipeline, database
4. **MEDIUM PRIORITY** — Wire OpenAPI config into FastAPI app
5. **MEDIUM PRIORITY** — Add property tests for registry constants
6. **MEDIUM PRIORITY** — Complete Storybook coverage for React components

---

## Architecture Analysis

### Layer Compliance ✅
Clean Architecture boundaries are correctly enforced:

```
Core (Domain)
  ├── entities/      [No violations found]
  ├── enums/         [No violations found]  
  ├── exceptions/    [No violations found]
  ├── interfaces/    [No violations found]
  └── value_objects/ [No violations found]

Application (Use Cases)
  ├── dtos/          [Depends on: core ✅]
  ├── handlers/      [Depends on: core ✅]
  ├── mappers/       [Depends on: core ✅]
  └── services/      [Depends on: core, infrastructure ✅]

Infrastructure (Adapters)
  ├── adapters/      [Depends on: core ✅]
  ├── audio_streamer/[Depends on: core, config ✅]
  ├── db/            [Depends on: core ✅]
  ├── llm/           [Depends on: core ✅]
  └── stt/           [Depends on: config, utils ✅]

AI (Isolated Vertical)
  ├── chains/        [Depends on: config, utils ✅]
  ├── crewai/        [Depends on: config, utils, core ✅]
  ├── embeddings/    [Depends on: config, utils ✅]
  ├── llm/           [Depends on: config, utils, core ✅]
  ├── pii/           [Depends on: config, utils ✅]
  └── prompts/       [Depends on: config, utils ✅]

Presentation (Interface)
  ├── api/           [Depends on: application, core ✅]
  └── graphql/       [Depends on: application, core ✅]
```

**Known exception:** `config/enums` imports from `core/enums/base` — accepted as pragmatic compromise (documented in KNOWLEDGE.md)

---

## STT Implementation Review — CRITICAL ISSUE ❌

### Current Implementation (Faster Whisper)
**Location:** `backend/src/ekko/infrastructure/stt/transcriber.py`

**Problems:**
1. ❌ **Batch-based, not true streaming** — Collects audio chunks for 5 seconds, then transcribes
2. ❌ **High latency** — 5+ second delay before first transcription
3. ❌ **Local model** — Requires heavy ML dependencies (faster-whisper, numpy)
4. ❌ **Not live** — Pseudo-live implementation with manual batching
5. ❌ **CPU/GPU bound** — Model inference is slow, blocks event loop
6. ❌ **Not using Azure** — User explicitly requires Azure built-in STT

**Current Flow:**
```
Audio bytes → Queue → Batch (5s) → Write WAV → Transcribe → Callback
                           ↑                     ↑
                      Blocking wait        CPU-intensive
```

### Required Implementation (Azure Speech Services)
**Target:** Azure Cognitive Services Speech SDK with continuous recognition

**Benefits:**
1. ✅ **True streaming** — Real-time recognition with partial results
2. ✅ **Low latency** — ~300ms from speech to text
3. ✅ **Cloud-based** — No heavy local dependencies
4. ✅ **Production-ready** — Microsoft-supported, enterprise-grade
5. ✅ **Multiple languages** — Easy language switching
6. ✅ **Speaker diarization** — Can identify different speakers (optional)

**Required Flow:**
```
Audio bytes → Push stream → Azure recognizer → Recognized event → Callback
                                     ↑
                              Real-time streaming
```

---

## Code Quality Analysis

### Linting Issues (2 found)
```bash
$ ruff check src --statistics
2	W293	blank-line-with-whitespace
```
**Impact:** Low — cosmetic only  
**Fix:** Run `ruff check --fix --unsafe-fixes`

### Type Safety Issues (2 found)

#### Issue 1: `app_factory.py:237`
```python
responses=OPENAPI_RESPONSES,  # type: dict[int, dict[str, object]]
# Expected: dict[int | str, dict[str, Any]] | None
```
**Impact:** Medium — FastAPI type mismatch  
**Fix:** Change `object` to `Any` in type annotation

#### Issue 2: `config/settings/base.py:29`
```python
class BaseAppConfig(BaseSettings):  # Pydantic import fallback
```
**Impact:** Low — ty cannot resolve MRO due to import fallback  
**Fix:** Simplify import or suppress warning (acceptable for optional dependency)

---

## Testing Analysis

### Current Coverage
- **Unit tests:** 129 tests ✅
  - GraphQL schema: 25 tests
  - Configuration: tests exist
  - Composition: container tests
  - Health routes: basic coverage
- **Integration tests:** Structure exists, minimal coverage ⚠️
- **E2E tests:** Directory exists, 0 tests ❌
- **Property tests:** Directory exists, 0 tests ❌
- **Performance tests:** Directory exists, 0 tests ❌

### Coverage Requirements (from REQUIREMENTS.md)
- **R006:** Core + application layers: 80%+ line coverage
- **R007:** Integration tests for DB, STT, audio, LLM clients
- **R008:** E2E test for full audio → STT → LLM → response flow
- **R009:** Property tests for registry constants
- **R010:** React component tests with Testing Library
- **R011:** Playwright E2E tests for UI flows
- **R012:** GraphQL schema validation tests

**Gap Analysis:**
- ✅ Unit tests: Good foundation (129 tests)
- ⚠️ Integration: Partially covered
- ❌ E2E: Not implemented
- ❌ Property: Not implemented
- ⚠️ Frontend: Vitest configured, minimal tests

---

## Dependency Analysis

### Current STT Dependencies
```toml
dependencies = [
    "faster-whisper>=1.2.0",  # ❌ TO BE REMOVED
    "numpy>=1.26",            # ⚠️ Keep for audio processing
    ...
]
```

### Required Azure Dependencies
```toml
dependencies = [
    "azure-cognitiveservices-speech>=1.40.0",  # ✅ ADD
    "numpy>=1.26",                              # ✅ KEEP
    ...
]
```

### Other Dependencies Review
- **FastAPI 0.116+**: ✅ Modern, up-to-date
- **SQLAlchemy 2.0+**: ✅ Async support, best practices
- **Pydantic v2**: ✅ Latest stable
- **Strawberry GraphQL**: ✅ Modern GraphQL library
- **CrewAI 0.100+**: ✅ Latest multi-agent framework
- **structlog**: ✅ Best-in-class structured logging

**Verdict:** Dependencies are modern and well-chosen. Only STT stack needs replacement.

---

## Security Analysis

### Secrets Management ✅
- Uses Pydantic `SecretStr` for API keys
- Environment variables with `EKKO_` prefix
- `.gitignore` excludes `.env` files

### Authentication ⚠️
- Current: Auto-login as `dev-user` (local-only app)
- **Acceptable** for local desktop app
- **Would need proper auth** if deploying to server

### Input Validation ✅
- Pydantic models validate all API inputs
- GraphQL schema enforces types

### Dependency Vulnerabilities
**Recommended:** Add `pip-audit` to CI (R022)

---

## Frontend Analysis

### Current State
- **React 19** with Vite 6 ✅
- **shadcn/ui** components ✅
- **Biome** for linting/formatting ✅
- **Storybook** configured with 2 stories ⚠️

### Gaps
- ❌ Minimal component test coverage
- ❌ Storybook stories incomplete (R023)
- ⚠️ Vite config not optimized for production (R025)
- ❌ Playwright E2E tests not written (R011)

---

## Docker & DevOps Analysis

### Current State
- ✅ `.devcontainer/` exists with compose.yml
- ✅ Containerfile exists
- ✅ GitHub Actions CI configured
- ⚠️ Containerfile doesn't follow golden standard (R013)
- ⚠️ Caddyfile doesn't use snippet imports (R015)
- ❌ `compose.override.yaml` doesn't exist (R016)

### CI/CD
- ✅ Lint, format, type check
- ⚠️ Unit tests only (missing integration)
- ❌ Security scans not in CI (bandit, pip-audit, detect-secrets)
- ❌ Architecture boundary check needs strengthening

---

## Modernization Roadmap

### Phase 1: Critical Fixes (This Session) 🔴
1. **Migrate to Azure Speech Services SDK**
   - Create new `AzureSpeechSTT` class
   - Implement `STTService` protocol
   - Update DI container
   - Remove Faster Whisper dependencies
   - Update tests

2. **Fix Code Quality Issues**
   - Fix 2 lint errors
   - Fix 2 type errors
   - Run full quality gate

3. **Update Documentation**
   - Update PROJECT.md to reflect Azure STT
   - Update REQUIREMENTS.md status
   - Add Azure setup instructions

### Phase 2: Testing Infrastructure (Next Session) 🟡
1. Add integration tests for:
   - Azure STT adapter
   - Audio pipeline
   - Database operations
   - LLM clients

2. Add property tests for:
   - Registry constants validation
   - Config parsing

3. Add basic E2E test for audio flow

### Phase 3: Production Readiness (Future) 🟢
1. OpenAPI wiring
2. Docker standardization
3. CI security scans
4. Frontend test coverage
5. Storybook completion

---

## Implementation Plan — Azure STT Migration

### Files to Create
1. `backend/src/ekko/infrastructure/stt/azure_speech_stt.py` — New Azure implementation
2. `backend/tests/unit/infrastructure/stt/test_azure_speech_stt.py` — Unit tests
3. `backend/tests/integration/stt/test_azure_stt_integration.py` — Integration tests

### Files to Modify
1. `backend/src/ekko/infrastructure/adapters/stt_adapter.py` — Update factory
2. `backend/src/ekko/composition/container.py` — Update DI (may not need changes)
3. `backend/src/ekko/config/settings/base.py` — Add Azure config
4. `backend/pyproject.toml` — Update dependencies
5. `.gsd/PROJECT.md` — Update to reflect Azure STT
6. `.gsd/DECISIONS.md` — Record decision
7. `.gsd/REQUIREMENTS.md` — Update R007 status

### Files to Delete
1. `backend/src/ekko/infrastructure/stt/transcriber.py` — Remove Faster Whisper

### Configuration Changes
**Add to `BaseAppConfig`:**
```python
# ── Azure Speech Services ──────────────────────
azure_speech_key: SecretStr | None = None
azure_speech_region: str = "northeurope"
azure_speech_language: str = "da-DK"
azure_speech_recognition_mode: str = "continuous"  # continuous | single-shot
```

**Environment variables:**
```bash
EKKO_AZURE_SPEECH_KEY=your-azure-key
EKKO_AZURE_SPEECH_REGION=northeurope
EKKO_AZURE_SPEECH_LANGUAGE=da-DK
```

### Protocol Compliance
The existing `STTService` protocol is compatible:
```python
class STTService(Protocol):
    async def start(self) -> None: ...
    async def stop(self) -> None: ...
    async def ensure_queue(self, queue_name: str) -> None: ...
    async def accept_bytes(self, queue_name: str, data: bytes) -> None: ...
```

**Azure implementation will:**
- Use `azure.cognitiveservices.speech.PushAudioInputStream` for bytes
- Maintain per-queue recognizers
- Emit recognized text via callback
- Support continuous recognition for true streaming

---

## Risk Assessment

### Migration Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Azure SDK incompatible with asyncio | Low | High | Use `asyncio.to_thread()` for SDK calls |
| Audio format mismatch | Medium | High | Test with actual audio pipeline early |
| Latency worse than Whisper | Low | Medium | Azure STT is typically faster than local |
| Cost (Azure API calls) | Medium | Low | Local dev uses free tier, document limits |

### Breaking Changes
- ⚠️ **STT Interface:** None — protocol stays the same
- ⚠️ **Configuration:** New env vars required
- ⚠️ **Dependencies:** Different package (backward compatible removal)
- ⚠️ **Audio Format:** May need adjustment (test thoroughly)

---

## Success Criteria

### Must Have ✅
- [ ] Azure Speech Services SDK integrated and working
- [ ] Existing STT tests updated and passing
- [ ] Audio → STT → callback flow verified end-to-end
- [ ] No Faster Whisper code remains
- [ ] All linting and type errors fixed
- [ ] Documentation updated (PROJECT.md, REQUIREMENTS.md)

### Should Have 🎯
- [ ] Integration test for Azure STT
- [ ] Error handling for network failures, API limits
- [ ] Graceful degradation if Azure credentials missing
- [ ] Performance comparable or better than Faster Whisper

### Nice to Have 🌟
- [ ] Support for interim results (real-time partial transcriptions)
- [ ] Language detection (auto-detect from audio)
- [ ] Speaker diarization (identify multiple speakers)
- [ ] Profanity filtering (optional config)

---

## Appendix: Key File Locations

### STT Infrastructure
- `backend/src/ekko/core/interfaces/audio.py` — STTService protocol
- `backend/src/ekko/infrastructure/stt/` — STT implementations
- `backend/src/ekko/infrastructure/adapters/stt_adapter.py` — Factory
- `backend/src/ekko/composition/container.py` — DI wiring

### Configuration
- `backend/src/ekko/config/settings/base.py` — Base settings
- `backend/src/ekko/config/settings/local.py` — Local overrides
- `backend/src/ekko/config/settings/test_env.py` — Test config

### Tests
- `backend/tests/unit/` — Unit tests (129 existing)
- `backend/tests/integration/` — Integration tests (sparse)
- `backend/tests/e2e/` — E2E tests (none yet)
- `backend/tests/property/` — Property tests (none yet)

### Documentation
- `.gsd/PROJECT.md` — Living project description
- `.gsd/REQUIREMENTS.md` — Requirements contract
- `.gsd/DECISIONS.md` — Architectural decisions
- `.gsd/KNOWLEDGE.md` — Lessons learned

---

## Next Steps

1. **Create Azure STT implementation** (this session)
2. **Update configuration and dependencies** (this session)
3. **Fix linting and type errors** (this session)
4. **Update documentation** (this session)
5. **Run full test suite** (this session)
6. **Integration tests** (next session - M001/S02)
7. **E2E tests** (next session - M001/S02)

**Estimated Time:** 2-3 hours for Phase 1 (Azure migration + cleanup)
