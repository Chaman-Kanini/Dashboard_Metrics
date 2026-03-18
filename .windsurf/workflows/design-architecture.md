---
description: Generates comprehensive design documents including NFR, TR, DR requirements, architecture patterns, technology stack validation, and cross-cutting concerns.
auto_execution_mode: 1
---

# Design Architecture Generator

As an expert Software Architect, generate comprehensive design documents including Non-Functional Requirements (NFR-XXX), Technical Requirements (TR-XXX), and Data Requirements (DR-XXX). This workflow focuses on architectural decisions, technology stack validation, and cross-cutting concerns.

## Input Parameter (Feature file): $ARGUMENTS (Optional)
Read the feature file first to understand what needs to be created, how the examples provided help, and any other considerations.

**Note:** Refer to '.propel/context/docs/spec.md' or '.propel/context/docs/codeanalysis.md' file if argument is not passed

### Input Processing Instructions
**CRITICAL**: Before proceeding with design generation, you MUST determine input type and process accordingly:

#### Input Type Detection
1. **File Path Detection**: Check if `$ARGUMENTS` contains a file path (contains file extensions .md, .txt)
2. **Default Fallback**: If `$ARGUMENTS` is empty, refer to `.propel/context/docs/spec.md` or `.propel/context/docs/codeanalysis.md`

#### File Input Processing
If `$ARGUMENTS` is a file path:
1. Verify file exists and read contents (supports .md, .txt)
2. Validate content contains relevant requirements

#### Default Input Processing
If `$ARGUMENTS` is not provided:
1. Look for `.propel/context/docs/spec.md` first
2. Fallback to `.propel/context/docs/codeanalysis.md` if spec.md doesn't exist

#### Fallback Handling
- If file cannot be read: Request alternative file path
- If no requirements found: Request specification file or text

## Output
- Artifact generation: `.propel/context/docs/design.md`
- Print the following:
  - List of rules used by the workflow in bulleted format
  - List of unclear technical understanding in bulleted format
  - Evaluation Scores in tabular format with average score.
  - Evaluation summary (less than 100 words).
  **Do not save as file.** (console output only)

**Note:**
- **File Handling**: IF file exists → UPDATE changed sections only (delta mode). IF file does not exist → CREATE complete file.
- Always create the output file in manageable smaller chunks to manage memory and processing constraints.
- Always generate a single unified document.
- Generate the output using the `.propel/templates/design-specification-template.md` template.
- design.md structure is defined by the referenced template. Populate all template sections. AI-related sections are CONDITIONAL per GenAI Fit Assessment.

## Essential Project Intelligence

### Reference Materials Integration
- **Existing Codebase**: Analyze `app`, `client`, `backend`, `server`, custom folders for current implementation patterns
- **Documentation Standards**: Follow existing documentation patterns and conventions
- **Design Specifications**: Reference `.propel/context/docs/spec.md` for requirements alignment

*** Comprehensive understanding of requirements and technical constraints is non-negotiable ***

### References Package
```yaml
- url: [Framework/library documentation URL]
  section: [Architecture constraints and capabilities]
  critical: [Key limitations affecting design]

- file: [existing/feature/path]
  why: [Current implementation to maintain compatibility]
```

## Execution Flow

### 1. Core Principles
- Understanding the requirements, is mandatory
- Understanding the existing codebase, if available, is mandatory.
- Analyze deeply and systematically plan your approach

### 2. Research Process
During the research process, deeper research we do here the better the design will be. We optimize for chance of success and not for speed.

**CRITICAL: Follow steps in exact sequence to prevent bias toward existing patterns.**

1. **Requirements-First Analysis** (Technology-Neutral)
   - Extract NFR constraints from input spec BEFORE looking at existing code
   - Document: concurrent users, response time SLA, data volume, compliance, team expertise, budget
   - Output: Technology-neutral constraint list for evaluating candidates

2. **GenAI Fit Assessment** (Before Technology Discovery)

   **Always:** Evaluate AI suitability BEFORE technology selection to avoid bias.

   **Step 1: Check for Upstream AI Tags from spec.md**
   ```
   Grep("[AI-CANDIDATE]", ".propel/context/docs/spec.md") → ai_candidate_count
   Grep("[HYBRID]", ".propel/context/docs/spec.md") → hybrid_count
   ```

   **Upstream Tag Detection:**
   - IF `ai_candidate_count + hybrid_count > 0` → Upstream tagged AI features, PROCEED with AI assessment
   - IF `ai_candidate_count + hybrid_count = 0` → No AI tags present (deterministic project), SKIP AI sections

   **When No AI Tags Found (Deterministic Project):**
   Document in design.md:
   ```markdown
   ## AI Consideration
   **Status:** Not applicable
   **Rationale:** No `[AI-CANDIDATE]` or `[HYBRID]` tags present in spec.md. Project follows deterministic architecture.
   ```
   Then SKIP to Step 3 (External Research), bypassing all AI-related sections.

   **Step 2: AI Fit Classification** (Only if AI tags found)
   For each major feature/capability from requirements:

   **AI Fit Classification Table:**
   | Feature | AI Fit Score (1-5) | Classification | Rationale |
   |---------|-------------------|----------------|-----------|
   | [feature from spec] | [score] | [HIGH-FIT/LOW-FIT/HYBRID] | [reason] |

   **Scoring Guide:**
   | Score | Classification | Indicators |
   |-------|---------------|------------|
   | 4-5 | HIGH-FIT | NLU, Q&A over docs, content generation, extraction, conversational |
   | 2-3 | HYBRID | Needs both AI + deterministic (AI assists, rules decide) |
   | 1-2 | LOW-FIT | Compliance traceability, exact calculations, <200ms latency, no grounding |

   **Decision Gate:**
   - IF any feature scores 4-5 → PROCEED with AI Requirements section
   - IF all features score 1-2 → SKIP AI sections, document: "AI consideration: Not applicable. Rationale: [X]"
   - IF mixed scores → Generate HYBRID architecture

3. **External Research (via Sequential-thinking MCP)**

   **Fallback Mechanism:** If the sequential-thinking MCP tool fails or is unavailable, automatically fall back to standard iterative analysis approach using Web fetch:
   - Perform systematic step-by-step design analysis
   - Use structured thinking with explicit validation checkpoints
   - Apply the same comprehensive methodology without the sequential-thinking tool
   - Ensure no degradation in analysis quality or completeness

   **Research Areas:**
   - Use Context7 MCP to pull official docs (GitHub, frameworks, libraries)
   - Search the web for recent articles, guides, and community discussions
   - Identify and analyze well-regarded open source projects that demonstrate the practices
   - Look for style guides, conventions, and standards from respected organizations
   - Prioritize official documentation and widely-adopted standards
   - Consider the recency of information (prefer current practices over outdated ones)
   - Look for popular repositories on GitHub that exemplify good practices

   **Technology Discovery:** For each category (database, backend, frontend, architecture, **AI infrastructure if AIR-XXX exists**), identify 2-3 candidates from research. Do NOT assume existing codebase technology is "primary".

   **AI Technology Discovery** [CONDITIONAL: If GenAI Fit ≥3]
   | Category | Candidates | Evaluation Criteria |
   |----------|------------|---------------------|
   | Model Provider | [e.g., OpenAI, Anthropic, Azure OpenAI] | Cost, latency, context window, compliance |
   | Vector Store | [e.g., pgvector, Pinecone, Azure AI Search] | Scale, filtering, hybrid search |
   | AI Gateway | [e.g., Custom, LiteLLM, Portkey] | Routing, caching, observability |
   | Embedding Model | [e.g., text-embedding-3-small, Cohere] | Dimensions, cost, multilingual |

4. **Technology Selection**
   - Score each candidate against NFR constraints (weighted 1-5, score 0-10)
   - Winner = highest weighted total

5. **Codebase Compatibility** (if existing code - AFTER selection)
   - If recommended DIFFERS from existing: document migration complexity and recommendation
   - If recommended MATCHES existing: explicitly confirm NFR-driven, not bias
   - Note existing conventions for compatibility

6. **Requirements Generation**

   Generate the following requirement types that inform architectural decisions:

   **CRITICAL: Before writing any detailed requirements, list all items to generate:**

   **Step 1 - Enumerate First:**
   Create a table listing all NFR/TR/DR/AIR requirements you will generate with a one-line rationale for each:

   | Req-ID | Type | Summary | Rationale |
   |--------|------|---------|-----------|
   | NFR-001 | Performance | Response time < 2s | User experience SLA |
   | TR-001 | Technology | PostgreSQL 14+ | ACID compliance needed |
   | DR-001 | Data | User entity | Core domain object |
   | AIR-001 | AI (if applicable) | RAG pattern | Q&A over docs |

   **Step 2 - Expand Each:**
   Now expand each requirement listed above with full specification.

   **Non-Functional Requirements (NFR-XXX)**
   Generate requirements for:
   - **Performance**: Response times, throughput, resource usage (NFR-001, NFR-002...)
   - **Security**: Encryption, authentication, authorization, data protection
   - **Availability**: Uptime targets, disaster recovery, failover
   - **Scalability**: Concurrent users, data volume, growth projections
   - **Reliability**: Error rates, mean time between failures
   - **Maintainability**: Code quality, documentation, upgrade paths

   **Technical Requirements (TR-XXX)**
   Generate requirements for:
   - **Technology Choices**: Database, frameworks, runtime environments (TR-001, TR-002...)
   - **Architecture Patterns**: RESTful APIs, microservices, event-driven
   - **Platform Requirements**: Containerization, cloud deployment, on-premise
   - **Integration Requirements**: OAuth, third-party APIs, message queues
   - **Development Standards**: Code style, testing frameworks, CI/CD

   **Data Requirements (DR-XXX)**
   Generate requirements for:
   - **Data Structures**: Entity definitions, relationships, unique identifiers (DR-001, DR-002...)
   - **Data Integrity**: Referential integrity, validation rules, constraints
   - **Data Retention**: Audit logs, archival policies, compliance periods
   - **Data Backup**: Backup frequency, point-in-time recovery, disaster recovery
   - **Data Migration**: Schema versioning, zero-downtime migrations

   **AI Requirements (AIR-XXX)** [CONDITIONAL: Only if GenAI Fit ≥3]

   Generate requirements using existing format:

   **AI Functional Requirements:**
   - AIR-001: System MUST generate [output] from [inputs] using [pattern: RAG/Tool/Fine-tune]
   - AIR-002: System MUST provide source citations for generated content (if RAG)
   - AIR-003: System MUST fallback to [deterministic flow] when confidence < [threshold]

   **AI Quality Requirements:**
   - AIR-Q01: System MUST maintain hallucination rate below [X]% on evaluation set
   - AIR-Q02: System MUST achieve [latency] p95 for AI responses
   - AIR-Q03: System MUST enforce output schema validity ≥ [X]%

   **AI Safety Requirements:**
   - AIR-S01: System MUST redact PII from prompts before model invocation
   - AIR-S02: System MUST enforce document ACL filtering in retrieval (if RAG)
   - AIR-S03: System MUST log all prompts/responses for audit (with retention: [period])

   **AI Operational Requirements:**
   - AIR-O01: System MUST enforce token budget of [N] per request
   - AIR-O02: System MUST implement circuit breaker for model provider failures
   - AIR-O03: System MUST support model version rollback within [time]

   **RAG Pipeline Requirements** [CONDITIONAL: If RAG pattern selected]
   - AIR-R01: System MUST chunk documents into [N] token segments with [X]% overlap
   - AIR-R02: System MUST retrieve top-[K] chunks with similarity ≥ [threshold]
   - AIR-R03: System MUST re-rank using [strategy: semantic/MMR/hybrid]

   **Requirement Format:**
   ```markdown
   - NFR-001: System MUST [performance requirement, e.g., "respond to user requests within 2 seconds"]
   - TR-001: System MUST [technology choice, e.g., "use PostgreSQL 14+ as the primary database"]
   - DR-001: System MUST [data structure, e.g., "store user profiles with email as unique identifier"]
   - AIR-001: System MUST [AI requirement, e.g., "generate responses using RAG pattern"]
   ```

   **Note:** Mark unclear requirements with [UNCLEAR] tag for later clarification. Each AIR traces to NFR for justification.

7. **User Clarification** (if needed)
   - Specific patterns to mirror and where to find them?
   - Integration requirements and where to find them?

### 3. Technical Design Considerations
- Architectural patterns to follow
- Technology stack considerations
   - Multi-Tier Requirements
      - **Frontend Requirements**: UI/UX, client-side functionality, responsive design
      - **Backend Requirements**: Business logic, API design, data processing
      - **Database Requirements**: Data models, queries, performance optimization
      - **Infrastructure Requirements**: Deployment, monitoring, scaling strategies
   - Cross-Cutting Concerns
      - **Security Requirements**: Authentication, authorization, data protection
      - **Performance Requirements**: Response times, throughput, resource usage
      - **Monitoring Requirements**: Logging, metrics, alerting, observability
      - **Compliance Requirements**: Regulatory standards, audit trails, data governance

### 4. Design Document Structure
**Document in design.md** (per design-specification-template.md):
- Project Overview with purpose, target users, capabilities
- Architecture Goals with numbered descriptions
- Non-Functional Requirements (NFR-XXX) — **drives technology selection**
- Data Requirements (DR-XXX) — **drives technology selection**
- AI Requirements (AIR-XXX) [CONDITIONAL] — **drives AI architecture selection**
- AI Architecture Pattern [CONDITIONAL: If AIR-XXX exists]
- Technology Stack (derived from NFR/DR/AIR above)
- Alternative Technology Options
- Technology Decision (includes AI Component Stack if applicable)
- Technical Requirements (TR-XXX) with NFR/DR/AIR justification
- Domain Entities (what they represent, attributes, relationships)
- Technical Constraints and Assumptions
- Development Workflow steps

### AI Architecture Pattern [CONDITIONAL: If AIR-XXX exists]

**Pattern Selection Matrix:**
| Pattern | Select When | Avoid When |
|---------|-------------|------------|
| **RAG** | Q&A over docs, dynamic knowledge, citation needed | No grounding data, exact calculations |
| **Tool Calling** | API actions, data fetch, system integration | Pure content generation |
| **Fine-tuning** | Consistent terminology, stable domain knowledge | Rapidly changing data |
| **Hybrid** | Complex workflows, RAG + actions | Simple single-pattern cases |

**Selected Pattern:** [RAG / Tool Calling / Fine-tuning / Hybrid]
**Rationale:** [Justify based on AIR-XXX requirements]

### 5. Design Generation
- Read template from `.propel/templates/design-specification-template.md`
- Populate template with the findings
- Use Write tool to create an artifact `.propel/context/docs/design.md`
- Ensure all template sections are populated with real data

### 6. Summary Presentation
- Present executive summary to user
- Highlight critical findings and recommendations
- Provide link to detailed report in `.propel/context/docs/design.md`
- Present the Quality Assessment metrics

**Design Validation (use sequential thinking MCP if available):**
- Validate research completeness before design generation
- Create and verify design hypothesis
- Ensure architectural decisions align with requirements
- **Fallback**: Create explicit validation checklist and document decision rationale

### Critical Context to Include
- **Documentation**: URLs with specific sections
- **Design**: Architecture and design considerations
- **Code Examples**: Real snippets from codebase
- **Guidelines**: Library quirks, version issues
- **Patterns**: Existing approaches to follow

### Implementation Blueprint
- Start with pseudocode showing approach
- Reference real files for patterns
- Include error handling strategy

## Guardrails
- `rules/ai-assistant-usage-policy.md`: Explicit commands; minimal output
- `rules/code-anti-patterns.md`: Avoid god objects, circular deps, magic constants
- `rules/dry-principle-guidelines.md`: Single source of truth; delta updates
- `rules/iterative-development-guide.md`: Strict phased workflow
- `rules/language-agnostic-standards.md`: KISS, YAGNI, size limits, clear naming
- `rules/markdown-styleguide.md`: Front matter, heading hierarchy, code fences
- `rules/performance-best-practices.md`: Optimize after measurement
- `rules/security-standards-owasp.md`: OWASP Top 10 alignment **[CRITICAL]**
- `rules/software-architecture-patterns.md`: Pattern selection, boundaries **[CRITICAL]**
- `rules/uml-text-code-standards.md`: PlantUML/Mermaid notation standards **[CRITICAL]**

**>>> ALWAYS: Execute Quality Evaluation. Follow the 4-tier evaluation framework instructions to evaluate the outcomes. <<<**

## Quality Evaluation

- **Invoke**: `.windsurf/workflows/evaluate-output.md`
  - **$OUTPUT_FILE**: `.propel/context/docs/design.md`
  - **$SCOPE_FILES**: `.propel/context/docs/spec.md`
  - **--workflow-type**: `design`

---

*This design architecture generator ensures comprehensive NFR/TR/DR requirements with technology stack validation and architectural decisions for successful implementation.*