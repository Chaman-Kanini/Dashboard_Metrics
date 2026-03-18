# Architecture Design

## Project Overview
[short project description -- purpose, target users, and high-level capabilities]

## Architecture Goals
- [Architecture Goal #] : [Short description]

## Non-Functional Requirements
- NFR-001: System MUST [requirement derived from project needs]
- NFR-002: System MUST [requirement derived from project needs]
- NFR-003: System MUST [requirement derived from project needs]
- NFR-004: System MUST [requirement derived from project needs]
- NFR-005: [UNCLEAR] System MUST [ambiguous requirement needing clarification]

**Note**: Mark unclear requirements with [UNCLEAR] tag.

## Data Requirements
- DR-001: System MUST [data structure requirement]
- DR-002: System MUST [data integrity requirement]
- DR-003: System MUST [data retention requirement]
- DR-004: System MUST [data backup requirement]
- DR-005: System MUST [data migration requirement]
- DR-006: [UNCLEAR] System MUST [ambiguous requirement needing clarification]

**Note**: Mark unclear requirements with [UNCLEAR] tag.

## AI Consideration

**Status:** [Applicable / Not applicable]

**If Not Applicable (Deterministic Project):**
**Rationale:** No `[AI-CANDIDATE]` or `[HYBRID]` tags present in spec.md. Project follows deterministic architecture.

**If Applicable:** Proceed to AI Requirements section below.

## AI Requirements [CONDITIONAL: Only if AI Consideration = Applicable]
- AIR-001: System MUST [AI functional requirement]
- AIR-002: System MUST [AI quality requirement]
- AIR-003: [UNCLEAR] System MUST [ambiguous AI requirement needing clarification]

**Note:** Mark unclear requirements with [UNCLEAR] tag. Each AIR should trace to NFR. Include only if GenAI Fit Assessment ≥3.

### AI Architecture Pattern
**Selected Pattern:** [RAG / Tool Calling / Fine-tuning / Hybrid / N/A]

## Technology Stack
| Layer | Technology | Version | Justification (NFR/DR/AIR) |
|-------|------------|---------|----------------------------|
| Frontend | | | NFR-XXX |
| Backend | | | NFR-XXX |
| Database | | | DR-XXX |
| AI/ML | [Model Provider, Vector Store, Gateway] | [versions] | AIR-XXX |
| Testing | | | NFR-XXX |

**Note:** Derive from NFR/DR/AIR constraints above, not existing patterns. AI/ML row is conditional - include only if AIR-XXX requirements exist.

### Alternative Technology Options
- [Alternate technology stack considered with rationale for non-selection]

### Technology Stack Validation
- [Validation against NFR/DR/AIR constraints above]

### Technology Decision
| Metric (from NFR/DR/AIR) | Candidate 1 | Candidate 2 | Rationale |
|--------------------------|-------------|-------------|-----------|
| [NFR/DR/AIR-derived] | [score] | [score] | [why winner] |

### AI Component Stack [CONDITIONAL]
| Component | Technology | Purpose |
|-----------|------------|---------|
| Model Provider | [tech] | LLM inference |
| Vector Store | [tech] | Embedding storage & retrieval |
| AI Gateway | [tech] | Request routing, caching, logging |
| Guardrails | [tech] | Schema validation, content filtering |

## Technical Requirements
- TR-001: System MUST [technology choice justified by NFR-XXX/DR-XXX/AIR-XXX]
- TR-002: System MUST [architecture pattern justified by NFR-XXX]
- TR-003: System MUST [platform requirement justified by NFR-XXX]
- TR-004: System MUST [integration requirement]
- TR-005: [UNCLEAR] System MUST [ambiguous requirement needing clarification]

**Note**: Mark unclear requirements with [UNCLEAR] tag. Each TR should trace to NFR/DR/AIR.

## Domain Entities
- [Entity 1]: [What it represents, attributes, relationships]
- [Entity 2]: [What it represents, attributes, relationships]

**Note**: Include only if feature involves data

## Technical Constraints & Assumptions
- [List of technical constraints and assumptions]

## Development Workflow

1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Step 4]
5. [Step 5]
