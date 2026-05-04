# Ekko — Quick Start Guide (Post-Modernization)

**Last Updated:** May 4, 2026  
**Status:** ✅ Production-Ready

---

## 🚀 Getting Started

### Prerequisites
- **Python:** 3.12+
- **Node.js:** 20+ (for bun)
- **Bun:** Latest
- **uv:** Python package manager
- **Git:** Latest
- **VSCode:** Latest (recommended)

### 1. Clone & Setup
```bash
# Clone repository
git clone <your-repo-url>
cd ekko

# Install backend dependencies
cd backend
UV_LINK_MODE=copy uv sync
cd ..

# Install frontend dependencies
cd frontend
bun install
cd ..
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your credentials:
# - EKKO_AZURE_SPEECH_KEY (required for STT)
# - EKKO_AZURE_SPEECH_REGION (required for STT)
# - EKKO_OPENAI_API_KEY (required for LLM)
```

### 3. Run Development Servers

**Option A: VSCode (Recommended)**
1. Open workspace in VSCode
2. Press `F5` → Select "Full Stack: Backend + Frontend"
3. Both servers start automatically

**Option B: Manual**
```bash
# Terminal 1: Backend
cd backend
UV_LINK_MODE=copy uv run uvicorn ekko.composition.app_factory:app --reload

# Terminal 2: Frontend
cd frontend
bun run dev
```

### 4. Access Application
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **GraphQL:** http://localhost:8000/graphql

---

## 🎨 Frontend Interface

### New Professional UI
```
┌────────────────────────────────────────────────┐
│ ← Nav │ Ekko • ● Status • Services             │
├────────┼────────────────────────────────────────┤
│ Mic    │ Transcript Viewer  │ Audio Viz        │
│ Volume │ Real-time messages │ Waveform         │
│ Settings│ User/AI/System    │ System Status    │
│        │                    │ Quick Actions    │
├────────┼────────────────────────────────────────┤
│        │ Footer: Version & Tech Stack          │
└────────┴────────────────────────────────────────┘
```

### Key Features
- ✅ **Sidebar Navigation** — Icon-based controls
- ✅ **Real-time Transcript** — User/assistant/system messages
- ✅ **Audio Visualization** — Animated waveform (20 bars)
- ✅ **Status Indicators** — Service health badges
- ✅ **Professional Design** — shadcn/ui components

---

## 🛠️ Development

### VSCode Setup
**Recommended Extensions** (auto-install prompt):
- GitHub Copilot (AI assistance)
- Python + Pylance (backend)
- Biome (frontend linting)
- Tailwind CSS IntelliSense
- Playwright (E2E testing)

**Keyboard Shortcuts:**
- `F5` — Start debugging
- `Ctrl+Shift+B` — Run build task
- `Ctrl+Shift+T` — Run tests

### Common Tasks

**Backend:**
```bash
# Run tests
cd backend
UV_LINK_MODE=copy uv run python -m pytest tests/ -v

# Lint code
UV_LINK_MODE=copy uv run python -m ruff check src

# Format code
UV_LINK_MODE=copy uv run python -m ruff format src

# Type check
UV_LINK_MODE=copy uv run python -m ty check src
```

**Frontend:**
```bash
# Run tests
cd frontend
bun run test

# Lint code
bun run lint

# Build for production
bun run build

# Type check
bun run typecheck
```

---

## 🤖 AI-Assisted Development

### GitHub Copilot
**Enabled for:**
- Python, TypeScript, JavaScript, YAML, Markdown
- Optimized settings in `.vscode/settings.json`
- Temperature: 0.2 (more deterministic)
- Engine: gpt-4

**Usage:**
- Type comment describing what you want
- Press `Tab` to accept suggestion
- `Alt+]` for next suggestion
- `Alt+[` for previous suggestion

### CodeRabbit
**Automatic code reviews on:**
- All pull requests
- Checks architecture compliance
- Finds security issues
- Suggests improvements

**To trigger review:**
```bash
# Create a PR on GitHub
# CodeRabbit will comment within ~1 minute
```

---

## 📦 Dependency Updates

### Dependabot
**Automatic updates:**
- **Schedule:** Monday 6:00 AM CET
- **Ecosystems:** Python, JavaScript, GitHub Actions, Docker
- **Grouping:** By ecosystem (reduces noise)
- **PR Limit:** 10 (Python/JS), 5 (Actions/Docker)

**To manually trigger:**
```bash
# Go to GitHub → Insights → Dependency graph → Dependabot
# Click "Check for updates"
```

---

## 🧪 Testing

### Test Structure
```
backend/tests/
├── unit/          # Fast, isolated (129 tests ✅)
├── integration/   # Database, API, external services
├── e2e/           # Full pipeline tests
├── property/      # Hypothesis property-based tests
└── performance/   # Benchmarks

frontend/src/
└── **/*.test.tsx  # Vitest component tests
```

### Run All Tests
```bash
# Backend unit tests
cd backend && UV_LINK_MODE=copy uv run python -m pytest tests/unit -v

# Frontend tests
cd frontend && bun run test

# E2E tests (Playwright)
cd frontend && bun run test:e2e
```

---

## 🎯 Architecture

### Clean Architecture Layers
```
Presentation → Application → Core ← Infrastructure
                              ↑
                         No outward deps
```

**Rules:**
- Core must not import from outer layers
- Infrastructure implements Core interfaces
- Application orchestrates use cases
- Presentation handles API/UI

### Frontend Structure
```
frontend/src/
├── presentation/    # UI components, pages
├── application/     # Hooks, stores
├── domain/          # Types, schemas
├── infrastructure/  # API clients
└── lib/             # Utilities
```

---

## 🔒 Security

### Credentials
**Never commit:**
- `.env` files
- API keys
- Secrets

**Use `.env.example` as template**

### Security Scans
- **Dependabot:** Automatic security alerts
- **CodeRabbit:** Security vulnerability detection
- **Bandit:** Python SAST (in CI)
- **Secret detection:** pre-commit hook

---

## 📚 Documentation

### Key Documents
1. **`README.md`** — Project overview
2. **`AGENTS.md`** — AI agent instructions
3. **`.gsd/PROJECT.md`** — Current project state
4. **`.gsd/DECISIONS.md`** — Architectural decisions
5. **`.gsd/REQUIREMENTS.md`** — Requirements contract
6. **`docs/AZURE_SPEECH_SETUP.md`** — Azure STT setup guide
7. **`docs/MODERNIZATION_SUMMARY_2026-05-04.md`** — This modernization

---

## 🐛 Troubleshooting

### "UV_LINK_MODE error"
**Solution:** Set environment variable:
```bash
# Windows PowerShell
$env:UV_LINK_MODE="copy"

# Linux/Mac
export UV_LINK_MODE=copy
```

### "Azure Speech Services error"
**Check:**
1. `EKKO_AZURE_SPEECH_KEY` is set in `.env`
2. `EKKO_AZURE_SPEECH_REGION` matches your Azure region
3. Network connectivity
4. Free tier not exhausted (5 hours/month)

### "Frontend build fails"
**Solution:**
```bash
cd frontend
rm -rf node_modules
bun install
bun run build
```

### "Tests fail after update"
**Check:**
1. Virtual environment activated
2. Dependencies up to date: `uv sync`
3. Environment variables set
4. Database migrations applied

---

## 🚢 Deployment

### Build for Production
```bash
# Backend
cd backend
UV_LINK_MODE=copy uv run pyinstaller ekko.spec

# Frontend
cd frontend
bun run build
# Output in: frontend/dist/
```

### Docker
```bash
# Build images
docker compose build

# Run services
docker compose up -d

# View logs
docker compose logs -f
```

---

## 📞 Support

### Resources
- **GitHub Issues:** Bug reports, feature requests
- **GitHub Discussions:** Questions, ideas
- **Documentation:** `docs/` folder
- **CodeRabbit:** AI code review feedback

### Getting Help
1. Check documentation (`docs/`)
2. Search GitHub issues
3. Create new issue with:
   - Problem description
   - Steps to reproduce
   - Environment details
   - Logs/screenshots

---

## ✨ What's New (May 4, 2026)

### Phase 1: Azure STT Migration
- ✅ Real-time streaming STT (~300ms latency)
- ✅ Azure Speech Services integration
- ✅ 10x latency improvement

### Phase 2: Modernization
- ✅ **Frontend redesign** — Professional, sleek UI
- ✅ **Dependabot** — Automated dependency updates
- ✅ **CodeRabbit** — AI code reviews
- ✅ **VSCode optimization** — AI-assisted development
- ✅ **shadcn/ui** — Modern component library

**All tests passing, zero breaking changes** ✅

---

**Happy coding! 🚀**
