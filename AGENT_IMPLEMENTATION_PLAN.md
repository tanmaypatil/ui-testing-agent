# Implementation Plan: Autonomous Test Agent for Web Application

## Overview

Add an AI-powered autonomous test agent that can test the transaction processing application using vision and reasoning, complementing the existing Playwright tests.

**Current State:**
- Working Flask application with login and payment flows
- Traditional Playwright test (1 test with pre-scripted steps)
- Clean, well-documented codebase
- 2 test accounts in metadata.json

**Goal:**
- Build an autonomous agent that can complete payment flows without pre-scripted steps
- Agent uses Claude's vision capabilities to "see" and interact with the UI
- Keep existing Playwright tests (hybrid approach)
- Demonstrate agent-based testing for exploratory scenarios

---

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│         Autonomous Test Agent                   │
│  ┌───────────────────────────────────────────┐ │
│  │  Agent Loop (Python)                      │ │
│  │  - Observe (screenshot)                   │ │
│  │  - Analyze (Claude Vision API)            │ │
│  │  - Decide (Claude reasoning)              │ │
│  │  - Act (Playwright commands)              │ │
│  │  - Reflect (update conversation)          │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
               │                    │
               │                    │
       ┌───────▼──────┐    ┌───────▼──────────┐
       │  Playwright  │    │  Claude API      │
       │  Browser     │    │  (Vision +       │
       │  Automation  │    │   Reasoning)     │
       └───────┬──────┘    └──────────────────┘
               │
               ▼
       ┌──────────────┐
       │ Web App      │
       │ (Flask)      │
       └──────────────┘
```

---

## Technology Stack

### New Dependencies
- **anthropic** (latest) - Claude API client with vision support
- **pillow** - Image processing for screenshots
- **python-dotenv** - Environment variable management for API keys

### Existing Stack (Reused)
- **Playwright** - Browser automation
- **Pytest** - Test framework
- **Flask** - Application under test

---

## Implementation Plan

### Phase 1: Setup & Configuration

#### 1.1 Install Dependencies
Create `tests/agent_requirements.txt`:
```txt
anthropic>=0.18.0
pillow>=10.0.0
python-dotenv>=1.0.0
```

#### 1.2 Environment Configuration
Create `.env` file (root directory):
```bash
ANTHROPIC_API_KEY=your_api_key_here
AGENT_MODEL=claude-opus-4-5-20251101
MAX_AGENT_ITERATIONS=15
```

Add to `.gitignore`:
```
.env
```

#### 1.3 Update Documentation
Update `README.md` with:
- Agent testing section
- API key setup instructions
- Cost considerations

---

### Phase 2: Core Agent Implementation

#### 2.1 Agent Framework (`tests/autonomous_agent.py`)

**Responsibilities:**
- Manage agent loop (observe → analyze → decide → act)
- Interface with Claude API
- Convert screenshots to base64
- Parse agent decisions into Playwright actions
- Maintain conversation history

**Key Classes:**
```python
class AutonomousTestAgent:
    def __init__(self, page, anthropic_client, goal, max_iterations=15)
    def run(self) -> AgentResult
    def _take_screenshot(self) -> bytes
    def _analyze_screen(self, screenshot: bytes) -> str
    def _decide_action(self, analysis: str) -> Action
    def _execute_action(self, action: Action) -> bool
    def _is_goal_complete(self, analysis: str) -> bool

class Action:
    type: str  # "click", "fill", "wait", "complete"
    selector: str
    value: Optional[str]
    reasoning: str

class AgentResult:
    success: bool
    final_state: str
    transaction_id: Optional[str]
    iterations_used: int
    screenshots: List[bytes]
    conversation_history: List[dict]
```

#### 2.2 Action Parser (`tests/action_parser.py`)

**Responsibilities:**
- Parse Claude's natural language responses into structured actions
- Extract selectors, values, and reasoning
- Handle multiple action formats

**Functions:**
```python
def parse_action_from_response(response: str) -> Action
def extract_selector(text: str) -> str
def extract_transaction_id(text: str) -> Optional[str]
def is_completion_signal(text: str) -> bool
```

#### 2.3 Prompt Engineering (`tests/agent_prompts.py`)

**System Prompt Template:**
```python
SYSTEM_PROMPT = """
You are an autonomous web testing agent. Your task is to test a transaction
processing web application by interacting with it through screenshots.

CAPABILITIES:
- You can see the current state of the web page through screenshots
- You can perform actions: CLICK, FILL, WAIT, COMPLETE
- You can read text, identify form fields, and verify outcomes

RESPONSE FORMAT:
Always respond in this format:

OBSERVATION: [What you see on the screen]
REASONING: [Why you're taking this action]
ACTION: [One of: CLICK <selector>, FILL <selector> <value>, WAIT, COMPLETE]

SELECTORS:
- Use CSS selectors like #id or .class
- Prefer IDs when available
- Be specific to avoid ambiguity

COMPLETION:
When the goal is achieved, use ACTION: COMPLETE and state the transaction ID.

CONSTRAINTS:
- Maximum {max_iterations} actions allowed
- If stuck, try alternative approaches
- Verify each action's result before proceeding
"""

INITIAL_USER_PROMPT_TEMPLATE = """
GOAL: {goal}

CONTEXT:
- Application: Transaction Processing System
- URL: http://localhost:5001
- Demo credentials: username='demo', password='password'
- Available accounts:
  - 123456789 (Vernor Vinge)
  - 987654321 (Issac Asimov)

BEGIN TESTING:
I will provide you with screenshots after each action. Analyze the screen and
decide your next action to achieve the goal.
"""
```

---

### Phase 3: Test Cases

#### 3.1 Basic Agent Test (`tests/test_autonomous_agent.py`)

**Test: Autonomous Payment Flow**
```python
def test_autonomous_payment_flow(flask_server, anthropic_api_key):
    """
    Agent autonomously completes a payment without pre-scripted steps.

    Agent should:
    1. Identify login form
    2. Fill credentials
    3. Navigate to payment page
    4. Select accounts
    5. Enter amount
    6. Submit payment
    7. Verify transaction ID
    """

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:5001")

        agent = AutonomousTestAgent(
            page=page,
            anthropic_client=Anthropic(api_key=anthropic_api_key),
            goal="Complete a payment of $250.00 from Vernor Vinge to Issac Asimov",
            max_iterations=15
        )

        result = agent.run()

        # Assertions
        assert result.success, f"Agent failed: {result.final_state}"
        assert result.transaction_id is not None
        assert result.transaction_id.startswith("txn_")
        assert result.iterations_used <= 15

        browser.close()
```

#### 3.2 Error Recovery Test

**Test: Agent Handles Invalid Input**
```python
def test_agent_error_recovery(flask_server, anthropic_api_key):
    """
    Agent should recognize and recover from errors (e.g., wrong password).
    """
    # Agent tries wrong password first, then corrects
```

#### 3.3 Exploratory Test

**Test: Agent Explores Different Amounts**
```python
def test_agent_multiple_scenarios(flask_server, anthropic_api_key):
    """
    Agent completes payments with various amounts: $1, $100, $9999.99
    """
    # Run agent 3 times with different goals
```

---

### Phase 4: Fixtures & Utilities

#### 4.1 Pytest Fixtures (`tests/conftest_agent.py`)

```python
import pytest
import os
from anthropic import Anthropic
from dotenv import load_dotenv

@pytest.fixture(scope="session")
def anthropic_api_key():
    """Load Anthropic API key from environment."""
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("ANTHROPIC_API_KEY not set in .env file")
    return api_key

@pytest.fixture(scope="session")
def anthropic_client(anthropic_api_key):
    """Create Anthropic client."""
    return Anthropic(api_key=anthropic_api_key)

@pytest.fixture
def agent_config():
    """Agent configuration parameters."""
    load_dotenv()
    return {
        "model": os.getenv("AGENT_MODEL", "claude-opus-4-5-20251101"),
        "max_iterations": int(os.getenv("MAX_AGENT_ITERATIONS", "15")),
        "temperature": 0.0  # Deterministic for testing
    }
```

#### 4.2 Debugging Utilities (`tests/agent_debug.py`)

```python
def save_agent_trace(result: AgentResult, output_dir: str):
    """
    Save agent execution trace for debugging:
    - Screenshots at each step
    - Conversation history
    - Final result JSON
    """

def print_agent_conversation(result: AgentResult):
    """Pretty-print agent's decision-making process."""
```

---

### Phase 5: Integration & Documentation

#### 5.1 Update Test Configuration

**pytest.ini:**
```ini
[pytest]
markers =
    agent: marks tests that use autonomous agent (may be slow, requires API key)
    traditional: marks traditional Playwright tests
```

**Run commands:**
```bash
# Run only traditional tests (fast, no API costs)
pytest -m traditional

# Run only agent tests (slower, API costs)
pytest -m agent

# Run all tests
pytest
```

#### 5.2 Update `.gitignore`

```
# API keys and secrets
.env

# Agent test artifacts
agent_traces/
screenshots_*.png
```

#### 5.3 Documentation Updates

**README.md additions:**
```markdown
## Agent-Based Testing

This project includes autonomous AI-powered tests using Claude's vision API.

### Setup

1. Get API key from https://console.anthropic.com/
2. Create `.env` file:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```
3. Install dependencies:
   ```
   pip install -r tests/agent_requirements.txt
   ```

### Running Agent Tests

```bash
pytest tests/test_autonomous_agent.py -v
```

### Cost Considerations

- Each agent test costs ~$0.015 (1.5 cents)
- 100 test runs ≈ $1.50
- Budget accordingly for CI/CD

### When to Use Agent Tests

- Exploratory testing
- Testing with dynamic data
- Edge case discovery
- New features before stabilization

Use traditional Playwright tests for:
- Critical paths (login, payment)
- Fast CI/CD feedback
- Stable, well-defined flows
```

---

## Critical Files to Create/Modify

### New Files (Create)

1. **tests/autonomous_agent.py** - Core agent loop implementation (~200 lines)
2. **tests/action_parser.py** - Action parsing logic (~100 lines)
3. **tests/agent_prompts.py** - Prompt templates (~80 lines)
4. **tests/test_autonomous_agent.py** - Agent test cases (~150 lines)
5. **tests/conftest_agent.py** - Agent-specific fixtures (~50 lines)
6. **tests/agent_debug.py** - Debugging utilities (~80 lines)
7. **tests/agent_requirements.txt** - Additional dependencies (3 packages)
8. **.env.example** - Example environment file (~10 lines)

### Modified Files

1. **README.md** - Add agent testing section (~50 lines added)
2. **.gitignore** - Add .env and agent artifacts (2 lines)
3. **pytest.ini** - Add agent marker (3 lines)
4. **tests/conftest.py** - Import agent fixtures (1 line)

---

## Implementation Sequence

### Step 1: Environment Setup (15 min)
1. Create `.env.example` with placeholder API key
2. Update `.gitignore`
3. Create `tests/agent_requirements.txt`
4. Install dependencies: `pip install -r tests/agent_requirements.txt`

### Step 2: Prompt Engineering (30 min)
1. Create `tests/agent_prompts.py`
2. Define system prompt with clear action format
3. Create goal-specific prompt templates
4. Test prompt clarity with Claude API manually

### Step 3: Action Parser (30 min)
1. Create `tests/action_parser.py`
2. Implement regex-based parsing for actions
3. Handle edge cases (missing selectors, malformed responses)
4. Write unit tests for parser

### Step 4: Core Agent (1-2 hours)
1. Create `tests/autonomous_agent.py`
2. Implement `AutonomousTestAgent` class
3. Build agent loop: observe → analyze → decide → act
4. Add screenshot capture and base64 encoding
5. Implement Claude API integration with vision
6. Add conversation history management

### Step 5: Fixtures (30 min)
1. Create `tests/conftest_agent.py`
2. Add API key fixture
3. Add agent configuration fixture
4. Add debugging output fixture

### Step 6: First Test (1 hour)
1. Create `tests/test_autonomous_agent.py`
2. Write basic payment flow test
3. Run and debug
4. Adjust prompts based on agent behavior
5. Verify transaction creation in database

### Step 7: Debugging Tools (30 min)
1. Create `tests/agent_debug.py`
2. Add screenshot saving
3. Add conversation trace logging
4. Add pretty-print for agent decisions

### Step 8: Additional Tests (1 hour)
1. Add error recovery test
2. Add multiple scenario test
3. Add performance benchmarks
4. Document expected costs

### Step 9: Documentation (30 min)
1. Update README.md
2. Create AGENT_TESTING.md guide
3. Add cost calculator
4. Add troubleshooting section

---

## Verification Steps

### Manual Verification

1. **Setup verification:**
   ```bash
   # Verify API key is loaded
   python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('Key loaded' if os.getenv('ANTHROPIC_API_KEY') else 'Key missing')"
   ```

2. **Run agent test:**
   ```bash
   pytest tests/test_autonomous_agent.py::test_autonomous_payment_flow -v -s
   ```

3. **Check output:**
   - Agent completes within 15 iterations
   - Transaction ID is captured
   - Database contains new transaction
   - Screenshots saved to debug folder

4. **Verify cost tracking:**
   ```bash
   # Check number of API calls made
   grep "API call" agent_traces/latest.log | wc -l
   ```

### Automated Verification

```bash
# Run all agent tests
pytest -m agent -v

# Verify traditional tests still work
pytest -m traditional -v

# Run everything
pytest -v
```

### Success Criteria

- ✅ Agent completes payment flow without pre-scripted steps
- ✅ Agent handles at least 3 different payment amounts
- ✅ Agent recovers from one error scenario
- ✅ Total test time < 30 seconds per agent test
- ✅ API costs < $0.05 per test run
- ✅ Conversation traces saved for debugging
- ✅ Traditional tests remain unchanged and passing

---

## Cost Analysis

### Per Agent Test Run

| Component | API Calls | Cost |
|-----------|-----------|------|
| Screenshots (avg 7) | 7 | ~$0.014 |
| Reasoning steps | Included | $0 |
| **Total per test** | **7** | **~$0.015** |

### Monthly Estimates

| Usage Pattern | Tests/Month | Cost/Month |
|---------------|-------------|------------|
| Development (10/day) | 300 | $4.50 |
| CI/CD (5 runs/day) | 150 | $2.25 |
| Production monitoring | 50 | $0.75 |
| **Total** | **500** | **$7.50** |

**Budget Recommendation:** $20/month for testing API usage

---

## Hybrid Testing Strategy

### Use Traditional Playwright For:
- ✅ Critical happy paths (login → payment)
- ✅ Regression testing
- ✅ Fast CI/CD feedback (< 5 seconds)
- ✅ Stable, well-defined flows
- ✅ Pre-deployment smoke tests

### Use Autonomous Agent For:
- 🤖 Exploratory testing
- 🤖 Testing with variable data
- 🤖 Edge case discovery
- 🤖 New feature validation
- 🤖 UI change resilience testing
- 🤖 Cross-browser compatibility (future)

### Test Suite Organization

```
tests/
├── traditional/
│   ├── test_payment_flow.py         # Fast, pre-scripted
│   ├── test_login.py                # Fast, pre-scripted
│   └── conftest.py
│
├── agent/
│   ├── test_autonomous_agent.py     # AI-powered, exploratory
│   ├── autonomous_agent.py          # Core agent implementation
│   ├── action_parser.py
│   ├── agent_prompts.py
│   └── conftest_agent.py
│
└── shared/
    └── conftest.py                   # Shared fixtures (Flask server)
```

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| API costs exceed budget | Medium | Set monthly spending limits, cache screenshots |
| Agent gets stuck in loop | Medium | Max iteration limit, timeout fallback |
| Claude API downtime | Low | Gracefully skip agent tests, run traditional |
| Inconsistent agent behavior | Medium | Temperature=0 for determinism, retry logic |
| Slow test execution | Low | Run agent tests separately from CI, parallelize |

---

## Future Enhancements

### Phase 2 (Optional)
- Multi-agent collaboration (separate agents for login, payment)
- Agent learns from past failures (RAG-based memory)
- Natural language test case generation
- Visual regression detection
- Agent reports bugs in natural language

### Phase 3 (Advanced)
- Agent orchestrates multiple user journeys
- Performance testing with agents
- Security testing (injection attempts)
- Accessibility testing via vision analysis

---

## Success Metrics

Track these to measure agent testing value:

1. **Bug Detection Rate:** Bugs found by agent vs traditional tests
2. **Maintenance Effort:** Time spent updating tests after UI changes
3. **Coverage:** UI states explored by agent vs traditional
4. **Cost Efficiency:** Bug detection cost (traditional = $0, agent = $0.015/run)
5. **Execution Time:** Agent test time vs traditional test time

**Expected Results After 1 Month:**
- 2-3 bugs discovered by agent that traditional tests missed
- 50% reduction in test maintenance after UI changes
- 30% increase in UI state coverage
- Total testing costs remain < $20/month

---

## References

- [Anthropic Vision API Docs](https://docs.anthropic.com/claude/docs/vision)
- [Playwright Python Docs](https://playwright.dev/python/)
- [Agent Testing Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/autonomous-agents)

---

**Implementation Time Estimate:** 6-8 hours
**Maintenance Time:** < 1 hour/month
**Monthly API Cost:** $7-20

---

**Document Version:** 1.0
**Last Updated:** 2026-01-11
**Status:** Planning Phase - Not Yet Implemented
