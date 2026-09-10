import { FormEvent, useMemo, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

type SummarizeResponse = {
  summary: string;
};

function App() {
  const [dialogue, setDialogue] = useState("");
  const [summary, setSummary] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const canSubmit = useMemo(() => dialogue.trim().length > 0 && !isLoading, [dialogue, isLoading]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!API_BASE_URL) {
      setError("Missing VITE_API_BASE_URL in frontend .env");
      return;
    }

    if (!dialogue.trim()) {
      return;
    }

    setIsLoading(true);
    setError("");
    setSummary("");

    try {
      const response = await fetch(`${API_BASE_URL}/summarize`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ dialogue }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = (await response.json()) as SummarizeResponse;
      setSummary(data.summary);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Unable to summarize text");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="workspace" aria-labelledby="page-title">
        <header className="workspace-header">
          <div>
            <p className="eyebrow">T5 backend</p>
            <h1 id="page-title">Text Summarizer</h1>
          </div>
          
        </header>

        <form className="summarizer" onSubmit={handleSubmit}>
          <label className="field-label" htmlFor="dialogue">
            Dialogue
          </label>
          <textarea
            id="dialogue"
            value={dialogue}
            onChange={(event) => setDialogue(event.target.value)}
            placeholder="Paste dialogue or long text here..."
            rows={10}
          />

          <div className="actions">
            <button type="submit" disabled={!canSubmit}>
              {isLoading ? "Summarizing..." : "Summarize"}
            </button>
            <button type="button" className="secondary" onClick={() => setDialogue("")} disabled={isLoading || !dialogue}>
              Clear
            </button>
          </div>
        </form>

        {(summary || error) && (
          <section className="result" aria-live="polite">
            <h2>{error ? "Error" : "Summary"}</h2>
            <p className={error ? "error" : undefined}>{error || summary}</p>
          </section>
        )}
      </section>
    </main>
  );
}

export default App;
