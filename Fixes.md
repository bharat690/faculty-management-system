# UI/UX Improvements & Bug Fixes

## 🔴 High Priority

### 1. Faculty Workload Analytics
**Issue:**
- **Path:** `Dean Dashboard → Dashboard → Analytics → Faculty Workload`
- Switching the dropdown causes the entire screen to flash and remain in a loading state for approximately **5 seconds**.

**Required Improvements:**
- Eliminate full-page flashing during dropdown changes.
- Implement smooth loading transitions (partial skeleton loader or spinner).
- Preserve graph state while new data is being fetched.
- Add **Ascending** and **Descending** sorting options for graph data.

---

### 2. Overall User Experience
- Improve the overall application UX.
- Ensure smoother page transitions and interactions.
- Reduce unnecessary layout shifts and screen flickering.
- Standardize loading and feedback patterns across the application.

---

### 3. Login Page
- Redesign and modernize the Login Page UI.
- Improve visual hierarchy, spacing, and responsiveness.
- Enhance loading and authentication feedback.

---

### 4. Loading Indicators
- Add consistent **screen-level loaders/spinners** wherever data is being fetched.
- Use skeleton loaders where appropriate to improve perceived performance.

---

### 5. Faculty Dashboard
- Improve the Faculty Dashboard UX.
- Add loading spinners/skeleton screens for all asynchronous data loads.
- Prevent abrupt content rendering and UI flashing.

---

## 🟡 Academic Structure Updates

### Department Consolidation

Merge the following programs under unified departments:

| Current Programs | Consolidated Department |
|------------------|-------------------------|
| BCA, MCA | **CSA** |
| B.Tech CSE, M.Tech CSE, DS in CSE | **CSE** |
| B.Tech AI&ML, B.Tech Cyber Security | **AI & ML** |