import { useEffect, useMemo, useState } from "react";

type Tender = {
  id: string;
  title: string;
  reference_number: string | null;
  organization: string | null;
  source_url: string;
  relevance_state: string;
  current_version: number;
  listing_metadata: Record<string, unknown>;
};
type Notification = { id: string; event_type: string; status: string; created_at: string };

const states = ["ALL", "RELEVANT", "UNCERTAIN", "NOT_RELEVANT"];

async function loadTenders(): Promise<Tender[]> {
  const response = await fetch("/api/v1/tenders");
  if (!response.ok) throw new Error(`Tender API returned ${response.status}`);
  return response.json() as Promise<Tender[]>;
}

export function Dashboard() {
  const [tenders, setTenders] = useState<Tender[]>([]);
  const [query, setQuery] = useState("");
  const [state, setState] = useState("ALL");
  const [selected, setSelected] = useState<Tender | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [decision, setDecision] = useState("BID");
  const [decisionError, setDecisionError] = useState<string | null>(null);
  const [notifications, setNotifications] = useState<Notification[]>([]);

  useEffect(() => {
    loadTenders().then(setTenders).catch((reason: Error) => setError(reason.message));
    fetch("/api/v1/notifications?unread_only=true").then((response) => response.ok ? response.json() as Promise<Notification[]> : []).then(setNotifications);
  }, []);

  const filtered = useMemo(
    () =>
      tenders
        .filter((tender) => state === "ALL" || tender.relevance_state === state)
        .filter((tender) =>
          `${tender.title} ${tender.organization ?? ""} ${tender.reference_number ?? ""}`
            .toLowerCase()
            .includes(query.toLowerCase()),
        ),
    [query, state, tenders],
  );

  async function submitDecision(value: string) {
    if (!selected) return;
    setDecision(value);
    setDecisionError(null);
    const response = await fetch(`/api/v1/tenders/${selected.id}/decisions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ decision, decline_reason: decision === "NO_BID" ? "Manual review" : null, category: decision === "NO_BID" ? "User decision" : null }),
    });
    if (!response.ok) {
      setDecisionError("Decision could not be saved.");
      return;
    }
    setDecisionError("Decision saved.");
  }

  return (
    <div className="shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">LOCAL OPERATIONS CONSOLE</p>
          <h1>Tender Scanner</h1>
        </div>
        <span className="status-dot">● API CONNECTED</span>
      </header>
      <main>
        <section className="hero">
          <div>
            <p className="eyebrow">REVIEW QUEUE</p>
            <h2>Find the next opportunity worth pursuing.</h2>
            <p className="muted">Filter tenders, inspect evidence, and keep bid decisions moving.</p>
          </div>
          <div className="metric"><strong>{tenders.length}</strong><span>Total tenders</span></div>
          <div className="metric"><strong>{tenders.filter((t) => t.relevance_state === "RELEVANT").length}</strong><span>Relevant</span></div>
          <div className="metric"><strong>{notifications.length}</strong><span>Unread alerts</span></div>
        </section>
        {notifications.length > 0 && <div className="notice alert-strip">{notifications.length} notification{notifications.length === 1 ? "" : "s"} need review.</div>}
        <section className="toolbar">
          <input aria-label="Search tenders" placeholder="Search title, organization, reference..." value={query} onChange={(e) => setQuery(e.target.value)} />
          <div className="filters">{states.map((item) => <button className={state === item ? "active" : ""} key={item} onClick={() => setState(item)}>{item.replace("_", " ")}</button>)}</div>
        </section>
        {error && <div className="error">{error}. Start the FastAPI server to load live data.</div>}
        <section className="workspace">
          <div className="list">
            <div className="section-heading"><span>{filtered.length} opportunities</span><span className="muted">Newest first</span></div>
            {filtered.map((tender) => (
              <button className={`tender-card ${selected?.id === tender.id ? "selected" : ""}`} key={tender.id} onClick={() => setSelected(tender)}>
                <span className={`badge ${tender.relevance_state.toLowerCase()}`}>{tender.relevance_state.replace("_", " ")}</span>
                <h3>{tender.title}</h3>
                <p>{tender.organization ?? "Organization not stated"} · {tender.reference_number ?? "No reference"}</p>
                <small>Version {tender.current_version}</small>
              </button>
            ))}
            {!filtered.length && <div className="empty"><strong>No tenders match this view.</strong><span>Run a source scan or adjust your filters.</span></div>}
          </div>
          <aside className="detail">
            {selected ? (
              <>
                <span className={`badge ${selected.relevance_state.toLowerCase()}`}>{selected.relevance_state}</span>
                <h2>{selected.title}</h2>
                <dl><dt>Organization</dt><dd>{selected.organization ?? "Not stated"}</dd><dt>Reference</dt><dd>{selected.reference_number ?? "Not stated"}</dd><dt>Source</dt><dd><a href={selected.source_url} target="_blank" rel="noreferrer">Open source ↗</a></dd></dl>
                <div className="notice">Analysis and document status appear as processing completes.</div>
                <div className="decision"><strong>Record decision</strong><div className="decision-actions"><button className={decision === "BID" ? "active" : ""} onClick={() => submitDecision("BID")}>BID</button><button className={decision === "NO_BID" ? "active" : ""} onClick={() => submitDecision("NO_BID")}>NO BID</button></div>{decisionError && <small>{decisionError}</small>}</div>
              </>
            ) : <div className="empty detail-empty"><strong>Select an opportunity</strong><span>Its analysis and evidence will appear here.</span></div>}
          </aside>
        </section>
      </main>
    </div>
  );
}
