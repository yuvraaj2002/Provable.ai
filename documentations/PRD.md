This is a comprehensive Product Requirements Document (PRD) tailored for a  **Frontend-First build** .

I have designed this to reject the standard "SaaS Purple/Round" aesthetic in favor of a **Cyber-Industrial / High-Fidelity HUD** design language (think Linear meets Kali Linux).

---

# Product Requirements Document (PRD): Provable.ai

**Version:** 1.0 | **Status:** Draft | **Theme:** Cyber-Industrial / Zero-Trust

## 1. Design System & Aesthetic (The "Anti-Basic" Mandate)

**Core Philosophy:** The UI must feel like a weapon system or a flight deck, not a marketing website. It should feel "dense" but "scannable."

* **Color Palette:**
  * **Background:** Deep Void (`#050505`) and Gunmetal (`#0A0A0A`). **No pure white.**
  * **Primary Accent:** "Acid Lime" (`#CCFF00`) for success/active states (high visibility).
  * **Danger/Alert:** "Plasma Red" (`#FF2A00`) and "Biohazard Orange" (`#FF8800`).
  * **Text:** Monospace fonts for data (JetBrains Mono/Fira Code) and geometric sans-serif for headers (Inter/Space Grotesk).
* **Visual Language:**
  * **Borders:** 1px sharp borders with low opacity (`rgba(255,255,255,0.1)`). No soft drop shadows.
  * **Glassmorphism:** Used sparingly, only for sticky headers/modals, with high blur and noise texture.
  * **Data Viz:** Sparklines, heatmaps, and "radar scans" instead of pie charts.
  * **Motion:** Instant, mechanical transitions (0.1s ease-out). No bouncy animations.

---

## 2. Core User Personas

1. **The Breaker (Red Teamer):** Wants to see where the AI failed. Needs detailed logs, diffs, and raw JSON.
2. **The Blocker (Compliance Officer):** Wants a "Green/Red" status. Needs PDF reports and high-level safety scores.

---

## 3. Sitemap & Navigation Structure

**Global Sidebar (Collapsible, Left):**

1. **Mission Control** (Dashboard)
2. **Attack Studio** (Red Teaming/Fuzzing)
3. **Live Interceptor** (Real-time Guardrails)
4. **Forensics** (Deep Trace Analysis)
5. **Compliance Vault** (Reports & Policies)
6. **Settings** (API Keys, Webhooks)

---

## 4. Page-by-Page UI Specifications

### A. Mission Control (Dashboard)

Goal: Instant situational awareness of AI health.

Layout: Bento Grid (Dense).

* **Widget 1: The "Defcon" Status:**
  * Large indicator showing current system trust score (e.g., "94% TRUSTED").
  * Visual: A circular progress ring that glows Lime or Red based on score.
* **Widget 2: Live Attack Surface:**
  * A real-time scrolling terminal log showing incoming prompts being audited.
  * *Effect:* Text fades in quickly like a hacker terminal.
* **Widget 3: Hallucination Heatmap:**
  * A 24-hour grid (like GitHub contributions) showing clusters of hallucinations.
  * *Interaction:* Hovering over a red square shows a tooltip summary of the failure.
* **Widget 4: Threat Vector Radar:**
  * A Spider Chart (Radar Chart) comparing risks: PII Leaks, Toxicity, Competitor Mentions, Hallucinations.

### B. Attack Studio (The Fuzzing Engine)

Goal: Configure and run adversarial agents against the user's AI model.

Layout: Split Screen (Configuration vs. Execution).

* **Left Panel (The Armory):**
  * **Agent Selector:** Dropdown to pick the attacker persona (e.g., "The Do Anything Now (DAN) Attacker", "The SQL Injector", "The PII Extractor").
  * **Intensity Slider:** A range slider from "Probe" (Low) to "Nuke" (High).
  * **Mutation Count:** Input field for how many prompt variations to generate (e.g., 50 variations).
* **Right Panel (The Battleground):**
  * **Prompt Diff View:** Show the "Base Prompt" vs. the "Mutated Prompt" side-by-side using red/green highlighting (standard code diff UI).
  * **Response Stream:** As the attack runs, responses stream in.
  * **Success Tags:** Auto-tagging outputs as `[SAFE]`, `[LEAK]`, or `[HALLUCINATION]` in distinct pill badges.

### C. Live Interceptor (Guardrails Config)

Goal: Visualizing the "Firewall" rules.

Layout: Node-based Flow Editor (React Flow / Svelte Flow).

* **Visual Editor:**
  * Users drag and drop "Logic Nodes" between the User and the LLM.
  * *Nodes:* "PII Scrubber", "Topic Blocker", "Tone Check", "Competitor Filter".
* **The "Simulation" Toggle:**
  * A toggle switch in the corner: "Dry Run" (Log only) vs. "Active Block" (Stop request).
  * *Visual Cue:* When "Active Block" is on, the border of the screen pulses a faint red.

### D. Forensics (Trace Analysis)

Goal: Deep dive into a single failed interaction.

Layout: Master-Detail View.

* **Left List:** List of flagged interactions, sorted by severity.
* **Center Stage (The Anatomy of a Prompt):**
  * **Timeline View:** A vertical waterfall chart showing latency breakdown (Retrieval -> Generation -> Audit).
  * **Context Inspector:** Display the exact chunks of text retrieved from the Vector DB.
  * **Hallucination Highlighter:** The AI's response is displayed in a text block.
    * *Feature:* Words that are *not* supported by the context are highlighted in Neon Orange.
    * *Interaction:* Clicking a highlighted sentence draws a connecting line to the contradictory evidence in the source docs (use SVG lines).

---

## 5. Key Micro-Interactions (The "Premium" Feel)

1. **Keyboard Shortcuts:** `Cmd+K` opens a global command palette (like Spotlight) to jump to any page or run a quick scan.
2. **Copy-to-Clipboard:** Clicking any ID, JSON snippet, or Prompt gives a satisfying "Copied" toast notification with a mechanical sound effect (optional toggle).
3. **Loading States:** No spinning circles. Use "scrambling text" decoding effects (Matrix style) or skeletal loaders with a scanning light bar.

---

## 6. Technical Frontend Stack Recommendation

* **Framework:** Next.js (React) or SvelteKit (for better performance).
* **Styling:** Tailwind CSS (utility-first is crucial for this dense layout).
* **Component Library:** **Shadcn UI** (customized to dark mode) or **Radix UI** primitives.
* **Charts:** Recharts or VisX (customizable D3 wrappers).
* **Icons:** Lucide Icons (clean, sharp).
* **Code Editor:** Monaco Editor (for viewing raw JSON/Prompts).

---

## 7. Next Step for You

"Build Phase 1: The Shell"

I recommend you start by setting up the Next.js project with Tailwind.

Would you like me to generate the tailwind.config.js file with the custom "Deep Void" and "Acid Lime" color palette I defined above so you can start with the exact theme immediately?
