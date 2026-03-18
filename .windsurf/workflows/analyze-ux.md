---
description: Comprehensive UI/UX analysis workflow leveraging Playwright automation, Context7 framework research, and sequential design reasoning to evaluate visual consistency, accessibility compliance, responsiveness, and user experience quality across multiple viewports and interaction patterns.
auto_execution_mode: 1
---

# Unified User Interface Analysis

As a Senior UX Designer with expertise in accessibility, responsive design, and user-centered design principles, conduct a structured evaluation of the user interface covering: visual consistency, accessibility (WCAG 2.1 AA), responsiveness across viewports, and interaction quality. This analysis combines automated testing via Playwright MCP, framework best practices research through Context7, and systematic design reasoning to ensure the UI meets high standards for visual consistency, accessibility compliance (WCAG 2.1 AA), responsive behavior across devices, intuitive interaction patterns, and overall user experience quality. The evaluation provides evidence-based feedback focused on identifying design issues and their impact on users, supporting continuous improvement of the interface.

## Input Parameters

**Primary Parameter (Recommended):**
- `task_file`: Path to task file containing Design References section (e.g., `.propel/context/tasks/us_001/task_001_login_ui.md`)
  - When provided, automatically extracts: Figma URL, Hi-Fi Wireframe path, Screen Spec (SCR-XXX), app_path, UXR requirements

**Alternative Parameters (Manual Override):**
- `figma_design`: Figma URL for visual reference (e.g., 'https://figma.com/file/abc123?node-id=2:45')
- `wireframe_path`: Wireframe reference for visual comparison. Accepts multiple formats:
  - **HTML file**: `.propel/context/wireframes/Hi-Fi/wireframe-SCR-001-login.html`
  - **PNG image**: `.propel/context/wireframes/Hi-Fi/wireframe-SCR-001-login.png`
  - **JPG image**: `.propel/context/wireframes/Hi-Fi/wireframe-SCR-001-login.jpg`
  - **External URL**: `https://figma.com/file/xxx?node-id=2:45` or `https://domain.com/wireframe.png`
- `screen_id`: Screen specification ID from figma_spec.md (e.g., 'SCR-001') for state requirements lookup
- `server_url`: URL of the development server (defaults to http://localhost:3000)
- `app_path`: URL path to review (e.g., '/checkout', '/dashboard', '/home'). Defaults to '/' if not specified
- `focus_area`: Aspect to emphasize in review - "full" (default), "accessibility", "responsive", "interactions", or "visual-polish"

### Parameter Processing
**If `task_file` is provided (Recommended Path):**
1. Read task file and parse "Design References" table
2. Extract values from table:
   | Reference Type | Extracted Value |
   |----------------|-----------------|
   | UI Impact | If "No", skip UX analysis entirely |
   | Figma URL | → `figma_design` parameter |
   | Wireframe Status | Check if AVAILABLE/EXTERNAL (proceed) or PENDING/N/A (skip wireframe comparison) |
   | Wireframe Path/URL | → `wireframe_path` parameter |
   | Screen Spec | → `screen_id` parameter (parse SCR-XXX) |
   | UXR Requirements | → Load from figma_spec.md for validation |
3. Derive `app_path` from screen specification route in figma_spec.md
4. Log: "Extracted design references from task file: [list extracted values]"

**If individual parameters provided (Manual Override):**
- Use provided values directly
- Log: "Using manual parameter override mode"

### Parameter Validation
- If task_file: Verify file exists and contains "Design References" section
- If UI Impact = "No" in task file: Return message "Task has no UI impact - skipping UX analysis"
- Verify server URL accessibility and response
- Validate Figma URL format if provided
- Validate wireframe_path exists and is readable (supports HTML, PNG, JPG, or URL)
- Validate screen_id exists in figma_spec.md (grep for SCR-XXX)
- Ensure app_path is properly formatted
- Validate focus_area against allowed values

### Wireframe Format Detection
**Before visual comparison, detect and validate wireframe format:**

```
INPUT: wireframe_path

1. IF wireframe_path is empty, NULL, or "N/A":
   - SET wireframe_type = "NONE"
   - Skip wireframe comparison phase
   - Log: "No wireframe provided - skipping pixel-perfect comparison"
   - Continue with other UX analysis phases

2. ELSE IF wireframe_path matches URL pattern (^https?://):
   - SET wireframe_type = "URL"
   - IF URL contains "figma.com":
     - SET wireframe_source = "FIGMA"
     - Use WebFetch to extract visual specifications
   - ELSE:
     - SET wireframe_source = "EXTERNAL_IMAGE"
     - Download image for comparison
   - Log: "Using external wireframe: [URL]"

3. ELSE IF wireframe_path ends with ".html":
   - SET wireframe_type = "HTML"
   - Verify file exists at path
   - Log: "Using HTML wireframe for Playwright multi-viewport comparison"

4. ELSE IF wireframe_path ends with ".png" OR ".jpg" OR ".jpeg":
   - SET wireframe_type = "IMAGE"
   - Verify file exists at path
   - Log: "Using image wireframe for visual comparison (single viewport)"

5. ELSE:
   - Log: "WARNING: Unrecognized wireframe format - attempting detection from file"
   - Attempt to detect format from file contents/headers
```

## Output
- Artifact generation:
  - `.propel/context/tasks/us_<ID>/reviews/ui-review-<task-id>.md`

**Note:** Extract US ID and task ID from task_file parameter
- Example: `.propel/context/tasks/us_001/task_001_login_ui.md`
  - US ID: `us_001`
  - Task ID: `task_001`
  - Output: `.propel/context/tasks/us_001/reviews/ui-review-task_001.md`
- Print the following:
  - List of rules applied to the workflow in bulleted format
  - Evaluation Scores in tabular format with average score
  - Evaluation summary (less than 100 words)
  **Do not save as file.** (Console output only)

**Note:**
- **File Handling**: IF file exists → UPDATE changed sections only (delta mode). IF file does not exist → CREATE complete file.
- Always create the output file in manageable smaller chunks to manage memory and processing constraints.
- Always generate a single unified document using
   - `.propel/templates/design-analysis-template.md` template

### US ID and Task ID Extraction
**Parse from task_file parameter:**
1. Extract US ID using pattern: `us_(\d{3})/`
   - Example: `.propel/context/tasks/us_001/task_001_login_ui.md` → `us_001`
2. Extract Task ID using pattern: `(task_\d{3}[^/]*?)\.md`
   - Example: `task_001_login_ui.md` → `task_001`
3. Construct output path: `.propel/context/tasks/{US_ID}/reviews/ui-review-{TASK_ID}.md`
4. Ensure reviews directory exists before writing

## Core Principles

### Automated Testing with Playwright MCP
- Navigate and interact with the UI programmatically
- Capture screenshots at multiple viewports with descriptive filenames
- Test keyboard navigation and accessibility features
- Monitor browser console for errors and warnings
- Verify responsive behavior across devices
- Capture interactive states (hover, focus, active) when relevant

### Framework Research via Context7 MCP (Use web fetch as a fallback)
- Detect UI frameworks from package.json or import statements
- Retrieve framework-specific design patterns and component guidelines
- Access accessibility best practices and ARIA implementation guides
- Review responsive design patterns and breakpoint strategies
- Gather performance optimization recommendations

### Sequential Design Reasoning (Use web fetch as a fallback)
- Use Sequential-thinking MCP for complex design analysis
- Evaluate component consistency and design token usage
- Assess visual hierarchy and information architecture
- Analyze user experience flow and cognitive load
- Perform step-by-step user journey evaluation

### Retrieve Design Specifications (Primary: figma_spec.md)
- **Primary Source**: Read `.propel/context/docs/figma_spec.md` for:
  - Screen inventory with state requirements (Default, Loading, Empty, Error, Validation)
  - Screen-to-persona mapping and flow definitions
  - Component requirements per screen
  - Export specifications and naming conventions
- **Secondary Source**: Read `.propel/context/docs/designsystem.md` for:
  - Design tokens (colors, typography, spacing, shadows)
  - Component specifications and variants
  - Brand guidelines and visual direction
- **Fallback**: Use Figma MCP to access design files directly if spec files unavailable
- Note any design annotations or developer handoff notes

### Communication Approach
- **Problems Over Prescriptions**: Describe problems and their impact, not technical solutions
- **Evidence-Based**: Always provide screenshots for visual issues with specific examples
- **Constructive Tone**: Maintain objectivity while being constructive

## Execution Flow

### Phase 1: Context7 Framework Research
**UI Framework Documentation Retrieval:**
1. Detect frameworks from codebase (package.json, imports)
2. Use `mcp__context7__resolve-library-id(libraryName: "framework-name")`
3. Fetch docs: `mcp__context7__get-library-docs(context7CompatibleLibraryID: "resolved-id", topic: "design-patterns,accessibility,responsive-design,best-practices")`

**Research Focus:**
- Framework-specific design patterns and component guidelines
- Accessibility best practices and ARIA implementation
- Responsive design patterns and breakpoint strategies
- Animation and interaction design principles
- Performance optimization for UI components

### Phase 2: Sequential Design Reasoning
Use `mcp__sequential-thinking__sequentialthinking` for:

**Design System Evaluation:**
- Analyze component consistency and design token usage
- Evaluate visual hierarchy and information architecture
- Assess brand alignment and design language coherence
- Review user experience flow and cognitive load

**Usability Analysis:**
- Step-by-step user journey evaluation
- Error prevention and recovery pattern analysis
- Accessibility impact assessment for different user groups
- Cross-platform and cross-browser compatibility reasoning

### Phase 3: Preparation & Setup
- Analyze PR description/changes to understand motivation and scope
- Review code diff to understand implementation details
- Set up Playwright browser with `mcp__playwright__browser_install`
- Configure initial viewport (1440x900 for desktop)
- Navigate to the development server URL

### Phase 4: Interaction and User Flow
- Execute primary user flows following testing notes
- Test all interactive states (hover, active, disabled, focus)
- Verify form submissions and validation feedback
- Check destructive action confirmations
- Assess perceived performance and responsiveness
- Document interaction patterns with screenshots

### Phase 5: Responsiveness Testing
- Test desktop viewport (1440px) with screenshot
- Test tablet viewport (768px) - verify layout adaptation
- Test mobile viewport (375px) - ensure touch optimization
- Verify no horizontal scrolling or element overlap
- Check responsive navigation patterns (hamburger menus, etc.)
- Document breakpoint transitions

### Phase 6: Visual Polish
- Assess layout alignment and spacing consistency
- Verify typography hierarchy and legibility
- Check color palette consistency and contrast
- Validate image quality and optimization
- Ensure visual hierarchy guides user attention
- Review animation timing and smoothness

### Phase 7: Accessibility (WCAG 2.1 AA)
- Test complete keyboard navigation (Tab order)
- Verify visible focus states on all interactive elements
- Confirm keyboard operability (Enter/Space activation)
- Validate semantic HTML usage
- Check form labels and ARIA attributes
- Verify image alt text and descriptions
- Test color contrast ratios (4.5:1 minimum for normal text)
- Run automated accessibility audit using `mcp__playwright__browser_evaluate`

### Phase 8: Robustness Testing
- Test form validation with invalid/edge case inputs
- Stress test with content overflow scenarios
- Verify loading, empty, and error states
- Check network failure handling
- Test browser back/forward navigation
- Validate data persistence across refreshes

### Phase 9: Code Health
- Verify component reuse over duplication
- Check for design token usage (no magic numbers)
- Ensure adherence to established patterns
- Review CSS organization and maintainability
- Check for console errors or warnings

### Phase 10: Content and Console
- Review grammar, spelling, and clarity of all text
- Check browser console for errors/warnings
- Verify proper error messaging
- Validate help text and tooltips

### Technical Implementation

**Playwright MCP Tools by Category:**

1. **Setup & Navigation:**
   - `mcp__playwright__browser_install` - Initialize browser
   - `mcp__playwright__browser_navigate` - Load pages
   - `mcp__playwright__browser_tabs` - Manage multiple views

2. **Interaction Testing:**
   - `mcp__playwright__browser_click` - Test clickable elements
   - `mcp__playwright__browser_type` - Input field testing
   - `mcp__playwright__browser_select_option` - Dropdown testing
   - `mcp__playwright__browser_hover` - Hover state validation
   - `mcp__playwright__browser_drag` - Drag and drop testing
   - `mcp__playwright__browser_press_key` - Keyboard navigation

3. **Visual Documentation:**
   - `mcp__playwright__browser_take_screenshot` - Capture evidence
   - `mcp__playwright__browser_resize` - Viewport testing
   - `mcp__playwright__browser_snapshot` - DOM analysis

4. **Quality Checks:**
   - `mcp__playwright__browser_console_messages` - Error monitoring
   - `mcp__playwright__browser_evaluate` - Run audits
   - `mcp__playwright__browser_network_requests` - Performance analysis
   - `mcp__playwright__browser_wait_for` - Loading state verification

### Pixel-Perfect Comparison (Design Specification Driven)

**Phase A: Load Design Specifications**

1. **Load Screen Specifications from figma_spec.md (using `screen_id`):**
   - Grep figma_spec.md for `SCR-XXX` section
   - Extract required states: Default, Loading, Empty, Error, Validation
   - Load component requirements for the screen
   - Note which personas this screen serves
   - Extract route/path for navigation

2. **Load Design Tokens from designsystem.md:**
   - Extract spacing scale for measurement validation
   - Load typography specifications (font, size, weight, line-height)
   - Reference color tokens for contrast and consistency checks
   - Load component variant specifications

3. **Load UXR Requirements (from task_file or figma_spec.md):**
   - Extract UXR-XXX requirements applicable to this screen
   - Create validation checklist for each UXR requirement

**Phase B: Wireframe Comparison (Adaptive by Format)**

**B.1: HTML Wireframe Comparison (wireframe_type = "HTML")**
1. **Open Wireframe in Playwright (Tab 1):**
   - Use `mcp__playwright__browser_navigate` to open wireframe HTML file (`file://` protocol)
   - Capture screenshot at each viewport: `wireframe_desktop_1440.png`, `wireframe_tablet_768.png`, `wireframe_mobile_375.png`
   - Note: Hi-Fi wireframes are static HTML representing the expected design

2. **Open Implementation in Playwright (Tab 2):**
   - Navigate to `server_url + app_path`
   - Capture screenshot at matching viewports: `impl_desktop_1440.png`, `impl_tablet_768.png`, `impl_mobile_375.png`

3. **Side-by-Side Visual Comparison:**
   ```
   For each viewport (1440px, 768px, 375px):
     1. Load wireframe screenshot and implementation screenshot
     2. Compare element positions (header, content, footer, navigation)
     3. Validate spacing matches designsystem.md tokens (±4px tolerance)
     4. Check typography matches (font-family, size, weight, color)
     5. Verify color usage against design tokens
     6. Document pixel deviations > 5px as issues
   ```

**B.2: Image Wireframe Comparison (wireframe_type = "IMAGE")**
1. **Load Wireframe Image:**
   - Read image file from wireframe_path (png/jpg)
   - Note: Image wireframes are single-viewport (no responsive variants)

2. **Capture Implementation Screenshot:**
   - Navigate to `server_url + app_path`
   - Capture at viewport closest to wireframe image dimensions
   - OR use default desktop viewport (1440px)

3. **Visual Comparison:**
   - Compare wireframe image against implementation screenshot
   - Note deviations in layout, spacing, typography
   - Document in Deviation Report
   - Note limitation: "Image wireframe - single viewport comparison only"

**B.3: External URL Wireframe Comparison (wireframe_type = "URL")**
1. **Fetch External Wireframe:**
   - IF Figma URL: Use WebFetch to extract frame specifications
   - IF Image URL: Download image for comparison

2. **Capture Implementation Screenshot:**
   - Navigate to `server_url + app_path`
   - Capture at appropriate viewport

3. **Visual Comparison:**
   - Compare external reference against implementation
   - Document limitations: "External URL reference - manual inspection may be required for full comparison"

**B.4: No Wireframe Available (wireframe_type = "NONE")**
1. **Skip Wireframe Comparison Phase**
2. **Log:** "No wireframe reference provided - focusing on implementation-only UX analysis"
3. **Alternative Checks:**
   - Verify against figma_spec.md state requirements
   - Check design token compliance from designsystem.md
   - Perform accessibility and responsiveness analysis without wireframe baseline

**Deviation Report Format (All Wireframe Types):**
| Element | Wireframe Source | Expected | Actual (Implementation) | Deviation | Severity |
|---------|------------------|----------|------------------------|-----------|----------|
| Header height | [HTML/PNG/URL] | 64px | 72px | +8px | Medium |
| Button padding | [type] | 16px | 12px | -4px | Low |

**Wireframe Source Limitations:**
| Source Type | Comparison Capability | Notes |
|-------------|----------------------|-------|
| HTML | Full responsive (3 viewports) | Can test all breakpoints |
| PNG/JPG | Single viewport | Limited to image dimensions |
| Figma URL | Reference only | Manual inspection may be required |
| External URL | Reference only | Subject to URL accessibility |

**Phase C: Figma URL Reference (when `figma_design` provided)**

1. **Extract Visual Details:**
   - For Figma URLs: Use WebFetch to extract visual specifications from Figma
   - Cross-reference with figma_spec.md screen specifications
   - Note any design annotations or developer handoff notes

2. **Validate Against Figma:**
   - Compare component styling against Figma frame
   - Verify iconography and imagery match
   - Check interactive state designs (hover, focus, active)

**Phase D: State Coverage Verification**

1. **Test All 5 Required States (per figma_spec.md):**
   | State | How to Trigger | Expected Behavior | Screenshot |
   |-------|---------------|-------------------|------------|
   | Default | Initial load | Normal content display | `state_default.png` |
   | Loading | Slow network / mock delay | Skeleton or spinner | `state_loading.png` |
   | Empty | No data scenario | Empty state message/illustration | `state_empty.png` |
   | Error | API failure / invalid input | Error message display | `state_error.png` |
   | Validation | Form submission errors | Field-level error indicators | `state_validation.png` |

2. **State Coverage Score:**
   - States implemented: [N]/5
   - Missing states: [list]

**Phase E: Document Deviations**
- List specific measurements that differ from designsystem.md tokens
- Identify missing screen states from figma_spec.md requirements
- Prioritize based on visual impact and state coverage
- Provide recommendations for both strict design adherence and practical implementation approaches

### Edge Cases to Consider
- Browser-specific rendering differences
- Font availability and fallbacks
- Dynamic content that might affect layout
- Animations and transitions not visible in static designs
- Screen state coverage (all 5 states per figma_spec.md)
- Accessibility improvements that might deviate from pure visual design

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
- `rules/ui-ux-design-standards.md`: Hierarchy, accessibility, consistency **[CRITICAL]**
- `rules/web-accessibility-standards.md`: WCAG 2.2 AA compliance **[CRITICAL]**

**>>> ALWAYS: Execute Quality Evaluation. Follow the 4-tier evaluation framework instructions to evaluate the outcomes. <<<**

## Quality Evaluation

- **Invoke**: `.windsurf/workflows/evaluate-output.md`
  - **$OUTPUT_FILE**: `.propel/context/tasks/us_XXX/reviews/ui-review-*.md`
  - **$SCOPE_FILES**: Task file path (from `task_file` parameter)
  - **--workflow-type**: `ui-review`

---