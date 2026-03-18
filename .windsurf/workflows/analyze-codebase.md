---
description: Entry point for comprehensive codebase analysis. Validates input and delegates complex analysis to the specialized code-analyzer agent for architectural insights and strategic recommendations.
auto_execution_mode: 1
---

# Codebase Analysis Command
As a solution architect, perfrom a structured codebase analysis covering: architecture patterns, security posture, performance characteristics, data model, and integration topology. Provides actionable insights and strategic recommendations for technical debt reduction and system improvement.

## Input Parameters: $ARGUMENTS (Optional)
**Accepts:** Repository URL | Folder Path | Root path | Technology stack | Business domain | Analysis depth

**Default Parameters:**
- `repo_url`: Current directory or provided Git URL
- 'Folder_path': Source code directory
- `root_path`: "." (current directory)
- `primary_stack`: Auto-detected from codebase
- `business_domain`: "General business application"
- `analysis_depth`: "comprehensive" (or "standard", "quick")
- `time_budget_minutes`: 60
- `priority_areas`: "architecture, security, performance, data model, integrations"

## Output
- Artifact generation: `.propel/context/docs/codeanalysis.md`
- Print the following: 
  - List of rules used by the workflow in bulleted format
  - Evaluation Scores in tabular format with average score. 
  - Evaluation summary (less than 100 words).
  **Do not save as file.**

**Note:**
- **File Handling**: IF file exists → UPDATE changed sections only (delta mode). IF file does not exist → CREATE complete file.
- Always create the output file in manageable smaller chunks to manage memory and processing constraints.
- Always generate a single unified document.
- Generate the output using the .propel/templates/codebase-analysis-template.md template.

## Core Principles
- **Comprehensive Discovery**: Document all architectural patterns, anti-patterns, and system topology
- **Evidence-Based Analysis**: Every finding must reference specific files, patterns, or metrics
- **Actionable Recommendations**: Provide prioritized improvements with clear remediation steps

## Execution Flow

### 1. Parameter Validation
- Validate repository access and permissions
- Set default values for missing parameters
- Verify basic repository accessibility

### 2. Core Responsibilities

#### Deep Analysis (use sequential-thinking MCP)
- Perform stepwise reasoning through complex architectural decisions and patterns
- Trace system flows and business logic transformations methodically
- Build layered understanding of technology choices and their implications
- Develop causal chains linking architectural patterns to system behaviors and risks

**Primary Approach:**
```
mcp__sequential-thinking__sequentialthinking for step-by-step analysis:
- Architectural Patterns: Layered, Microservices, Event-Driven, Hexagonal, CQRS, MVC, MVP, MVVM
- Design Patterns: Singleton, Factory, Observer, Strategy, Repository, Unit of Work
- Anti-Patterns Detection: God objects, circular dependencies, tight coupling
- System Topology: Entry points, communication protocols, external integrations
- Use Case Discovery: Actors, goals, success scenarios from routes and business logic
```

**Fallback Strategy (if Sequential-thinking MCP fails):**
```
Manual structured analysis:

**Phase A: Architecture Pattern Discovery**
- Step 1: Identify directory structure and module organization
- Step 2: Map component relationships and dependencies  
- Step 3: Classify architectural style (monolith/microservices/etc.)

**Phase B: Design Pattern Recognition** 
- Step 1: Scan for common creational patterns (Factory, Builder, Singleton)
- Step 2: Identify behavioral patterns (Observer, Strategy, Command)
- Step 3: Find structural patterns (Adapter, Decorator, Repository)

**Phase C: Quality & Risk Assessment**
- Step 1: Calculate complexity metrics and identify God objects
- Step 2: Map circular dependencies and coupling issues
- Step 3: Document system entry points and data flow
```

**Before writing analysis findings, list all findings:**
| Category | Finding | Severity |
|----------|---------|----------|
| Architecture | ... | ... |
| Security | ... | ... |
| Performance | ... | ... |
**Now expand each finding listed above.**

**Business Logic Analysis**
- **Core Business Logic Discovery**: Identify classes/modules solving business problems
- **Method Analysis**: Document key methods and their business purpose
- **Business Rules Extraction**: Document enforced business rules
- **Process Flow Mapping**: Step-by-step business flow in plain English
- **Dependencies Mapping**: Track critical dependencies for business logic
- **User Persona Journey**: Identify the user persona journey for validation
- **Use Case Diagrams**: Generate PlantUML diagram for each discovered use case

**AI Component Analysis** [CONDITIONAL: If LLM/AI patterns detected]

**AI Detection Gate:**
```
Grep("langchain|openai|anthropic|llama|huggingface|vectorstore|embedding|rag|prompt" , "package.json|requirements.txt|*.csproj") → ai_indicators
IF ai_indicators.count > 0 → Execute AI Component Analysis
```

**If AI components detected:**
- **LLM Integration Patterns**: SDK usage, streaming, rate limiting, error handling
- **RAG Pipeline Topology**: Document chunking, embedding models, retrieval strategies
- **Prompt Template Catalog**: System prompts, user prompts, versioning approach
- **Guardrails Implementation**: Input sanitization, output validation, schema enforcement
- **Token/Cost Tracking**: Budget enforcement, usage monitoring, cost attribution
- **Vector Store Configuration**: Index type, dimensions, similarity metrics
- **AI Gateway/Router**: Load balancing, caching, fallback strategies
- **Model Versioning**: How model versions are tracked and rolled back
- **Observability**: Prompt/response logging, evaluation metrics, A/B testing

**AI Security Assessment** (if AI detected):
- Prompt injection vulnerabilities
- Jailbreak prevention mechanisms
- PII handling in prompts/responses
- Document-level ACL in RAG pipelines
- Model provider credential management

**Quality Assessment & Risk Analysis**
- **Code Quality Metrics**: Cyclomatic complexity, code duplication, technical debt
- **OWASP Top 10 Compliance Assessment**:
  - A01:2021 - Broken Access Control
  - A02:2021 - Cryptographic Failures
  - A03:2021 - Injection
  - A04:2021 - Insecure Design
  - A05:2021 - Security Misconfiguration
  - A06:2021 - Vulnerable and Outdated Components
  - A07:2021 - Identification and Authentication Failures
  - A08:2021 - Software and Data Integrity Failures
  - A09:2021 - Security Logging and Monitoring Failures
  - A10:2021 - Server-Side Request Forgery (SSRF)


#### Technical Research (use Context7 MCP)
- Gather technology stack documentation and framework best practices simultaneously using Context7
- Map architectural patterns, anti-patterns, and structural metrics concurrently
- Understand PlantUML syntax for use case diagram generation 

**Primary Approach:**
```
For each detected technology/framework:
1. mcp__context7__resolve-library-id(libraryName: "technology-name")
2. mcp__context7__get-library-docs(context7CompatibleLibraryID: "resolved-id")
```

**Fallback Strategy (if Context7 MCP fails):**
```
WebSearch: "[technology] architecture best practices documentation"
WebSearch: "[framework] security vulnerabilities CVE"
Read: package.json (detect technology stack and versions)
Read: README.md (understand project structure and technologies)
Grep: "import.*|require.*|using.*" (identify framework usage patterns)
```

**Parallel Research Tasks:**
- **Package Managers**: package.json, pom.xml, build.gradle, go.mod, requirements.txt, Gemfile, *.csproj
- **Frameworks**: React, Angular, Vue, .NET, Spring, Django, Rails, Express
- **Build Tools**: Webpack, Vite, Maven, Gradle, MSBuild, Make
- **Container/Orchestration**: Dockerfile, docker-compose.yml, k8s/*, helm/*
- **IaC**: terraform/*, bicep/*, arm/*, cloudformation/*
- **CI/CD**: .github/workflows, azure-pipelines.yml, .gitlab-ci.yml, Jenkinsfile
- **Monorepo Detection**: nx.json, lerna.json, rush.json, turbo.json, pnpm-workspace.yaml

**Security & Performance Scanning**
```bash
# Parallel vulnerability scanning
npm audit --audit-level=moderate || true
dotnet list package --vulnerable --include-transitive || true
pip-audit || safety check || true

# Secret scanning
trufflehog filesystem . --json || true
gitleaks detect --source . || true
rg -n "(?i)(api[_-]?key|secret|password|token|private[_-]?key)" --glob "!*.lock" || true

# Performance metrics
npm run build -- --stats || webpack-bundle-analyzer || true
npx vite-bundle-visualizer || true
```

**Documentation & Test Coverage Extraction**
```bash
# Coverage analysis
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=opencover || true
npm test -- --coverage --coverageReporters=json-summary text lcov || true
pytest --cov=. --cov-report=json --cov-report=term || true
```

### 3. Analysis Generation
- Read template from `.propel/templates/codebase-analysis-template.md`
- Populate template with the findings
- Use Write tool to create an artifact `.propel/context/docs/codeanalysis.md`
- Ensure all template sections are populated with real data

### 4. Summary Presentation
- Present executive summary to user
- Highlight critical findings and recommendations
- Provide link to detailed report in `.propel/context/docs/codeanalysis.md`
- Present the Quality Assessment metrics

## Guardrails
- `rules/ai-assistant-usage-policy.md`: Explicit commands; minimal output
- `rules/code-anti-patterns.md`: Avoid god objects, circular deps, magic constants **[CRITICAL]**
- `rules/dry-principle-guidelines.md`: Single source of truth; delta updates
- `rules/iterative-development-guide.md`: Strict phased workflow
- `rules/language-agnostic-standards.md`: KISS, YAGNI, size limits, clear naming
- `rules/markdown-styleguide.md`: Front matter, heading hierarchy, code fences
- `rules/performance-best-practices.md`: Optimize after measurement
- `rules/security-standards-owasp.md`: OWASP Top 10 alignment **[CRITICAL]**
- `rules/software-architecture-patterns.md`: Pattern selection, boundaries **[CRITICAL]**
- `rules/uml-text-code-standards.md`: PlantUML/Mermaid notation standards

**>>> ALWAYS: Execute Quality Evaluation. Follow the 4-tier evaluation framework instructions to evaluate the outcomes. <<<**

## Quality Evaluation

- **Invoke**: `.windsurf/workflows/evaluate-output.md`
  - **$OUTPUT_FILE**: `.propel/context/docs/codeanalysis.md`
  - **$SCOPE_FILES**: `[existing codebase]`
  - **--workflow-type**: `codebase`

---