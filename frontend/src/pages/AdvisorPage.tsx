import { useEffect, useState } from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { ConfidenceRing } from '../components/ui/Charts';
import { Skeleton, EmptyState } from '../components/ui/Feedback';
import {
    getExecutiveReport,
    generateExecutiveReport,
} from "../lib/api";
import type { AiRecommendation, IntelligenceItem, DecisionStatus, IntelligenceCategory } from '../lib/types';
import { formatRelativeTime, cn } from '../lib/utils';
import type { ExecutiveReport } from "../lib/types";

const statusConfig: Record<DecisionStatus, { variant: 'brand' | 'emerald' | 'rose' | 'amber'; label: string }> = {
  pending: { variant: 'amber', label: 'Pending' },
  approved: { variant: 'emerald', label: 'Approved' },
  rejected: { variant: 'rose', label: 'Rejected' },
  monitoring: { variant: 'brand', label: 'Monitoring' },
};

const severityVariant = { critical: 'rose', high: 'amber', medium: 'brand', low: 'slate' } as const;
const categoryFilters: (IntelligenceCategory | 'All')[] = ['All', 'Market', 'Risk', 'Operations', 'Finance', 'Competitor'];

export function AdvisorPage() {
  const [report, setReport] = useState<ExecutiveReport | null>(null);
  const [intel, setIntel] = useState<IntelligenceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<IntelligenceCategory | 'All'>('All');
  const [expanded, setExpanded] = useState<string | null>(null);
  const [localStatus, setLocalStatus] = useState<Record<string, DecisionStatus>>({});

  useEffect(() => {
    async function load() {
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
    }

    load();
}, []);

  const filtered = [];
  const pendingCount = 0;

  function updateStatus(id: string, status: DecisionStatus) {
    setLocalStatus((s) => ({ ...s, [id]: status }));
  }

  return (
    <div className="space-y-6">
      {/* Advisor summary banner */}
      <Card className="overflow-hidden border-brand-100">
        <div className="flex flex-col gap-4 bg-gradient-to-br from-brand-50/80 via-white to-white p-6 md:flex-row md:items-center md:justify-between">
          <div className="flex items-start gap-4">
            <div className="relative flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 shadow-lg shadow-brand-600/30">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 3v4M3 5h4M6 17v4M4 19h4M13 3l3.5 9L13 21M11 3l-3.5 9L11 21" />
              </svg>
              <span className="absolute -right-0.5 -top-0.5 h-3 w-3 rounded-full border-2 border-white bg-emerald-400" />
            </div>
            <div>
              <h2 className="font-display text-lg font-bold text-slate-900">AI Executive Advisor</h2>
              <p className="mt-0.5 text-sm text-slate-600">
                Executive report generated using Customer Intelligence,
                Data Intelligence, and Forecast Intelligence.
              </p>
            </div>
          </div>
          <div className="flex gap-6">
            <Metric
              label="Recommendations"
              value={report ? report.strategic_recommendations.length.toString() : "0"}
              color="text-amber-600"
            />

            <Metric
              label="Business Risks"
              value={report ? report.business_risks.length.toString() : "0"}
              color="text-rose-600"
            />

            <Metric
              label="Key Findings"
              value={report ? report.key_findings.length.toString() : "0"}
              color="text-brand-600"
            />
          </div>
        </div>
      </Card>
      {/* Temporary Debug */}
      {report && (
        <Card className="overflow-hidden border-brand-100">
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

          <p className="text-slate-700 leading-8 text-[16px]">
            {report.executive_summary}
          </p>

        </div>
      </Card>
      )}  
      {report && (
        <Card className="p-6">
          <h2 className="text-xl font-bold mb-4">
            Key Findings
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
          <h2 className="text-xl font-bold mb-4 text-red-600">
            Business Risks
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
          <h2 className="text-xl font-bold mb-6">
            Strategic Recommendations
          </h2>

          <div className="space-y-4">
            {report.strategic_recommendations.map((rec, index) => (
              <div
                key={index}
                className="rounded-xl border border-slate-200 p-5 hover:border-blue-300 transition"
              >
                <div className="flex items-center justify-between">

                  <span
                    className={`px-3 py-1 rounded-full text-sm font-semibold
                    ${
                      rec.priority === "High"
                        ? "bg-red-100 text-red-700"
                        : rec.priority === "Medium"
                        ? "bg-amber-100 text-amber-700"
                        : "bg-green-100 text-green-700"
                    }`}
                  >
                    {rec.priority}
                  </span>

                </div>

                <h3 className="mt-4 text-lg font-semibold">
                  {rec.action}
                </h3>

                <p className="mt-2 text-slate-600">
                  {rec.rationale}
                </p>

              </div>
            ))}
          </div>
        </Card>
      )}
      {report && (
      <Card className="p-6">
        <h2 className="text-xl font-bold mb-6">
          Supporting Evidence
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
  );
}

function Metric({ label, value, color }: { label: string; value: string; color: string }) {
  return (
    <div className="text-center">
      <p className={cn('font-display text-xl font-bold', color)}>{value}</p>
      <p className="text-[11px] uppercase tracking-wider text-slate-400">{label}</p>
    </div>
  );
}
