import { useEffect, useState } from 'react';
import { Card } from "../components/ui/Card";
import {
    getExecutiveReport,
    generateExecutiveReport,
} from "../lib/api";
import { Button } from "../components/ui/Button";

import type { ExecutiveReport } from "../lib/types";

export function AdvisorPage() {
  const [report, setReport] = useState<ExecutiveReport | null>(null);
  const [loading,setLoading] = useState(true);
  const [showAllRecommendations, setShowAllRecommendations] = useState(false);
  

  useEffect(() => {
    async function load() {
        try {
            setLoading(true);

            const data = await getExecutiveReport();

            setReport(data);

        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    }

    load();
}, []);

const handleGenerateReport = async () => {
    try {
        setLoading(true);

        await generateExecutiveReport();

        const data = await getExecutiveReport();

        setReport(data);
    } catch (err) {
        console.error(err);
    } finally {
        setLoading(false);
    }
};

const displayedRecommendations = showAllRecommendations
  ? report?.strategic_recommendations ?? []
  : report?.strategic_recommendations.slice(0, 4) ?? [];



if (loading) {
    return (
    <div className="space-y-6">
      <Card className="p-8">
        <p className="text-slate-500">Generating executive report...</p>
      </Card>
    </div>
  );
  }
  return (
    <div className="mx-auto max-w-7xl">
      {/* Advisor summary banner */}
      <Card className=" overflow-hidden border-brand-100">
        <div className="flex flex-col gap-4 bg-gradient-to-br from-brand-50/80 via-white to-white p-6 md:flex-row md:items-center md:justify-between">
          <div className="flex items-start gap-4">
            <div className="relative flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 shadow-lg shadow-brand-600/30">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 3v4M3 5h4M6 17v4M4 19h4M13 3l3.5 9L13 21M11 3l-3.5 9L11 21" />
              </svg>
              <span className="absolute -right-0.5 -top-0.5 h-3 w-3 rounded-full border-2 border-white bg-emerald-400" />
            </div>
            <div>
              <h2 className="font-display text-lg font-bold text-slate-900">Executive Decision Report</h2>
              <p className="mt-0.5 text-sm text-slate-600">
                Executive report generated using Customer Intelligence,
                Data Intelligence, and Forecast Intelligence.
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Last Updated •{" "}
                {report?.generated_at &&
                  `${new Date(report.generated_at).toLocaleDateString()} • ${new Date(
                    report.generated_at
                  ).toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}`}
              </p>
            </div>
          </div>
          <div className="flex flex-col items-end gap-4">

            <Button
              onClick={handleGenerateReport}
              disabled={loading}
            >
              {loading ? "Generating..." : "🔄 Generate New Report"}
            </Button>
            <div className="grid grid-cols-3 gap-4">

              <div className="rounded-xl bg-amber-50 border border-amber-200 px-6 py-4 text-center">
                <p className="text-3xl font-bold text-amber-600">
                  {report?.strategic_recommendations.length ?? 0}
                </p>
                <p className="mt-1 text-xs font-medium uppercase tracking-wider text-slate-500">
                  Recommendations
                </p>
              </div>

              <div className="rounded-xl bg-rose-50 border border-rose-200 px-6 py-4 text-center">
                <p className="text-3xl font-bold text-rose-600">
                  {report?.business_risks.length ?? 0}
                </p>
                <p className="mt-1 text-xs font-medium uppercase tracking-wider text-slate-500">
                  Business Risks
                </p>
              </div>

              <div className="rounded-xl bg-blue-50 border border-blue-200 px-6 py-4 text-center">
                <p className="text-3xl font-bold text-blue-600">
                  {report?.key_findings.length ?? 0}
                </p>
                <p className="mt-1 text-xs font-medium uppercase tracking-wider text-slate-500">
                  Key Findings
                </p>
              </div>

            </div>
          </div>
        </div>
      </Card>
      {/* Temporary Debug */}
      <div className="space-y-8">
      {report && (
        <Card className="mt-8 overflow-hidden border-brand-100">
        <div className="bg-gradient-to-r from-brand-50 via-white to-white p-8">

          <div className="flex items-center gap-3 mb-6">

            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-600 text-white text-xl">
              📋
            </div>

            <div>
              <h2 className="text-2xl font-bold text-slate-900">
                Executive Summary
              </h2>

              <p className="text-sm text-slate-500">
                AI-generated business overview
              </p>
            </div>

          </div>

          <p className="mt-5 text-[15px] leading-8 text-slate-700 max-w-5xl">
            {report.executive_summary}
          </p>

        </div>
      </Card>
      )}  
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

        {/* Left Column */}
        <div className="space-y-8">
          {report && (
            <Card className="p-6">
              <h2 className="text-xl font-bold mb-4 text-red-600">
                ⚠ Business Risks
              </h2>

              <ul className="space-y-3">
                {report.business_risks.map((risk, index) => (
                  <li
                    key={index}
                    className="flex items-center gap-3"
                  >
                    ⚠️ {risk}
                  </li>
                ))}
              </ul>
            </Card>
          )}
          {report && (
            <Card className="p-6">
              <h2 className="text-xl font-semibold tracking-tight text-slate-900">
                📊 Key Findings
              </h2>

              <ul className="space-y-3">
                {report.key_findings.map((item, index) => (
                  <li
                    key={index}
                    className="flex items-center gap-3"
                  >
                    <span className="text-blue-600">•</span>
                    {item}
                  </li>
                ))}
              </ul>
            </Card>
          )}
          {report && (
            <Card className="p-6">
              <h2 className="text-xl font-semibold tracking-tight text-slate-900">
                📄 Supporting Evidence
              </h2>

              <div className="space-y-4">
                {report.evidence.map((item, index) => (
                  <div
                    key={index}
                    className="border-l-4 border-blue-500 bg-slate-50 p-4 rounded-r-lg"
                  >
                    <h3 className="font-semibold">
                      {item.source}
                    </h3>

                    <p className="text-sm text-slate-500 mb-2">
                      {item.reference}
                    </p>

                    <p className="text-slate-700">
                      {item.text}
                    </p>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>
        {/* Right Column */}
        <div className="xl:col-span-2 space-y-8">
          {report && (
            <Card className="p-7">
              <h2 className="text-xl font-semibold tracking-tight text-slate-900">
                🎯 Strategic Recommendations
              </h2>

              <p className="text-sm text-slate-500 mb-6">
                Prioritized actions generated by the Executive Intelligence Agent.
              </p>

              <div className="space-y-6">
                {displayedRecommendations.map((rec, index) => (
                  <div
                    key={index}
                    className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition"
                  >
                    <div className="flex items-center justify-between">
                      <span
                        className={`px-4 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                          rec.priority === "High"
                            ? "bg-red-100 text-red-700"
                            : rec.priority === "Medium"
                            ? "bg-amber-100 text-amber-700"
                            : "bg-emerald-100 text-emerald-700"
                        }`}
                      >
                        {rec.priority} Priority
                      </span>
                    </div>

                    <h3 className="mt-4 text-lg font-semibold">
                      {rec.action}
                    </h3>

                    <p className="mt-2 leading-7 text-slate-600">
                      {rec.rationale}
                    </p>
                  </div>
                ))}
              </div>

              {report.strategic_recommendations.length > 3 && (
                <div className="mt-6 text-center">
                  <button
                    onClick={() =>
                      setShowAllRecommendations(!showAllRecommendations)
                    }
                    className="text-brand-600 font-medium hover:underline"
                  >
                    {showAllRecommendations
                      ? "Show Less"
                      : `View All Recommendations (${report.strategic_recommendations.length})`}
                  </button>
                </div>
              )}
            </Card>
          )}
          
        </div>
      </div>
    </div>
  </div>
  )}
  


