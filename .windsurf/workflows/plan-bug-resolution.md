---
description: Performs comprehensive bug triage, root cause analysis, and generates fix implementation tasks with validation criteria
auto_execution_mode: 1
---

# Bug Fix Task Generator with Triage
As a Senior Software Engineer specializing in debugging and system reliability, perform comprehensive bug triage and generate actionable fix tasks based on the provided bug report.

## Input Parameter: $ARGUMENTS (Mandatory)
**Accepts:** Bug report file | Bug URL | Issue description | Error log

**Optional Parameters:**
- `--skip-history`: Skip git history analysis and findings registry lookup for faster execution (default: false)

## Output
- Artifact generation: `/.propel/context/tasks/bug_<ID>/task_*.md`
- Print the following: 
    - List of rules used by the workflow in bulleted format
    - Evaluation Scores in tabular format with average score. 
    - Evaluation summary (less than 100 words).
    **Do not save as file.**

**Note:**
- **File Handling**: IF file exists → UPDATE changed sections only (delta mode). IF file does not exist → CREATE complete file.
- Always generate a single unified bug task document.
- Generate the output using the .propel/templates/issue-triage-template.md template.

### Output Specifications

**Bug with ID Found**:
- **Directory**: `/.propel/context/tasks/bug_<ID>/` 
- **File Pattern**: `task_<seqnum>_fix_<descriptive_name>.md`
- **Example**: `/.propel/context/tasks/bug_042/task_001_fix_login_error.md`

**No Bug ID (Fallback)**:
- **Directory**: `/.propel/context/tasks/bug_<short_descriptive_name>`
- **File Pattern**: `task_<seqnum>_fix_<descriptive_name>.md`
- **Example**: `/.propel/context/tasks/bug_validation_error/task_001_fix_validation_error.md`

**Sequence Number Logic**:
- Auto-increment within target directory (bug folder or root)
- Use zero-padded 3-digit format (001, 002, 003...)
- Continue from highest existing number in directory
- Descriptive name should reflect the bug being fixed

**Compatibility**: Generated tasks must be executable via `/execute-task` command

### Directory Management

**Bug ID Extraction Priority**:
1. **Parse Input**: Extract bug ID using patterns above
2. **Validate Format**: Ensure valid bug ID format
3. **Create Directory**: `/.propel/context/tasks/bug_<ID>/` if ID found
4. **Fallback**: Use `/.propel/context/tasks/bug_<short_descriptive_name>` if no ID extracted

**Supported Bug ID Formats**:
- `bug_XXX` or `BUG-XXX` (3-4 digits)
- `issue_XXX` or `ISSUE-XXX` (3-5 digits)
- `#XXX` (GitHub/GitLab style)
- JIRA format: `PROJECT-XXX`
- Custom patterns from bug tracking systems

**Directory Examples**:
```
.propel/context/tasks/
+-- bug_042/
|   +-- bug_report.md
|   +-- task_001_fix_login_error.md
|   +-- task_002_add_regression_tests.md
+-- bug_general_error/
    +-- task_001_fix_general_error.md
```

## Core Principles
- **Root Cause Focus**: Address underlying cause, not just symptoms
- **Multi-Hypothesis Analysis**: Identify 3+ potential causes before committing
- **Regression Prevention**: Document risks and create tests to prevent recurrence

## Execution Flow

### Delta Processing Protocol
**Before generating any output:**
1. Check if target output file (`task_<seqnum>_fix_<name>.md`) already exists
2. If EXISTS: Read current content, identify only sections requiring update, EDIT those sections only
3. If NOT EXISTS: Generate complete new file
4. Log: "Mode: [Delta update to X sections | New file creation]"

### 1. Bug Triage Protocol

Execute comprehensive triage before creating any bug fixing tasks:

#### 1. Issue Reproduction & Verification
- Parse bug report for reproduction steps and environment details
- Search codebase for error messages using Grep tool
- Examine relevant files with Read tool
- Execute reproduction steps with Bash tool (if runnable commands provided)
- Capture stack traces and error logs
- Verify issue exists in latest codebase version

#### 2. Root Cause Analysis (use Sequential-Thinking MCP)
- Use `mcp__sequential-thinking__sequentialthinking` to trace error through codebase
- For root cause, answer: (1) What is the immediate trigger? (2) What is the underlying cause? (3) Why wasn't this caught earlier?
- Analyze git history for root cause (skip with --skip-history):
  - `git log --oneline -10 -- <affected_file>` - Last 10 changes only
  - `git log --grep="fix" --oneline -5 -- <affected_file>` - Last 5 bug fixes only
  - If >2 "fix" commits found, flag as **Recurring Issue Hotspot**
  - **Git Fallback** (if git unavailable or commands fail): Skip git history, proceed with registry lookup."
- **Registry Lookup** (skip with --skip-history): Grep `.propel/learnings/findings-registry.md` for affected file (selective read)
- Review component dependencies and interactions
- Identify regression source if applicable
- Document root cause with specific file:line references

#### 3. Impact Assessment
- Determine affected features and user workflows
- Evaluate data integrity implications
- Assess security and performance impacts
- Calculate affected user percentage
- Check for similar issues in related components

#### 4. Priority Categorization
- **Critical**: System down, data loss, security breach
- **High**: Core feature broken, major UX degradation
- **Medium**: Minor features affected, workarounds exist
- **Low**: Cosmetic issues, rare edge cases

#### 4a. AI Component Bug Analysis [CONDITIONAL: If affected code touches AIR-XXX components]

**AI Bug Detection Gate:**
```
Grep("langchain|openai|anthropic|embedding|vector|prompt|llm|rag", affected_files) → ai_indicators
IF ai_indicators.count > 0 → Apply AI Bug Investigation
```

**If AI components affected:**
- **Check model version**: Has the model version or configuration changed?
- **Verify prompt templates**: Have prompt templates been modified recently?
- **Test with fixed seed/temperature**: Reproduce with deterministic settings if possible
- **Review retrieval quality metrics**: For RAG issues, check relevance scores
- **Check for training data changes**: Any updates to embeddings or knowledge base?
- **Verify guardrails configuration**: Are input/output validators working correctly?
- **Token budget analysis**: Is the issue related to truncation or token limits?
- **Rate limit status**: Check if model provider rate limits are affecting behavior
- **Fallback logic verification**: Is the fallback path working when expected?

**AI-Specific Root Causes to Consider:**
- Model provider API changes or deprecations
- Embedding model version mismatch
- Vector store index corruption or staleness
- Prompt injection or jailbreak attempts
- Guardrails false positives/negatives
- Token counting errors leading to truncation
- Concurrent request race conditions in AI gateway

#### 5. Solution Validation
- Research similar fixes in git history using Bash
- Consider multiple solution approaches before settling on one
- List potential side effects: (a) What other code paths are affected? (b) What regressions are possible?
- Identify edge cases the fix must handle: boundary values, null inputs, concurrent access
- Use Context7 MCP (`mcp__context7__resolve-library-id` and `mcp__context7__get-library-docs`) for framework-specific or technology-specific solutions
- Avoid referencing libraries or patterns incompatible with the project's tech stack
- Validate approach with code examples from trusted sources
- Evaluate multiple solution approaches with deep consideration
- Define rollback procedure: (1) How to detect fix failure? (2) Steps to revert? (3) Data recovery needed?
- Estimate complexity and regression risk
- Specify validation criteria for successful fix

### Fix Task Generation

#### Task Structure Requirements

**CRITICAL: Before writing the fix task, enumerate the fix strategy:**

**Step 1 - List Fix Components:**
List all components of the fix with a one-line rationale for each:

| Fix Component | Type | Rationale |
|---------------|------|-----------|
| [Component 1] | [Code change / Test / Config] | [Why needed] |
| [Component 2] | [Code change / Test / Config] | [Why needed] |

**Step 2 - Expand Fix Task:**
Now generate the complete fix task with:
- Base task structure on `.propel/templates/issue-triage-template.md`
- Include complete triage summary in task description
- Define clear, sequential fix implementation steps
- Specify regression test requirements
- Include rollback procedures and validation checkpoints

#### Context Documentation Requirements

*** 1. Essential Bug Context Package ***
- **Triage Results**: Complete reproduction steps and root cause analysis
- **Technical Investigation**: Error traces, affected components, dependency analysis
- **Fix Strategy**: Solution approach with implementation examples from research
- **Validation Plan**: Testing requirements, regression prevention measures

*** 2. Framework Research Integration ***
- **Version Pinning**: Use `mcp__context7__resolve-library-id` to identify exact library versions
- **Implementation Patterns**: Use `mcp__context7__get-library-docs` for bug fix patterns and best practices
- **Error Handling**: Include framework-specific error handling approaches
- **Testing Strategies**: Framework-appropriate testing and validation methods

#### Quality Assurance Framework

*** 1. Pre-Delivery Checklist ***
- [ ] **Bug ID Extraction**: Attempted to extract bug ID from input
- [ ] **Folder Structure**: Created appropriate bug_XXX folder or used fallback to /.propel/context/tasks/
- [ ] **Root Cause Analysis Complete**: Answered (1) immediate trigger, (2) underlying cause, (3) why not caught earlier
- [ ] **Edge Case Analysis**: Listed all edge cases and related issues
- [ ] **Issue Reproduction**: Bug successfully reproduced and documented
- [ ] **Root Cause Verified**: Technical cause identified with code references
- [ ] **Impact Assessment**: Complete evaluation of affected systems
- [ ] **Priority Assignment**: Correct categorization based on business impact
- [ ] **Solution Validation**: Approach verified through research and analysis
- [ ] **Regression Tests**: Testing strategy defined for preventing recurrence
- [ ] **Task Executability**: Generated task is compatible with execute-task command
- [ ] **Context Completeness**: All necessary implementation context included
- [ ] **Framework Research**: Version-specific documentation and patterns included
- [ ] **Rollback Plan**: Clear reversion procedure documented

## Guardrails
- `rules/ai-assistant-usage-policy.md`: Explicit commands; minimal output
- `rules/code-anti-patterns.md`: Avoid god objects, circular deps, magic constants **[CRITICAL]**
- `rules/dry-principle-guidelines.md`: Single source of truth; delta updates **[CRITICAL]**
- `rules/iterative-development-guide.md`: Strict phased workflow
- `rules/language-agnostic-standards.md`: KISS, YAGNI, size limits, clear naming **[CRITICAL]**
- `rules/markdown-styleguide.md`: Front matter, heading hierarchy, code fences
- `rules/performance-best-practices.md`: Optimize after measurement
- `rules/security-standards-owasp.md`: OWASP Top 10 alignment
- `rules/software-architecture-patterns.md`: Pattern selection, boundaries

### Extended Standards (apply based on task domain)
- `rules/code-documentation-standards.md`: Comment WHY, not WHAT
- `rules/react-development-standards.md`: React component patterns
- `rules/typescript-styleguide.md`: TypeScript typing & consistency
- `rules/web-accessibility-standards.md`: WCAG 2.2 AA validation
- `rules/backend-development-standards.md`: Service/controller patterns
- `rules/frontend-development-standards.md`: Frontend patterns
- `rules/ui-ux-design-standards.md`: Layout/interaction standards
- `rules/database-standards.md`: Schema/migration standards
- `rules/stored-procedure-standards.md`: Stored procedure patterns
- `rules/dotnet-architecture-standards.md`: .NET architecture patterns

**Selection**: Apply only standards matching task domain. Most specific overrides general.

**>>> ALWAYS: Execute Quality Evaluation. Follow the 4-tier evaluation framework instructions to evaluate the outcomes. <<<**

## Quality Evaluation

- **Invoke**: `.windsurf/workflows/evaluate-output.md`
  - **$OUTPUT_FILE**: `.propel/context/tasks/bug_*/task_*.md`
  - **$SCOPE_FILES**: `[bug report]`
  - **--workflow-type**: `bug-task`

---