---
description: Generates Playwright TypeScript automation scripts from test workflow specifications
auto_execution_mode: 1
---

# Playwright Script Generator

As an expert Test Automation Engineer, generate production-ready Playwright TypeScript scripts from test workflow specifications created by `/create-automation-test`.

## Input Parameters

### $ARGUMENTS (Optional)
**Accepts:** Workflow file path | Empty (auto-scan)
**Default:** Auto-discover `tw_*.md` and `e2e_*.md` files in `.propel/context/test/`

### --type (Optional)
**Accepts:** `feature` | `e2e` | `both`
**Default:** `both`

| Value | Input Files | Output Location |
|-------|-------------|-----------------|
| `feature` | `tw_*.md` | `test-automation/tests/<feature>.spec.ts` |
| `e2e` | `e2e_*.md` | `test-automation/e2e/<journey>.spec.ts` |
| `both` | Both patterns | Both locations (default) |

### Input Processing Instructions

| Input | Action |
|-------|--------|
| Empty | Scan `.propel/context/test/tw_*.md` and `e2e_*.md` |
| File path | Process specified workflow file |
| Feature name | Find matching `tw_<feature>.md` or `e2e_<journey>.md` |

## Output

| --type Value | Artifacts Generated |
|--------------|---------------------|
| `feature` | `test-automation/tests/<feature>.spec.ts` |
| `e2e` | `test-automation/e2e/<journey>.spec.ts` |
| `both` | Both locations |

**Common Artifacts:**
- `test-automation/pages/<page>.page.ts`
- `test-automation/data/<feature>.json`
- `test-automation/playwright.config.ts` (if not exists)

**Print** (console only):
- Rules used (bulleted list)
- Evaluation Scores (table)
- Summary (<100 words)

## Execution Flow

### Deep Research Methodology

**MCP Tools Required:**
- `mcp__sequential-thinking__sequentialthinking` - Systematic code generation
- `mcp__context7__resolve-library-id` - Pin Playwright version
- `mcp__context7__get-library-docs` - Fetch API documentation

**Fallback:** If MCP unavailable, use structured iterative analysis.

### Step 1: Workflow Discovery

| --type Value | Scan Pattern |
|--------------|--------------|
| `feature` | `.propel/context/test/tw_*.md` |
| `e2e` | `.propel/context/test/e2e_*.md` |
| `both` | Both patterns |

1. If $ARGUMENTS empty: scan based on --type
2. Parse YAML blocks from workflow file
3. Extract: test_cases, page_objects, test_data, metadata

### Step 2: Technology Research
**Use:** `mcp__context7__resolve-library-id`, `mcp__context7__get-library-docs`

1. Resolve and pin Playwright version
2. Fetch current assertion API patterns
3. Fetch page object best practices
4. Detect TypeScript version for compatibility

### Step 3: Test File Generation (--type feature or both)
**Use:** `mcp__sequential-thinking__sequentialthinking`
**Condition:** Execute when --type is `feature` or `both`

**Output:** `test-automation/tests/<feature>.spec.ts`

**Template:**
```typescript
import { test, expect } from '@playwright/test';
import { [PageName]Page } from '../pages/[page].page';

test.describe('[FEATURE_NAME]', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('[BASE_URL]');
  });

  test('[TC_ID]: [TEST_NAME]', async ({ page }) => {
    // Step-by-step from workflow YAML
  });
});
```

**Generation Rules:**
- One `test.describe` block per feature
- One `test()` per TC-XXX
- `beforeEach` for navigation
- Assertions use `await expect()`

### Step 3.5: E2E Test File Generation (--type e2e or both)
**Use:** `mcp__sequential-thinking__sequentialthinking`
**Condition:** Execute when --type is `e2e` or `both`

**Output:** `test-automation/e2e/<journey>.spec.ts`

**Template:**
```typescript
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { DashboardPage } from '../pages/dashboard.page';
import { [PageName]Page } from '../pages/[page].page';

test.describe('E2E: [JOURNEY_NAME]', () => {
  test('[TC_ID]: Complete user journey', async ({ page }) => {
    // Phase 1: [UC-001 NAME]
    const loginPage = new LoginPage(page);
    await page.goto('/login');
    await loginPage.login(testData.user.email, testData.user.password);
    await expect(page).toHaveURL(/dashboard/);

    // Phase 2: [UC-002 NAME]
    const dashboardPage = new DashboardPage(page);
    await dashboardPage.navigateToOrders();
    await expect(page).toHaveURL(/orders/);

    // Phase 3: [UC-003 NAME]
    const orderPage = new OrderPage(page);
    await orderPage.createOrder(testData.order);
    await expect(page.getByText('Order Created')).toBeVisible();
  });
});
```

**E2E Generation Rules:**
- One `test.describe` block per journey
- One `test()` per E2E journey (phases are sequential within test)
- NO `beforeEach` for E2E (journey maintains state across phases)
- Checkpoints validate intermediate states
- Session state shared across all phases

### Step 4: Page Object Generation
**Use:** `mcp__context7__get-library-docs` + `mcp__sequential-thinking__sequentialthinking`

**Output:** `test-automation/pages/<page>.page.ts`

**Template:**
```typescript
import { Page, Locator } from '@playwright/test';

export class [PageName]Page {
  constructor(private page: Page) {}

  // Locators as getters
  get [elementName](): Locator {
    return this.page.getByRole('[role]', { name: '[name]' });
  }

  // Actions (no assertions)
  async [actionName]([params]): Promise<void> {
    // Action implementation
  }
}
```

**Rules:**
- Locators as readonly getters
- Actions as async methods
- NO assertions in page objects
- NO waitForTimeout

### Step 5: Test Data Generation

**Output:** `test-automation/data/<feature>.json`

Extract test_data from workflow YAML into JSON fixtures.

### Step 6: Configuration

**Output:** `test-automation/playwright.config.ts` (if not exists)

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30000,
  expect: { timeout: 5000 },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: 'html',
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
```

### Step 7: Validation

1. Run: `npx tsc --noEmit`
2. Fix any TypeScript errors
3. Verify all TC-XXX have corresponding test() blocks

## Guardrails

- `rules/playwright-testing-guide.md`: Test independence, wait strategies **[CRITICAL]**
- `rules/playwright-typescript-guide.md`: Code quality, assertions **[CRITICAL]**
- `rules/playwright-standards.md`: Locator priority, templates
- `rules/typescript-styleguide.md`: TypeScript conventions **[CRITICAL]**

**>>> ALWAYS: Execute Quality Evaluation. <<<**

## Quality Evaluation

### 4-Tier Playwright Script Assessment

| Tier | Dimension | Gate | Conditional |
|------|-----------|------|-------------|
| T1 | TypeScript Validity + Test Isolation | MUST PASS | No (always required) |
| T2 | Test Coverage + E2E Coverage | ≥80% | No (always required) |
| T3 | Locator Quality + Wait Strategy + POM Compliance | ≥80% | Yes (skip if ≤5 tests generated) |
| T4 | Journey Continuity + Pattern Adherence | ≥80% | Yes (skip if no E2E tests) |

### Tier Definitions

**T1 - Build & Isolation (REQUIRED)**
- TypeScript must compile without errors (`tsc --noEmit` exit 0)
- Tests must be isolated (no shared state, proper beforeEach usage)
- Gate: MUST PASS (execution halts if either fails)

**T2 - Coverage (REQUIRED)**
- Test coverage: test() blocks / TC count from workflow ≥80%
- E2E coverage: E2E tests / journey count ≥80%
- Gate: ≥80% aggregate

**T3 - Code Quality Patterns (CONDITIONAL)**
- Skip Condition: ≤5 tests generated (small test sets don't benefit from pattern analysis)
- Locator quality: Role-based locators vs CSS selectors (prefer getByRole/getByTestId/getByLabel)
- Wait strategy: No waitForTimeout usage (use assertions instead)
- POM compliance: No expect() in page object files
- Gate: ≥80% (or SKIPPED if condition met)

**T4 - E2E Journey Quality (CONDITIONAL)**
- Skip Condition: No E2E tests generated (--type=feature only)
- Journey continuity: Session state maintained across E2E phases
- Pattern adherence: Follows E2E best practices from guardrails
- Gate: ≥80% (or SKIPPED if condition met)

### Executable Verification

#### T1: Build & Isolation
| Check | Command | Expected | Actual | Status |
|-------|---------|----------|--------|--------|
| TypeScript | `tsc --noEmit` | exit 0 | [result] | PASS/FAIL |
| Test List | `npx playwright test --list` | lists tests | [result] | PASS/FAIL |
| Shared State | grep `let.*=.*` outside describe | 0 | [count] | PASS/FAIL |
| beforeEach | grep `beforeEach` per describe | ≥1 | [count] | PASS/FAIL |

#### T2: Coverage
| Check | Threshold | Actual | Score |
|-------|-----------|--------|-------|
| Test Blocks | TC count from workflow | [N]/[M] | [X]% |
| E2E Tests | Journey count from workflow | [N]/[M] | [X]% |

```
Test Coverage = (implemented TC / source TC) × 100%
E2E Coverage = (E2E tests / journey count) × 100%
T2 Score = Average(Test Coverage, E2E Coverage)
```

#### T3: Code Quality Patterns [CONDITIONAL]
Status: [EVALUATED / SKIPPED - ≤5 tests]

| Check | Pattern | Threshold | Actual | Score |
|-------|---------|-----------|--------|-------|
| Role-based Locators | `getByRole\|getByTestId\|getByLabel` | 100% | [N]/[total] | [X]% |
| CSS Selectors | `querySelector\|\.class\|#id` | 0 | [count] | [computed] |
| waitForTimeout | `waitForTimeout` | 0 | [count] | [computed] |
| POM Assertions | `expect\(` in pages/*.ts | 0 | [count] | [computed] |

```
Locator Score = (role-based / total locators) × 100%
Wait Score = (waitForTimeout == 0) ? 100% : 0%
POM Score = (expect in pages == 0) ? 100% : 0%
T3 Score = Average(Locator, Wait, POM)
```

#### T4: E2E Journey Quality [CONDITIONAL]
Status: [EVALUATED / SKIPPED - no E2E tests]

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Session State | Maintained across phases | [yes/no] | PASS/FAIL |
| No beforeEach in E2E | 0 beforeEach in e2e/*.spec.ts | [count] | PASS/FAIL |
| Checkpoint Assertions | ≥1 per phase | [count] | PASS/FAIL |

### Overall Assessment

| Tier | Dimension | Score | Gate | Result |
|------|-----------|-------|------|--------|
| T1 | Build & Isolation | [PASS/FAIL] | MUST | [P/F] |
| T2 | Coverage | [X]% | ≥80% | [P/F] |
| T3 | Code Quality | [X]% | ≥80% | [P/F/S] |
| T4 | E2E Journey | [X]% | ≥80% | [P/F/S] |

**Verdict**: [PASS / CONDITIONAL PASS / FAIL]

**Top 3 Weaknesses:**
1. [Tier] - [Dimension] ([X]%): [Specific issue]
2. [Tier] - [Dimension] ([X]%): [Specific issue]
3. [Tier] - [Dimension] ([X]%): [Specific issue]

**Critical Failures**: [List MUST gates that failed, or "None"]

---

*Generates production-ready Playwright TypeScript scripts from test workflow specifications.*
