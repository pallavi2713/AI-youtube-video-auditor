"use client";

import { useState } from "react";

interface ComplianceResult {
  category: string;
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  evidence_type: "TRANSCRIPT" | "VIDEO" | "TRANSCRIPT_AND_VIDEO";
  start_time: string;
  end_time: string;
  evidence: string;
  rule: string;
  description: string;
  recommendation: string;
  confidence: number;
}

interface AuditResponse {
  session_id: string;
  video_id: string;
  compliance_results: ComplianceResult[];
  status: "PASS" | "FAIL";
  final_report: string;
}

export default function Home() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<AuditResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [openIssue, setOpenIssue] = useState<number | null>(null);

  const handleAudit = async () => {
    if (!url.trim()) {
      setError("Please enter a video URL.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    setOpenIssue(null);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/audit`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            video_url: url.trim(),
          }),
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || "Audit failed");
      }

      const data: AuditResponse = await response.json();

      setResult(data);
    } catch (error) {
      console.error(error);

      setError(
        "Unable to audit the video. Please check the URL and backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const toggleIssue = (index: number) => {
    setOpenIssue(openIssue === index ? null : index);
  };

  return (
    <main className="container">

      {/* HEADER */}

      <header className="header">

       

        <div>
          <h1>YouTube Ad Compliance & Claims Auditor</h1>

          <p>
            AI-powered video compliance analysis
          </p>
        </div>

      </header>


      {/* INPUT */}

      <section className="input-section">

        <input
          type="url"
          placeholder="Paste YouTube video URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleAudit();
            }
          }}
        />

        <button
          onClick={handleAudit}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Audit Video"}
        </button>

      </section>


      {/* ERROR */}

      {error && (
        <div className="error">
          {error}
        </div>
      )}


      {/* LOADING */}

      {loading && (
        <section className="loading">

          <div className="spinner"></div>

          <h3>
            Analyzing video
          </h3>

          <p>
            Checking transcript, video content and
            compliance rules.
          </p>

          <span>
            This may take a few minutes.
          </span>

        </section>
      )}


      {/* RESULTS */}

      {result && !loading && (

        <section className="results">

          {/* FINAL REPORT FIRST */}

          <div className="report-card">

            <div className="report-header">

              <div>
                <span className="eyebrow">
                  AUDIT REPORT
                </span>

                <h2>
                  Final Report
                </h2>
              </div>

              <div
                className={`status-badge ${
                  result.status === "PASS"
                    ? "status-pass"
                    : "status-fail"
                }`}
              >
                {result.status === "PASS"
                  ? "✓ COMPLIANT"
                  : "✕ FAIL"}
              </div>

            </div>

            <p className="report-text">
              {result.final_report}
            </p>

            <div className="report-meta">

          

            </div>

          </div>


          {/* ISSUES */}

          <div className="issues-header">

            <div>
              <span className="eyebrow">
                FINDINGS
              </span>

              <h2>
                Compliance Issues
              </h2>
            </div>

            <span className="issue-count">
              {result.compliance_results.length}
              {" "}
              {result.compliance_results.length === 1
                ? "Issue"
                : "Issues"}
            </span>

          </div>


          {/* ISSUE CARDS */}

          {result.compliance_results.length === 0 ? (

            <div className="no-results">
              <span className="success-icon">
                ✓
              </span>

              <div>
                <strong>
                  No compliance issues found
                </strong>

                <p>
                  The video passed the available compliance checks.
                </p>
              </div>
            </div>

          ) : (

            <div className="issues-list">

              {result.compliance_results.map(
                (item, index) => {

                  const isOpen =
                    openIssue === index;

                  return (

                    <div
                      className={`issue-card ${
                        isOpen ? "issue-open" : ""
                      }`}
                      key={index}
                    >

                      {/* ISSUE HEADER */}

                      <button
                        className="issue-header"
                        onClick={() =>
                          toggleIssue(index)
                        }
                      >

                        <div className="issue-number">
                          {String(index + 1).padStart(2, "0")}
                        </div>


                        <div className="issue-title">

                          <h3>
                            {item.category}
                          </h3>

                          <span>
                            {item.evidence_type}
                            {" • "}
                            {item.start_time}
                            {" → "}
                            {item.end_time}
                          </span>

                        </div>


                        <span
                          className={`severity ${item.severity.toLowerCase()}`}
                        >
                          {item.severity}
                        </span>


                        <span className="arrow">
                          {isOpen ? "−" : "+"}
                        </span>

                      </button>


                      {/* DETAILS */}

                      {isOpen && (

                        <div className="issue-details">

                          <div className="detail-grid">

                            {/* EVIDENCE */}

                            <div className="detail-block">

                              <span className="detail-label">
                                EVIDENCE
                              </span>

                              <p>
                                {item.evidence}
                              </p>

                            </div>


                            {/* RULE */}

                            <div className="detail-block">

                              <span className="detail-label">
                                COMPLIANCE RULE
                              </span>

                              <p>
                                {item.rule}
                              </p>

                            </div>


                            {/* DESCRIPTION */}

                            <div className="detail-block">

                              <span className="detail-label">
                                DESCRIPTION
                              </span>

                              <p>
                                {item.description}
                              </p>

                            </div>


                            {/* RECOMMENDATION */}

                            <div className="detail-block recommendation">

                              <span className="detail-label">
                                RECOMMENDATION
                              </span>

                              <p>
                                {item.recommendation}
                              </p>

                            </div>

                          </div>


                          <div className="issue-footer">

                            <div>
                              <span>
                                Timestamp
                              </span>

                              <strong>
                                {item.start_time}
                                {" → "}
                                {item.end_time}
                              </strong>
                            </div>


                            <div>
                              <span>
                                Confidence
                              </span>

                              <strong>
                                {(item.confidence * 100).toFixed(0)}%
                              </strong>
                            </div>

                          </div>

                        </div>

                      )}

                    </div>

                  );
                }
              )}

            </div>

          )}

        </section>

      )}

    </main>
  );
}