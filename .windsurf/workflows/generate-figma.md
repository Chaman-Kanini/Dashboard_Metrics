---
description: AI-assisted Figma artifact generation workflow that transforms screen specifications into production-ready Figma structures with component libraries, clickable prototypes organized by flow, and JPG exports.
auto_execution_mode: 1
---

# Generate Figma Artifacts

As a Senior Product Designer and Figma Specialist, build production-ready Figma design artifacts from specifications. Your output includes 7-page Figma structure, clickable prototypes organized by flow, and JPG exports.

## Input Parameters

### Primary Input (Required)
- `.propel/context/docs/figma_spec.md` - **PRIMARY** - Screen inventory, states, flows, components
- `.propel/context/docs/designsystem.md` - **READ ONLY** - Design tokens, branding, component specs

### Optional Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--app-name` | String | From figma_spec.md | Override application name |
| `--platform` | Enum | From figma_spec.md | `web` / `ios` / `android` / `responsive` |
| `--export-scale` | String | `2x` | JPG export scale |

### Input Validation
```
1. Check if figma_spec.md exists
   - IF NOT EXISTS -> EXIT with "figma_spec.md not found. Run create-figma-spec first."
2. Check if designsystem.md exists
   - IF NOT EXISTS -> EXIT with "designsystem.md not found. Run create-figma-spec first."
3. Validate figma_spec.md has required sections:
   - Screen Inventory
   - Prototype Flows
   - Component Requirements
4. ELSE -> Proceed with generation
```

## Output

### Artifact Generation
- `.propel/context/figma/figma_structure.json` - Figma-compatible JSON structure
- `.propel/context/figma/components/component_library.md` - Component specifications with variants
- `.propel/context/figma/exports/export_manifest.md` - JPG export list with naming

### Console Output (Do Not Save)
- List of rules used by the workflow in bulleted format
- Evaluation Scores in tabular format with average score
- Evaluation summary (less than 100 words)

**Note:**
- This workflow does NOT create or modify figma_spec.md or designsystem.md
- If these files need updates, run create-figma-spec workflow
- **File Handling**: IF file exists → UPDATE changed sections only (delta mode). IF file does not exist → CREATE complete file.

## Core Principles

### Read-Only Design System
- **NEVER** create or modify designsystem.md
- Read all tokens from designsystem.md
- Apply tokens consistently across all artifacts
- If tokens are missing, report error (do not generate defaults)

### Spec-Driven Generation
- **NEVER** derive screens - use Screen Inventory from figma_spec.md
- **NEVER** create flows - use Prototype Flows from figma_spec.md
- Build exactly what is specified, nothing more

### Flow-Organized Prototypes
- Organize prototypes BY FLOW NAME (not by persona)
- Include persona coverage as metadata per flow
- Wire flows exactly as defined in figma_spec.md

### Auto Layout First
- All frames MUST use Auto Layout
- No absolute positioning except overlays
- Use spacing tokens from designsystem.md consistently

## Execution Flow

### Phase 0: Input Validation
**Critical First Step - Validate Required Files Exist**

```
1. Read figma_spec.md
   - Extract app name, platform
   - Extract screen inventory
   - Extract prototype flows
   - Extract component requirements

2. Read designsystem.md
   - Extract color tokens
   - Extract typography tokens
   - Extract spacing tokens
   - Extract border radius tokens
   - Extract elevation/shadow tokens
   - Extract component specifications

3. Validate completeness
   - IF missing screens -> ERROR
   - IF missing flows -> ERROR
   - IF missing tokens -> ERROR
```

### Phase 1: Build Figma Structure
**Goal:** Create 7-page Figma file structure

```
00_Cover      - Project metadata from figma_spec.md
01_Foundations - Tokens from designsystem.md
02_Components  - Component library with variants
03_Patterns    - Reusable layout patterns
04_Screens     - All screens with all states (from figma_spec.md)
05_Prototype   - Interactive flows (from figma_spec.md)
06_Handoff     - Developer notes and specs
```

### Phase 2: Foundations (01_Foundations)
**Goal:** Document design tokens from designsystem.md

**Apply directly from designsystem.md:**
- **Colors:** Primary, Secondary, Semantic, Neutral scale
- **Typography:** Font families, size scale, weights, line-heights
- **Spacing:** Base unit, scale values
- **Border Radius:** Small, Medium, Large, Full
- **Elevation:** Levels 1-5 with shadow definitions

**Frame Sizes (from figma_spec.md or defaults):**
| Platform | Width | Height |
|----------|-------|--------|
| Mobile | 390px | 844px |
| Tablet | 768px | 1024px |
| Web | 1440px | 1024px |

### Phase 3: Component Library (02_Components)
**Goal:** Build components specified in figma_spec.md

**Read component requirements from figma_spec.md:**
- Build only specified components
- Apply variants as defined
- Use tokens from designsystem.md

**Naming Convention:** `C/<Category>/<Name>`

**Required States per Component:**
| State | Visual Treatment |
|-------|-----------------|
| Default | Base styling per design tokens |
| Hover | Subtle elevation/color shift |
| Focus | Visible outline (>=3:1 contrast) |
| Active | Pressed/depressed visual |
| Disabled | 40% opacity |
| Loading | Skeleton or spinner |

### Phase 4: Patterns (03_Patterns)
**Goal:** Build reusable patterns from components

Patterns based on screen requirements in figma_spec.md:
- Auth form pattern (if login screens exist)
- Search + filter pattern (if search screens exist)
- List + pagination pattern (if list screens exist)
- Error/Empty/Loading pattern blocks (required for all)

All patterns built from 02_Components using designsystem.md tokens.

### Phase 5: Build Screens (04_Screens)
**Goal:** Create all screens with all states from figma_spec.md

**For each screen in Screen Inventory:**
1. Create frames for ALL 5 states:
   - `<ScreenName>/Default`
   - `<ScreenName>/Loading`
   - `<ScreenName>/Empty`
   - `<ScreenName>/Error`
   - `<ScreenName>/Validation`

2. Apply from 01_Foundations:
   - Grid system
   - Design tokens
   - Spacing scale

3. Build from 02_Components and 03_Patterns

4. Use state specifications from figma_spec.md

### Phase 6: Prototype Flows (05_Prototype)
**Goal:** Wire clickable flows as defined in figma_spec.md

**For each flow in Prototype Flows section:**
1. Read flow definition:
   - Flow name
   - Personas covered (as metadata)
   - Screen sequence
   - Interactions required

2. Wire screens in sequence:
   - Entry point -> Steps -> Exit conditions
   - Decision points with branches
   - Error paths

3. Document flow metadata:
   ```
   Flow: [Flow Name]
   Personas: [List from figma_spec.md]
   Screens: [Count]
   Interactions: [Count]
   ```

**Overlay Usage:**
| Element | Type | Animation |
|---------|------|-----------|
| Modal | Centered | Fade + scale |
| Drawer | Edge | Slide |
| Toast | Fixed | Slide + fade |
| Bottom Sheet | Bottom | Slide |

### Phase 7: Handoff (06_Handoff)
**Goal:** Generate developer documentation

**Documentation Sections:**
1. **Token Usage Rules**: From designsystem.md
2. **Component Usage**: Props, variants, usage guidelines
3. **Responsive Behavior**: Breakpoint changes
4. **Edge Cases**: Max content, truncation, overflow
5. **Accessibility Notes**: Focus order, ARIA requirements
6. **Screen-to-Code Mapping**: Reference figma_spec.md screen IDs

### Phase 8: Export Specifications
**Goal:** Generate export manifest for JPG exports

**Export Settings:**
| Setting | Value |
|---------|-------|
| Format | JPG (JPEG) |
| Quality | High (85%) |
| Scale - Mobile | 2x |
| Scale - Web | 2x |
| Color Profile | sRGB |

**Naming Convention:**
`<AppName>__<Platform>__<ScreenName>__<State>__v1.jpg`

**Generate export_manifest.md:**
- List all screens x states
- Full file paths
- Dimensions
- Export timestamp

## Guardrails
- `rules/figma-design-standards.md`: File structure, Auto Layout, components, exports **[CRITICAL]**
- `rules/ui-ux-design-standards.md`: Design tokens, component states **[CRITICAL]**
- `rules/web-accessibility-standards.md`: WCAG 2.2 AA, keyboard nav, contrast **[CRITICAL]**
- `rules/ai-assistant-usage-policy.md`: Explicit commands; minimal output
- `rules/dry-principle-guidelines.md`: Single source of truth; delta updates
- `rules/markdown-styleguide.md`: Front matter, heading hierarchy

**>>> ALWAYS: Execute Quality Evaluation. <<<**

## Quality Evaluation

### 4-Tier Figma Artifact Assessment

| Tier | Dimension | Gate | Conditional |
|------|-----------|------|-------------|
| T1 | Figma Structure (7 pages) + Spec Compliance | MUST PASS / MUST=100% | No (always required) |
| T2 | Token Application + Component Coverage | ≥80% | No (always required) |
| T3 | Screen State Coverage (5 states/screen) | ≥80% | Yes (skip if --states=minimal) |
| T4 | Flow Implementation | ≥80% | Yes (skip if no FL-XXX in spec) |

### Tier Definitions

**T1 - Structure & Spec Compliance (REQUIRED)**
- Figma file must have all 7 pages (00_Cover through 06_Handoff)
- All screens from figma_spec.md must be generated in 04_Screens
- SCR-XXX IDs must match between spec and output
- Gate: Structure MUST PASS, Spec MUST=100%

**T2 - Tokens & Components (REQUIRED)**
- Design tokens from designsystem.md applied consistently
- All specified components built in 02_Components
- Component variants and states documented
- Gate: ≥80% aggregate

**T3 - Screen State Coverage (CONDITIONAL)**
- Skip Condition: --states=minimal flag provided (quick iteration mode)
- Each screen must have 5 states: Default, Loading, Empty, Error, Validation
- States built from component library
- Gate: ≥80% (or SKIPPED if condition met)

**T4 - Flow Implementation (CONDITIONAL)**
- Skip Condition: No FL-XXX flows defined in figma_spec.md
- Prototype flows wired in 05_Prototype
- Screen transitions match flow definitions
- Gate: ≥80% (or SKIPPED if condition met)

### Executable Verification

#### T1: Structure & Spec Compliance
| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| 00_Cover | exists | [yes/no] | PASS/FAIL |
| 01_Foundations | exists | [yes/no] | PASS/FAIL |
| 02_Components | exists | [yes/no] | PASS/FAIL |
| 03_Patterns | exists | [yes/no] | PASS/FAIL |
| 04_Screens | exists | [yes/no] | PASS/FAIL |
| 05_Prototype | exists | [yes/no] | PASS/FAIL |
| 06_Handoff | exists | [yes/no] | PASS/FAIL |
| SCR Count | = spec count | [N]/[M] | PASS/FAIL |

```
Structure = (pages present / 7) × 100% - MUST = 100%
Spec Compliance = (generated screens / source screens) × 100% - MUST = 100%
T1 Score = MIN(Structure, Spec Compliance)
```

#### T2: Tokens & Components
| Check | Threshold | Actual | Score |
|-------|-----------|--------|-------|
| Color Tokens | = designsystem count | [N]/[M] | [X]% |
| Typography Tokens | = designsystem count | [N]/[M] | [X]% |
| Spacing Tokens | = designsystem count | [N]/[M] | [X]% |
| Components Built | = spec count | [N]/[M] | [X]% |
| Component States | 6 per component | [N]/[expected] | [X]% |

```
Token Score = (applied tokens / total tokens) × 100%
Component Score = (built components / specified components) × 100%
T2 Score = Average(Token Score, Component Score)
```

#### T3: Screen State Coverage [CONDITIONAL]
Status: [EVALUATED / SKIPPED - minimal mode]

| Check | Threshold | Actual | Score |
|-------|-----------|--------|-------|
| Default States | = screen count | [N]/[M] | [X]% |
| Loading States | = screen count | [N]/[M] | [X]% |
| Empty States | = screen count | [N]/[M] | [X]% |
| Error States | = screen count | [N]/[M] | [X]% |
| Validation States | = screen count | [N]/[M] | [X]% |

```
State Coverage = (total states / (screen count × 5)) × 100%
T3 Score = State Coverage
```

#### T4: Flow Implementation [CONDITIONAL]
Status: [EVALUATED / SKIPPED - no FL-XXX]

| Check | Threshold | Actual | Score |
|-------|-----------|--------|-------|
| Flows Wired | = FL count | [N]/[M] | [X]% |
| Screen Transitions | per flow definition | [N]/[expected] | [X]% |
| Entry Points | defined | [count] | [computed] |

```
Flow Score = (wired flows / total flows) × 100%
T4 Score = Flow Score
```

### Overall Assessment

| Tier | Dimension | Score | Gate | Result |
|------|-----------|-------|------|--------|
| T1 | Structure & Spec | [X]% | 100% | [P/F] |
| T2 | Tokens & Components | [X]% | ≥80% | [P/F] |
| T3 | Screen States | [X]% | ≥80% | [P/F/S] |
| T4 | Flow Implementation | [X]% | ≥80% | [P/F/S] |

**Verdict**: [PASS / CONDITIONAL PASS / FAIL]

**Top 3 Weaknesses:**
1. [Tier] - [Dimension] ([X]%): [Specific issue]
2. [Tier] - [Dimension] ([X]%): [Specific issue]
3. [Tier] - [Dimension] ([X]%): [Specific issue]

**Critical Failures**: [List MUST gates that failed, or "None"]

## Console Output Format

```
===============================================================
              FIGMA ARTIFACT GENERATION COMPLETE
===============================================================

1) Input Validation:
   - figma_spec.md: FOUND
   - designsystem.md: FOUND
   - Screens defined: [X]
   - Flows defined: [Y]

2) Figma Structure:
   [check] 00_Cover
   [check] 01_Foundations
   [check] 02_Components
   [check] 03_Patterns
   [check] 04_Screens
   [check] 05_Prototype
   [check] 06_Handoff

3) Components Built:
   - From designsystem.md: [X components]
   - Variants per component: [Y average]

4) Screens Generated:
   | Screen Name | States | From Spec |
   |-------------|--------|-----------|
   | [Name]      | 5      | SCR-XXX   |

5) Prototype Flows Wired:
   | Flow Name | Personas | Screens | Interactions |
   |-----------|----------|---------|--------------|
   | [Name]    | [List]   | [X]     | [Y]          |

6) Export Manifest:
   - Total JPGs: [Screens x 5 states]
   - Naming: <AppName>__<Platform>__<Screen>__<State>__v1.jpg

===============================================================

Rules Applied:
- rules/figma-design-standards.md
- rules/ui-ux-design-standards.md
- rules/web-accessibility-standards.md

Evaluation Scores:
| Dimension | Score |
|-----------|-------|
| Spec Compliance | [X]% |
| Token Application | [X]% |
| Structure | [X]% |
| Components | [X]% |
| Screen States | [X]% |
| Flow Implementation | [X]% |
| Export Completeness | [X]% |

Average Score: [X]%

Summary: [< 100 words]
===============================================================
```

---

*This workflow generates Figma artifacts from specifications. It does NOT create specifications - run create-figma-spec first.*
