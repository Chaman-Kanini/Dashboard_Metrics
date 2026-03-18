---
description: Generates comprehensive unit test plans from user story specifications with test coverage analysis, test case design, and validation strategies
auto_execution_mode: 1
---

# Unit Test Plan Generator
As an expert QA Engineer and Test Automation Specialist, generate comprehensive unit test plans that ensure code quality, coverage, and maintainability. This command focuses specifically on unit test planning with detailed test case design and validation strategies.

## Input Parameters: $ARGUMENTS (Mandatory)
**Accepts:** User story file path | User story ID | User story URL | User story text

### Argument Types:
1. **User Story File**: Path to us_XXX.md file (e.g., .propel/context/tasks/us_001/us_001.md)
2. **User Story ID**: US ID pattern (us_001, us_002, etc.)
3. **User Story URL**: URL pointing to user story specification
4. **User Story Text**: Direct user story content in "As a... I want... so that..." format

### User Story Input Processing
**When $ARGUMENTS contains user story (file, URL, or text):**
1. **Extract US ID**: Parse us_XXX identifier from file path, content, or generate if text input
2. **Create Test Plan Folder**: Ensure `.propel/context/tasks/us_<ID>/unittest/` directory exists
3. **Test Plan File Naming**: Generate plans as `test_plan_<layer>_<descriptive_name>.md` within unittest folder
4. **Parent Story Reference**: Maintain traceability to parent user story in all test plans
5. **Acceptance Mapping**: Map test cases to user story acceptance criteria

### US ID Extraction Algorithm
**File Input**: Extract us_XXX from file path using pattern matching
- Pattern: `/us_(\d{3})/` or `us_(\d{3})\.md`
- Example: `.propel/context/tasks/us_001/us_001.md` -> Extract `us_001`

**URL Input**:
- First attempt: Parse URL path for us_XXX pattern
- If not found: Fetch URL content and search for US ID in content
- Pattern: `US[_-]?(\d{3,4})`

**Text Input**:
- Search for existing US ID in text: `US[_-]?(\d{3,4})`

**Fallback Behavior**:
- If no US ID can be extracted -> Create test plans in `.propel/context/tasks/us_<short_descriptive_name>/unittest/`
- Log clearly where test plans are being created (US folder vs. fallback folder)

## Output
- Artifact generation: `.propel/context/tasks/us_<ID>/unittest/test_plan_*.md`
- Print the following:
    - List of rules used by the workflow in bulleted format
    - Evaluation Scores in tabular format with average score.
    - Evaluation summary (less than 100 words).
    **Do not save as file.**

**Note:**
- **File Handling**: IF file exists → UPDATE changed sections only (delta mode). IF file does not exist → CREATE complete file.
- Always generate a single unified unit test plan document.
- Generate the output using the `.propel/templates/unit-test-template.md` template.

### Output Specifications

#### File Organization Strategy:
**For User Story Unit Test (US ID found in input):**
- **Directory**: `.propel/context/tasks/us_<ID>/unittest/`
- **File Pattern**: `test_plan_<layer>_<descriptive_name>.md` (layer: fe, be, db, infra)
- **Example**: `.propel/context/tasks/us_001/unittest/test_plan_fe_login_ui.md`
- **Trigger**: Valid us_XXX pattern extracted from file path, URL, or text content

**For General Unit Test (no US ID found - fallback):**
- **Directory**: `.propel/context/tasks/us_<short_descriptive_name>/unittest/`
- **File Pattern**: `test_plan_<layer>_<descriptive_name>.md`
- **Example**: `.propel/context/tasks/us_setup_db/unittest/test_plan_be_setup_database.md`
- **Trigger**: No valid US ID extractable from input -> automatic fallback to root folder

#### Unit Test Organization Examples
```
.propel/context/tasks/
+-- us_001/
|   +-- us_001.md
|   +-- task_001_implement_login_ui.md
|   +-- task_002_implement_auth_api.md
|   +-- unittest/
|       +-- test_plan_fe_login_form.md
|       +-- test_plan_be_auth_api.md
|       +-- test_data/
|       +-- mocks/
|       +-- coverage/
+-- us_002/
|   +-- us_002.md
|   +-- task_001_password_reset.md
|   +-- unittest/
|       +-- test_plan_fe_password_reset.md
|       +-- test_plan_be_password_reset.md
+-- us_general_setup/
|   +-- unittest/
|       +-- test_plan_infra_setup.md
```

**Additional Artifacts:**
- **Test Data Files**: `.propel/context/tasks/us_<ID>/unittest/test_data/`
- **Mock Specifications**: `.propel/context/tasks/us_<ID>/unittest/mocks/`
- **Coverage Reports**: `.propel/context/tasks/us_<ID>/unittest/coverage/`

## Core Principles
- **Acceptance Criteria Mapping**: Every test case traces to specific acceptance criteria
- **Test Independence**: Each test must be isolated and independently executable
- **Coverage Completeness**: Include happy path, edge cases, and error scenarios

### Task Decomposition Rule
- **Maximum Checklist Items Per Test Plan**: If checklist items exceed 8 for a single test plan, the plan MUST be decomposed into smaller layer-specific plans
- **Decomposition Strategy**:
  1. Group tests by technology layer (FE, BE, DB, Infra)
  2. Split complex plans into independently testable units
  3. Ensure each decomposed plan remains under 8 hours of effort
  4. Maintain traceability: Test Plan -> User Story -> Epic
- **Validation Gate**: Before finalizing test plan generation, count checklist items. If > 8, trigger decomposition process

## Execution Flow

### 1. User Story Analysis
- **Acceptance Criteria Mapping**: Extract all Given/When/Then scenarios from user story
- **Edge Case Identification**: Enumerate all boundary conditions and error scenarios
- **Business Logic Extraction**: Identify core business rules requiring validation
- **Component Identification**: List all functions, methods, classes, and modules to be tested
- **Dependency Analysis**: Map external dependencies, mocks, and test doubles needed

#### 2. Codebase Intelligence Gathering
- **Implementation Task Review**: Read all test_XXX files in .propel/context/tasks/us_XXX/ folder
- **Pattern Discovery**: Search for existing unit test patterns in codebase
- **Framework Detection**: Identify testing framework used (Jest, pytest, xUnit, JUnit, etc.)
- **Test Structure Analysis**: Review existing test file organization and naming conventions
- **Coverage Strategy**: Determine code coverage tools and targets used in project
- **Mock Strategy**: Identify mocking libraries and patterns (unittest.mock, Jest mocks, Mockito, etc.)

#### 3. Technology Stack Detection
**CRITICAL**: Identify technology stack from implementation tasks and codebase:
- **Frontend Frameworks**: React, Angular, Vue, Svelte (use Jest, Vitest, Karma)
- **Backend Frameworks**: Node.js, Python, .NET, Java, Go (use appropriate test frameworks)
- **Database Layer**: SQL, NoSQL, ORM testing strategies
- **API Layer**: REST, GraphQL, gRPC testing approaches
- **Version Pinning**: Use `mcp__context7__resolve-library-id` to pin exact testing framework versions

#### 4. AI/LLM Testing Strategy [CONDITIONAL: If design.md contains AIR-XXX]

**Detection Gate:**
```
Grep("AIR-\d{3}", ".propel/context/docs/design.md") → air_requirements
IF air_requirements.count > 0 → Apply AI Testing Strategy
```

**LLM Output Testing Approach:**
- Use evaluation-based testing (NOT deterministic assertions for LLM outputs)
- Mock LLM responses using GenericFakeChatModel (LangChain) or equivalent
- Define scoring functions for output quality (relevance, faithfulness, coherence)
- Test passes if score meets threshold (e.g., relevance ≥ 0.8)

**Test Categories for AI Components:**

| Category | Focus | Tool/Framework | When to Use |
|----------|-------|----------------|-------------|
| Unit (Mocked) | Prompt formatting, parsing, orchestration | pytest/Jest + mocks | Always for AI code |
| Evaluation | Output quality (relevance, faithfulness) | DeepEval, RAGAS, LangSmith | RAG and generation tasks |
| Integration | End-to-end RAG pipeline | LangSmith, Langfuse | RAG pattern verification |
| Guardrails | Input sanitization, output validation | Custom assertions | Safety requirements |

**Mock Strategy for LLM Dependencies:**

| Dependency | Mock Approach | Example |
|------------|---------------|---------|
| LLM API | GenericFakeChatModel / Mock response factory | Returns predetermined responses for consistent testing |
| Embedding Model | Fixed vectors | Consistent 1536-dim test vectors for retrieval testing |
| Vector Store | In-memory mock | Predetermined retrieval results for known queries |
| AI Gateway | Mock gateway | Bypass routing/caching for unit tests |

**AI Test Case Design Pattern:**
```
# For prompt construction tests
Given: User query = "[test input]"
When: Prompt template is rendered
Then:
  - Contains system prompt
  - Contains user context
  - Token count < budget limit

# For LLM response tests (mocked)
Given: LLM returns mocked response "[predetermined output]"
When: Response is parsed
Then:
  - Output schema is valid
  - Required fields are present
  - No PII in output

# For fallback logic tests
Given: LLM returns low confidence score (< threshold)
When: Confidence is evaluated
Then:
  - Deterministic fallback is triggered
  - Fallback response matches expected format
```

**AI-Specific Test Coverage Requirements:**
- [ ] Prompt template construction tests (formatting, context injection)
- [ ] Response parsing tests (schema validation, field extraction)
- [ ] Guardrails tests (PII detection, prompt injection prevention)
- [ ] Fallback logic tests (confidence threshold, error handling)
- [ ] Token budget tests (input truncation, budget enforcement)
- [ ] Rate limit handling tests (backoff, retry logic)
- [ ] Audit logging tests (log format, PII redaction)

### Deep Research Methodology

Optimize for test quality and comprehensive coverage. Use Context7 MCP for version-specific testing framework documentation.

#### 1. Testing Framework Research
- **Framework Detection**: Identify testing framework from package.json, requirements.txt, or project files
- **Version Pinning**: Use Context7 MCP (`mcp__context7__resolve-library-id`) for exact framework version
- **Documentation Retrieval**: Use Context7 MCP (`mcp__context7__get-library-docs`) for testing patterns
- **Best Practices**: Research framework-specific best practices and anti-patterns
- **Mock Library Research**: Identify and document mocking libraries and patterns

#### 2. Existing Test Analysis
- **Test Pattern Discovery**: Search for existing unit test files in codebase
- **Convention Extraction**: Document naming conventions, file structure, test organization
- **Assertion Patterns**: Identify assertion styles and validation approaches
- **Setup/Teardown Patterns**: Document test lifecycle management approaches
- **Coverage Configuration**: Review existing coverage targets and configurations

#### 3. Component Dependency Analysis
- **Dependency Mapping**: Identify all dependencies for components under test
- **Mock Candidates**: Determine which dependencies should be mocked
- **Test Double Strategy**: Define mocks, stubs, spies, fakes for each dependency
- **Integration Points**: Identify boundaries between unit and integration testing

#### MCP Fallback Protocol
**If Context7 MCP unavailable:**
- Use web search: "[testing framework] [version] official documentation [current year]"
- Document: "Fallback: Web search for docs (Context7 unavailable)"

**If both unavailable:**
- Use package.json/requirements.txt for framework version detection
- Search codebase for existing test patterns
- Document: "Fallback: Codebase analysis only (MCP unavailable)"

### Unit Test Planning Methodology

#### Test Plan Structure

##### 1. Test Scope Definition
**User Story Context:**
- **US ID**: [us_XXX]
- **User Story Title**: [Extracted from user story]
- **User Story Description**: [As a... I want... so that...]
- **Implementation Tasks**: [List of task files in us_XXX folder]

**Testing Objectives:**
- **Primary Goal**: [What aspect of functionality is being validated]
- **Coverage Target**: [Percentage or specific components]
- **Quality Gates**: [Pass criteria for test suite]

##### 2. Test Component Identification
**Components Under Test:**

| Component | Type | File Path | Priority | Mock Dependencies |
|-----------|------|-----------|----------|-------------------|
| [ComponentName] | [class/function/service] | [src/path/to/file.ts] | [high/med/low] | [deps to mock] |

##### 3. Test Case Design

**Before writing test cases, list all tests to generate:**
| Test-ID | Summary | Type |
|---------|---------|------|
| ... | ... | ... |
**Now expand each test listed above.**

**Test Case Table Format** (use template structure):

| Test-ID | Type | Description | Given | When | Then | Assertions |
|---------|------|-------------|-------|------|------|------------|
| TC-001 | positive | [Description] | [Precondition] | [Action] | [Expected] | [Assertions] |
| TC-002 | negative | [Description] | [Invalid state] | [Action] | [Error] | [Error check] |
| EC-001 | edge_case | [Boundary] | [Boundary condition] | [Action] | [Behavior] | [Validation] |

#### Test Coverage Analysis

##### 1. Code Coverage Metrics

| Metric | Target | Critical Paths |
|--------|--------|----------------|
| Line Coverage | 80% | 95% |
| Branch Coverage | 75% | - |

### Context Documentation Requirements

**Essential References:**
- **User Story**: `.propel/context/tasks/us_XXX/us_*.md` (Acceptance Criteria, Edge Cases)
- **Implementation Tasks**: `task_*.md` files in us_XXX folder
- **Testing Framework Docs**: Framework documentation (version-pinned via Context7 or web search)
- **Project Conventions**: Existing test patterns, code standards, coverage config

### Implementation Instructions

#### Automated Test Plan Generation Flow
```
1. Parse $ARGUMENTS to determine input type (file/ID/URL/text)
2. Extract user story content based on argument type
3. Parse US ID using pattern matching (us_XXX)
4. Read implementation tasks from .propel/context/tasks/us_XXX/ folder
5. Analyze codebase to identify:
   a. Technology stack and testing framework
   b. Existing test patterns and conventions
   c. Component locations and dependencies
6. Pin testing framework version using Context7
7. Extract acceptance criteria and edge cases from user story
8. Design test cases for each criterion. For each, answer: (1) What is being tested? (2) What inputs? (3) Expected output? (4) Edge cases?
9. Identify mock and stub requirements
10. Define test data strategy
11. Generate test plan document
12. Create directory structure: .propel/context/tasks/us_<ID>/unittest/
13. Write test_plan_<layer>_<descriptive_name>.md file
14. Validate test plan completeness
15. Report test plan generation summary
```

#### Error Handling and Recovery
**Common Error Scenarios:**
- **Missing User Story**: Request user to provide valid user story path or ID
- **Invalid US ID**: Validate US ID format and request correction
- **Inaccessible URL**: Request alternative source or local file
- **Empty/Invalid Content**: Ask for clarification or additional detail
- **No Implementation Tasks**: Generate basic test plan based on user story alone
- **Unknown Technology Stack**: Request user to specify testing framework

#### Output Confirmation
After successful test plan generation:
1. **User Story Summary**: Report which user story was analyzed
2. **Test Coverage Summary**: List total test cases generated by category
3. **Component Coverage**: Report components identified for testing
4. **File Confirmation**: Confirm test plan file created successfully
5. **Next Steps**: Suggest follow-up actions (implement tests, run coverage, etc.)

**Example Output Messages:**
- "Generated unit test plan for US-001 with 15 test cases covering 3 components"
- "Test plan created at .propel/context/tasks/us_001/unittest/test_plan_fe_login.md"
- "Identified Jest v29.7 as testing framework with mocking requirements for 4 dependencies"
- "Expected code coverage: 85% (12 test cases for acceptance criteria, 3 for edge cases)"


### Test Implementation Blueprint

#### Test File Location
- **Location**: `.propel/context/tasks/us_<ID>/unittest/`
- **Naming**: `test_<component_name>.<ext>` (e.g., `test_login_service.spec.ts`)

#### Mocking Strategy

| Dependency | Mock Type | Behavior | Return Value |
|------------|-----------|----------|--------------|
| [ServiceName] | mock/stub/spy | [When method called] | [Return or throw] |

#### Test Data

| Scenario | Input | Expected Output |
|----------|-------|-----------------|
| [Valid case] | `{ field: "value" }` | `{ result: "success" }` |
| [Edge case] | `{ field: "" }` | `Error: "Field required"` |

### Quality Assurance Framework

#### Test Plan Validation Checklist
Before completing test plan generation, validate:

**Coverage Validation:**
- [ ] All acceptance criteria have corresponding test cases
- [ ] All edge cases from user story are covered
- [ ] All error scenarios are tested
- [ ] All public methods/functions have test coverage
- [ ] All business logic branches are tested

**Test Design Validation:**
- [ ] Test cases are independent and isolated
- [ ] Test cases have clear Given/When/Then structure
- [ ] Assertions are specific and measurable
- [ ] Test data is realistic and representative
- [ ] Mocks are properly defined and scoped

**Technology Validation:**
- [ ] Testing framework version is pinned via Context7
- [ ] Test patterns match project conventions
- [ ] Test file locations follow project structure
- [ ] Naming conventions are consistent
- [ ] Framework-specific best practices are followed

**AI Component Validation (if AIR-XXX in scope):**
- [ ] LLM mocking strategy defined (GenericFakeChatModel or equivalent)
- [ ] Prompt construction tests designed
- [ ] Response parsing tests designed
- [ ] Guardrails test cases for input/output validation
- [ ] Fallback logic test cases for low-confidence scenarios
- [ ] Token budget enforcement tests
- [ ] Evaluation metrics defined for AI output quality

**Implementation Validation:**
- [ ] Test plan references implementation tasks
- [ ] Component paths are accurate
- [ ] Dependencies are correctly identified
- [ ] Mock requirements are documented
- [ ] Test execution order is defined

## Guardrails
- `rules/ai-assistant-usage-policy.md`: Explicit commands; minimal output
- `rules/code-anti-patterns.md`: Avoid god objects, circular deps, magic constants
- `rules/dry-principle-guidelines.md`: Single source of truth; delta updates
- `rules/iterative-development-guide.md`: Strict phased workflow
- `rules/language-agnostic-standards.md`: KISS, YAGNI, size limits, clear naming
- `rules/markdown-styleguide.md`: Front matter, heading hierarchy, code fences
- `rules/performance-best-practices.md`: Optimize after measurement
- `rules/security-standards-owasp.md`: OWASP Top 10 alignment
- `rules/software-architecture-patterns.md`: Pattern selection, boundaries
- `rules/unit-testing-standards.md`: Unit test plan scaffold **[CRITICAL]**

**>>> ALWAYS: Execute Quality Evaluation. Follow the 4-tier evaluation framework instructions to evaluate the outcomes. <<<**

## Quality Evaluation

- **Invoke**: `.windsurf/workflows/evaluate-output.md`
  - **$OUTPUT_FILE**: `.propel/context/tasks/us_XXX/unittest/test_plan_*.md`
  - **$SCOPE_FILES**: `.propel/context/tasks/us_XXX/us_XXX.md`
  - **--workflow-type**: `unit-test`

---

*This unit test plan generator ensures comprehensive test coverage with detailed test case design, proper mocking strategies, and technology-specific best practices for successful test-driven development.*