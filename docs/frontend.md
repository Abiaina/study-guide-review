---
title: Frontend Development
---

# Frontend Development

*Concise reference for DevOps, Backend, and Full-Stack interviews. Focuses on concepts and talking points, not deep frontend engineering.*

---

## The DOM (Document Object Model)

**What it is**: A tree-structured in-memory representation of an HTML document. JavaScript manipulates this tree to update the UI without page reloads.

**Key API surface**:

| Method / Property | Purpose |
|---|---|
| `document.querySelector('.cls')` | Select first matching element (CSS selector) |
| `element.addEventListener('click', fn)` | Attach event handler |
| `element.appendChild(child)` | Add child node |
| `element.remove()` | Remove element from DOM |
| `element.textContent = '...'` | Set text safely (no XSS risk unlike `innerHTML`) |
| `element.setAttribute('data-id', '1')` | Set HTML attribute |

**Event delegation** — Attach one listener to a parent instead of many listeners to individual children. Works because DOM events bubble up the tree. Essential for dynamically added elements and for performance with large lists.

```javascript
// One listener handles all button clicks in the list
document.getElementById('list').addEventListener('click', (event) => {
    if (event.target.matches('.item-btn')) {
        handleClick(event.target.dataset.id);
    }
});
```

**Reflow vs repaint**:
- **Reflow** (expensive) — changing layout properties: `width`, `height`, `position`, `margin`. Causes browser to recalculate layout of affected elements and descendants.
- **Repaint** (cheaper) — changing visual properties only: `color`, `background`, `visibility`. No layout recalculation.
- **Batch writes** using `DocumentFragment` or a single CSS class swap to minimize reflows.

---

## React — Mental Model

**Core idea**: `UI = f(state)` — the view is a pure function of state. React re-renders a component whenever its state or props change, diffs the new Virtual DOM against the previous one (**reconciliation**), and applies only the changed nodes to the real DOM.

**Data flow**:
- Data flows **down** via props
- Events flow **up** via callback props
- Shared state lives in the **nearest common ancestor**

### Hooks Quick Reference

| Hook | Purpose | Interview gotcha |
|---|---|---|
| `useState` | Local component state | Setter is async — don't read state immediately after calling it |
| `useEffect` | Side effects: fetching, subscriptions, timers | Dependency array controls when it runs (see below) |
| `useRef` | DOM refs; mutable values that don't trigger re-render | Changing `.current` does NOT cause a re-render |
| `useMemo` | Cache expensive computed values | Only add when profiling shows real cost |
| `useCallback` | Stable function reference across renders | Needed when passing callbacks to memoized children |
| `useContext` | Read from Context without prop drilling | Context changes re-render ALL consumers |

**`useEffect` dependency array** — the most common interview question:

```javascript
useEffect(() => { /* ... */ }, []);      // runs once on mount
useEffect(() => { /* ... */ }, [dep]);   // runs on mount + when dep changes
useEffect(() => { /* ... */ });          // runs after every render (usually a bug)
// Return a cleanup function to cancel subscriptions/timers on unmount
useEffect(() => {
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
}, []);
```

---

## Performance Patterns

| Pattern | What it does | When to reach for it |
|---|---|---|
| `React.memo` | Skips re-render if props are shallow-equal | Child receives stable props but parent re-renders often |
| `useMemo` | Caches computed value | Expensive derivation (sorting/filtering large arrays) |
| `useCallback` | Caches function reference | Callback passed to a `React.memo`-wrapped child |
| `React.lazy` + `Suspense` | Defers loading a component's JS bundle | Large feature not needed on initial load |
| Virtual list | Renders only visible rows | Lists with 1000+ items |

**Rule of thumb**: don't add `useMemo`/`useCallback` preemptively. React is fast by default; memoization adds complexity and has its own overhead. Profile first.

---

## Interview Talking Points

**Virtual DOM**: "React keeps a lightweight JS-object copy of the DOM. On re-render it diffs old vs new virtual trees and batches the minimal real DOM mutations — avoiding redundant layout recalculations."

**When to lift state**: "When two sibling components need shared data, move the state to their nearest common ancestor and pass it down as props plus a setter callback."

**Context vs Redux / Zustand**: "Context is built-in and fine for low-frequency global values like theme or auth user. A dedicated store (Zustand, Redux Toolkit) is better when many components need frequent updates, or when you need middleware, time-travel debugging, or serializable state."

**Reconciliation and keys**: "React compares elements by type and key. If the type changes it unmounts and remounts. Stable, unique keys tell React which list items are the same across renders — missing or index-based keys can force unnecessary remounts."

**Class components vs hooks**: "Class components use lifecycle methods (`componentDidMount`, `componentDidUpdate`, `componentWillUnmount`). Hooks unify this into `useEffect` and make it easier to reuse stateful logic via custom hooks. New code should use function components with hooks."

---

## Quick-Reference Card

```
Component re-renders when:    state changes | parent re-renders | context changes
Prevent re-render:            React.memo | PureComponent
Side effects go in:           useEffect (not render body)
Cleanup side effects:         return fn from useEffect
Avoid passing as props:       new object/array literals each render — breaks memo
State updates are:            batched and async — don't read state right after setState
```

---

*For deep frontend work (advanced state machines, SSR, accessibility, bundler config) see a dedicated frontend guide.*
