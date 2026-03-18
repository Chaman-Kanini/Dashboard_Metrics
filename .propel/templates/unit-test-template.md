# Unit Test Plan - [TASK_XXX]

## Requirement Reference
- **User Story**: [us_XXX]
- **Story Location**: [.propel/context/tasks/us_XXX/us_XXX.md]
- **Layer**: [FE/BE/DB/Infra]
- **Related Test Plans**: [Links to other layer test plans for same US]
- **Acceptance Criteria Covered**:
  - [AC-1: Description from user story]
  - [AC-2: Description from user story]

## Test Plan Overview
[High level description of what this test plan covers - purpose and scope]

## Dependent Tasks
- [List of tasks/test plans that must complete before this one]

## Components Under Test

| Component | Type | File Path | Responsibilities |
|-----------|------|-----------|------------------|
| [ComponentName] | [class/function/service/controller] | [src/path/to/file.ts] | [What this component does] |

## Test Cases

| Test-ID | Type | Description | Given | When | Then | Assertions |
|---------|------|-------------|-------|------|------|------------|
| TC-001 | positive | [Test description] | [Precondition/setup] | [Action/trigger] | [Expected outcome] | [Specific assertions to verify] |
| TC-002 | negative | [Invalid input test] | [Invalid state] | [Action] | [Error handling] | [Error message/code] |
| EC-001 | edge_case | [Boundary test] | [Boundary condition] | [Action] | [Expected behavior] | [Boundary validation] |
| ES-001 | error | [Error scenario] | [Error condition] | [Action] | [Graceful handling] | [Error state assertions] |

## AI Component Test Cases [CONDITIONAL: If AIR-XXX in scope]

> **Note:** This section applies only when the user story maps to AIR-XXX requirements.
> Skip this section entirely if AI Impact = No.

**AI Requirements Covered:**
- [AIR-001: Description from design.md]
- [AIR-002: Description from design.md]

| Test-ID | Type | Description | Input | Expected | Assertions |
|---------|------|-------------|-------|----------|------------|
| AI-001 | prompt_mock | Verify prompt construction | User query: "[test input]" | Formatted prompt string | Contains system prompt, user context, token count < budget |
| AI-002 | response_parse | Verify output parsing | LLM response: "[mock response]" | Structured data object | Schema valid, required fields present |
| AI-003 | fallback | Test confidence threshold | Low confidence response | Fallback triggered | Deterministic path executed, fallback format matches |
| AI-004 | guardrails_input | Test PII detection in input | Input with PII: "[PII test input]" | PII redacted | No PII in sanitized output |
| AI-005 | guardrails_output | Test output validation | Invalid schema response | Validation error | Schema validation triggered, error logged |
| AI-006 | token_budget | Test token limit enforcement | Large input exceeding budget | Truncated input | Token count ≤ budget, truncation logged |
| AI-007 | rate_limit | Test rate limit handling | Rate limited response (429) | Retry with backoff | Backoff triggered, retry count ≤ max |
| AI-008 | model_error | Test model failure handling | Model timeout/5xx error | Graceful degradation | Error logged, fallback response returned |

### AI Test Case Design Patterns

**Prompt Construction Test:**
```
Given: User query = "[test input]", context = "[mock context]"
When: Prompt template is rendered
Then:
  - Prompt contains system instruction block
  - Prompt contains user query
  - Prompt contains context (if RAG)
  - Total token count < configured budget
```

**Response Parsing Test:**
```
Given: LLM returns mocked response "[predetermined JSON/text]"
When: Response parser processes output
Then:
  - Output matches expected schema
  - Required fields are extracted correctly
  - Optional fields handled appropriately
```

**Fallback Logic Test:**
```
Given: LLM returns confidence score < threshold (e.g., 0.3)
When: Confidence evaluation runs
Then:
  - Fallback path is triggered
  - Fallback response matches expected format
  - Audit log records fallback reason
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | [tests/unit/componentName.spec.ts] | [Unit tests for ComponentName] |
| CREATE | [tests/mocks/serviceName.mock.ts] | [Mock for ServiceName dependency] |
| CREATE | [tests/fixtures/testData.ts] | [Test data fixtures] |

## Mocking Strategy

| Dependency | Mock Type | Mock Behavior | Return Value |
|------------|-----------|---------------|--------------|
| [ServiceName] | mock | [When method X called] | [Return value or throw error] |
| [APIClient] | stub | [Always return] | [Fixed response data] |
| [Logger] | spy | [Track calls] | [Pass through] |

## AI Mocking Strategy [CONDITIONAL: If AIR-XXX in scope]

| Dependency | Mock Type | Mock Approach | Example Return |
|------------|-----------|---------------|----------------|
| LLM API | GenericFakeChatModel | Returns predetermined responses | `{"response": "mocked answer", "confidence": 0.95}` |
| Embedding Model | Fixed vectors | Returns consistent embeddings | `[0.1, 0.2, ..., 0.9]` (1536-dim) |
| Vector Store | In-memory mock | Returns predetermined chunks | `[{"id": "doc1", "text": "...", "score": 0.85}]` |
| AI Gateway | Mock gateway | Bypasses routing/caching | Direct mock response |
| Guardrails | Pass-through or mock | Configurable validation | `{"valid": true}` or validation errors |

### AI Mock Response Factory

```typescript
// Example mock factory for consistent LLM responses
const createMockLLMResponse = (overrides = {}) => ({
  content: "Default mocked response",
  confidence: 0.9,
  tokens_used: 150,
  model: "gpt-4-turbo",
  ...overrides
});

// Example mock for low-confidence scenario
const lowConfidenceResponse = createMockLLMResponse({ confidence: 0.2 });

// Example mock for error scenario
const errorResponse = { error: "Rate limit exceeded", status: 429 };
```

## Test Data

| Scenario | Input Data | Expected Output |
|----------|------------|-----------------|
| [Valid case] | `{ field: "value" }` | `{ result: "success" }` |
| [Invalid case] | `{ field: null }` | `Error: "Field required"` |
| [Edge case] | `{ field: "" }` | `{ result: "empty" }` |

## Test Commands
- **Run Tests**: [command to run tests, e.g., `npm test -- --testPathPattern=componentName`]
- **Run with Coverage**: [e.g., `npm run test:coverage -- --collectCoverageFrom='src/path/**'`]
- **Run Single Test**: [e.g., `npm test -- -t "test name"`]

## Coverage Target
- **Line Coverage**: [X]%
- **Branch Coverage**: [X]%
- **Critical Paths**: [List specific functions/branches that MUST have 100% coverage]

## Documentation References
- **Framework Docs**: [Link to testing framework documentation]
- **Project Test Patterns**: [Link to existing test examples in codebase]
- **Mocking Guide**: [Link to mocking library documentation]

## Implementation Checklist
- [ ] Create test file structure per Expected Changes
- [ ] Set up test data fixtures per Test Data section
- [ ] Configure mocking dependencies per Mocking Strategy
- [ ] Implement positive test cases (TC-XXX)
- [ ] Implement negative test cases
- [ ] Implement edge case tests (EC-XXX)
- [ ] Implement error scenario tests (ES-XXX)
- [ ] Run test suite and validate coverage meets target

### AI Test Implementation Checklist [CONDITIONAL: If AIR-XXX in scope]
- [ ] Set up AI mock factory (LLM, embedding, vector store mocks)
- [ ] Implement prompt construction tests (AI-001)
- [ ] Implement response parsing tests (AI-002)
- [ ] Implement fallback logic tests (AI-003)
- [ ] Implement guardrails input tests (AI-004)
- [ ] Implement guardrails output tests (AI-005)
- [ ] Implement token budget tests (AI-006)
- [ ] Implement rate limit handling tests (AI-007)
- [ ] Implement model error handling tests (AI-008)
- [ ] Validate all AIR-XXX requirements have corresponding tests
- [ ] Verify no actual LLM API calls are made in unit tests (all mocked)
