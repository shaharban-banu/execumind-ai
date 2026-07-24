import { useEffect, useState } from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge, StatusDot } from '../components/ui/Badge';
import { Sparkline, AreaChart} from '../components/ui/Charts';
import { Skeleton } from '../components/ui/Feedback';

import {
  getKpis,
  getRevenueTrend,
  getExecutiveActivity,
  getSystemStatus,
  getSegmentMix,
  getDashboardSummary,
  getRevenueHistory,
} from "../lib/api";
import type { Kpi, ExecutiveActivity, SystemStatusItem, MetricTrend, SeriesPoint } from '../lib/types';
import { formatRelativeTime, cn } from '../lib/utils';
import type { PageId } from '../components/layout/Sidebar';

const accentMap = {
  brand: { text: 'text-brand-600', bg: 'bg-brand-50', stroke: '#2563eb' },
  emerald: { text: 'text-emerald-600', bg: 'bg-emerald-50', stroke: '#10b981' },
  amber: { text: 'text-amber-600', bg: 'bg-amber-50', stroke: '#f59e0b' },
  accent: { text: 'text-accent-600', bg: 'bg-accent-50', stroke: '#06b6d4' },
} as const;

const statusConfig = {
  operational: { variant: 'emerald' as const, label: 'Operational', dot: 'emerald' as const },
  degraded: { variant: 'amber' as const, label: 'Degraded', dot: 'amber' as const },
  down: { variant: 'rose' as const, label: 'Down', dot: 'rose' as const },
};

export function DashboardPage({ onNavigate }: { onNavigate: (p: PageId) => void }) {
  const [kpis, setKpis] = useState<Kpi[]>([]);
  const [activity, setActivity] = useState<ExecutiveActivity[]>([]);
  const [systemStatus, setSystemStatus] = useState<SystemStatusItem[]>([]);
  const [revenueHistory, setRevenueHistory] = useState<any[]>([]);
  const [segments, setSegments] = useState<SeriesPoint[]>([]);
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState<any>(null);
  const [summaryLoading, setSummaryLoading] = useState(true);
  const latestRevenue =
  revenueHistory.length > 2
    ? revenueHistory[revenueHistory.length - 3]
    : null;

  useEffect(() => {
  const load = async () => {
    try {
      const [
        kpis,
        activity,
        status,
        revenueHistory,
        segments,
        summary,
      ] = await Promise.all([
        getKpis(),
        getExecutiveActivity(),
        getSystemStatus(),
        getRevenueHistory(),
        getSegmentMix(),
        getDashboardSummary(),
      ]);
      console.log("Revenue API:", revenueHistory);
      console.log("Summary API:", summary);
      setKpis(kpis);
      setActivity(activity);
      setSystemStatus(status);
      setRevenueHistory(revenueHistory);
      setSegments(segments);
      try {
        const summary = await getDashboardSummary();
        setSummary(summary);
      } catch (err) {
        console.error("Summary failed:", err);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
      setSummaryLoading(false);
    }
  };

  load();
}, []);

  const monthLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const operationalCount = systemStatus.filter((s) => s.status === 'operational').length;

  console.log("Revenue History:", revenueHistory);
  return (
    <div className="space-y-6">
      {/* Hero banner */}
      <div className="overflow-hidden rounded-2xl border border-brand-100 bg-gradient-to-br from-brand-50 via-white to-accent-50/40 p-6">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="max-w-2xl">
            <div className="mb-2 flex items-center gap-2">
              <Badge variant="brand" tone="soft" dot>AI Briefing · {new Date().toLocaleDateString('en-US', { weekday: 'long' })}</Badge>
              <Badge variant="emerald" tone="soft" dot>{operationalCount}/{systemStatus.length || 6} systems operational</Badge>
            </div>
            <h2 className="font-display text-xl font-bold text-slate-900 md:text-2xl">
              Hai.., Shah. Here's your executive snapshot.
            </h2>
            <p className="mt-1.5 text-sm leading-relaxed text-slate-600">
              Revenue is trending <span className="font-semibold text-emerald-600">+12.4%</span> with order volume up <span className="font-semibold text-emerald-600">+8.2%</span>.
              All core agents are operational and processing overnight signals.
            </p>
          </div>
          <div className="flex shrink-0 gap-2.5">
            <button
              onClick={() => onNavigate('advisor')}
              className="inline-flex h-10 items-center gap-2 rounded-xl bg-brand-600 px-4 text-sm font-medium text-white shadow-sm shadow-brand-600/25 transition hover:bg-brand-700"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 3v4M3 5h4M6 17v4M4 19h4M13 3l3.5 9L13 21M11 3l-3.5 9L11 21" />
              </svg>
              Ask Advisor
            </button>
            <button
              onClick={() => onNavigate('forecast')}
              className="inline-flex h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 17l6-6 4 4 7-7M17 8h4v4" />
              </svg>
              Forecast
            </button>
          </div>
        </div>
      </div>

      {/* KPI cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {loading
          ? Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-[140px] rounded-2xl" />)
          : kpis.map((kpi) => {
              const a = accentMap[kpi.accent];
              return (
                <Card key={kpi.id} hover className="animate-fade-in p-5">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-xs font-medium text-slate-500">{kpi.label}</p>
                      <p className="mt-1 font-display text-2xl font-bold text-slate-900">{kpi.value}</p>
                    </div>
                    <span className={cn('flex h-10 w-10 items-center justify-center rounded-xl', a.bg, a.text)}>
                      <KpiIcon icon={kpi.icon} />
                    </span>
                  </div>
                  <div className="mt-3 flex items-end justify-between gap-3">
                    <div>
                      <div className={cn('inline-flex items-center gap-1 text-xs font-semibold', kpi.changePct > 0 ? 'text-emerald-600' : kpi.changePct < 0 ? 'text-rose-600' : 'text-slate-500')}>
                        {kpi.trend === 'up' ? (
                          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M7 17l5-5 5 5" /></svg>
                        ) : kpi.trend === 'down' ? (
                          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M7 7l5 5 5-5" /></svg>
                        ) : (
                          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14" /></svg>
                        )}
                        {kpi.changePct > 0 ? '+' : ''}{kpi.changePct}%
                      </div>
                      <p className="mt-0.5 text-[11px] text-slate-400">vs last month</p>
                    </div>
                    <Sparkline data={kpi.spark} color={a.stroke} className="h-9 w-24" />
                  </div>
                </Card>
              );
            })}
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader
            title="Revenue"
            subtitle="Historical monthly revenue"
            icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M3 17l6-6 4 4 7-7M17 8h4v4" /></svg>}
            action={<Badge variant="emerald" tone="soft">+12.4% YoY</Badge>}
          />
          <div className="px-5 pt-2">
            <p className="text-2xl font-bold text-slate-900">
              ${latestRevenue ? latestRevenue.value.toLocaleString() : "--"}
            </p>

            <p className="text-sm text-slate-500">
              Latest monthly revenue
            </p>
          </div>
          <div className="px-3 pb-4 pt-2">
            {revenueHistory.length > 0  ? (
              <AreaChart
                labels={revenueHistory.map((r) => r.label)}
                series={revenueHistory.map((r) => r.value)}
              />
            ) : (
              <Skeleton className="h-[260px]" />
            )}
          </div>
        </Card>

        <Card>
          <CardHeader
            title="Executive Briefing"
            subtitle="AI-generated business summary"
            icon={
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z" />
              </svg>
            }
            action={
              <Badge variant="brand" tone="soft">
                Executive Agent
              </Badge>
            }
          />
          <div className="space-y-4 px-5 py-5">
            {summaryLoading ? (
              <p className="text-sm text-slate-500">
                Generating executive briefing...
              </p>
            ) : (
              <>
                <div className="rounded-xl bg-slate-50 p-3">
                  <p className="text-xs font-semibold uppercase text-slate-600">
                    Executive Summary
                  </p>
                  <p className="mt-1 text-sm text-slate-700">
                    {summary?.executive_summary}
                  </p>
                </div>

                <div className="rounded-xl bg-emerald-50 p-3">
                  <p className="text-xs font-semibold uppercase text-emerald-700">
                    Opportunity
                  </p>
                  <p className="mt-1 text-sm text-slate-700">
                    {summary?.opportunity}
                  </p>
                </div>

                <div className="rounded-xl bg-amber-50 p-3">
                  <p className="text-xs font-semibold uppercase text-amber-700">
                    Risk
                  </p>
                  <p className="mt-1 text-sm text-slate-700">
                    {summary?.risk}
                  </p>
                </div>

                <div className="rounded-xl bg-blue-50 p-3">
                  <p className="text-xs font-semibold uppercase text-blue-700">
                    Recommendation
                  </p>
                  <p className="mt-1 text-sm font-medium text-slate-700">
                    {summary?.recommendation?.action}
                  </p>
                  <p className="mt-2 text-xs text-slate-500">
                    {summary?.recommendation?.rationale}
                  </p>
                </div>
              </>
            )}
          </div>
        </Card>
      </div>

      {/* Executive Activity + System Status row */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        {/* Executive Activity panel */}
        <Card className="lg:col-span-2">
          <CardHeader
            title="Recent Executive Activity"
            subtitle="Agent actions and platform events"
            icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></svg>}
          />
          <div className="px-5 py-3">
            {loading
              ? Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} className="my-2.5 h-14" />)
              : activity.map((a, i) => (
                  <div key={a.id} className="flex gap-3 py-3">
                    <div className="relative">
                      <div className={cn('flex h-9 w-9 items-center justify-center rounded-xl', activityIconBg(a.type))}>
                        <ActivityIcon type={a.type} />
                      </div>
                      {i < activity.length - 1 && <div className="absolute left-1/2 top-9 h-[calc(100%-12px)] w-px -translate-x-1/2 bg-slate-100" />}
                    </div>
                    <div className="min-w-0 flex-1 pb-1">
                      <div className="flex items-center gap-2">
                        <p className="text-sm font-medium text-slate-800">{a.label}</p>
                      </div>
                      <p className="mt-0.5 text-xs text-slate-500">{a.detail}</p>
                      <div className="mt-1 flex items-center gap-2">
                        {a.actor && (
                          <span className="inline-flex items-center gap-1 rounded-md bg-slate-100 px-1.5 py-0.5 text-[10px] font-medium text-slate-500">
                            <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><rect x="4" y="8" width="16" height="12" rx="2" /><path d="M12 8V4" /><circle cx="12" cy="3" r="1" /></svg>
                            {a.actor}
                          </span>
                        )}
                        <span className="text-[11px] text-slate-400">{formatRelativeTime(a.timestamp)}</span>
                      </div>
                    </div>
                  </div>
                ))}
          </div>
        </Card>

        {/* System Status panel */}
        <Card>
          <CardHeader
            title="System Status"
            subtitle={`${operationalCount} of ${systemStatus.length || 6} operational`}
            icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2" /></svg>}
            action={
              <span className={cn(
                'inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium',
                operationalCount === systemStatus.length ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'
              )}>
                <StatusDot variant={operationalCount === systemStatus.length ? 'emerald' : 'amber'} pulse />
                {operationalCount === systemStatus.length ? 'All Systems Go' : 'Partial'}
              </span>
            }
          />
          <div className="divide-y divide-slate-100 px-5 py-1">
            {loading
              ? Array.from({ length: 6 }).map((_, i) => <Skeleton key={i} className="my-2.5 h-12" />)
              : systemStatus.map((s) => {
                  const sc = statusConfig[s.status];
                  return (
                    <div key={s.id} className="flex items-center gap-3 py-3">
                      <div className={cn(
                        'flex h-9 w-9 shrink-0 items-center justify-center rounded-xl',
                        s.status === 'operational' ? 'bg-emerald-50 text-emerald-600' : s.status === 'degraded' ? 'bg-amber-50 text-amber-600' : 'bg-rose-50 text-rose-600'
                      )}>
                        <SystemIcon id={s.id} />
                      </div>
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-2">
                          <p className="text-sm font-medium text-slate-800">{s.label}</p>
                          <StatusDot variant={sc.dot} pulse={s.status !== 'operational'} />
                        </div>
                        <p className="truncate text-xs text-slate-500">{s.detail}</p>
                      </div>
                      <div className="shrink-0 text-right">
                        <p className="text-xs font-medium text-slate-600">{s.latency}</p>
                        <p className="text-[10px] text-slate-400">{formatRelativeTime(s.lastChecked)}</p>
                      </div>
                    </div>
                  );
                })}
          </div>
          {systemStatus.some((s) => s.status === 'degraded') && (
            <div className="mx-5 mb-4 mt-1 flex items-center gap-2 rounded-xl bg-amber-50 px-3 py-2.5 text-xs text-amber-700">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 9v4M12 17h.01" /><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z" /></svg>
              Data Agent is processing a large dataset — response times may be elevated.
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

function KpiIcon({ icon }: { icon: Kpi['icon'] }) {
  switch (icon) {
    case 'revenue':
      return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>;
    case 'orders':
      return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z" /><path d="M3 6h18M16 10a4 4 0 0 1-8 0" /></svg>;
    case 'customers':
      return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" /></svg>;
    case 'aov':
      return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 12V8H6a2 2 0 0 1-2-2c0-1.1.9-2 2-2h12v4" /><path d="M4 6v12a2 2 0 0 0 2 2h14v-4" /><path d="M18 12a2 2 0 0 0-2 2c0 1.1.9 2 2 2h4v-4h-4z" /></svg>;
  }
}

function activityIconBg(type: ExecutiveActivity['type']): string {
  const map: Record<ExecutiveActivity['type'], string> = {
    agent: 'bg-brand-50 text-brand-600',
    forecast: 'bg-accent-50 text-accent-600',
    upload: 'bg-slate-100 text-slate-500',
    decision: 'bg-emerald-50 text-emerald-600',
    alert: 'bg-rose-50 text-rose-600',
    scenario: 'bg-amber-50 text-amber-600',
    insight: 'bg-brand-50 text-brand-600',
  };
  return map[type] ?? 'bg-slate-100 text-slate-500';
}

function ActivityIcon({ type }: { type: ExecutiveActivity['type'] }) {
  const icons: Record<ExecutiveActivity['type'], React.ReactNode> = {
    agent: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="4" y="8" width="16" height="12" rx="2" /><path d="M12 8V4" /><circle cx="12" cy="3" r="1" /><path d="M9 13h.01M15 13h.01M9 17h6" /></svg>,
    forecast: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M3 17l6-6 4 4 7-7" /></svg>,
    upload: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 9l5-5 5 5M12 4v12" /></svg>,
    decision: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M9 11l3 3 8-8" /><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" /></svg>,
    alert: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 9v4M12 17h.01" /><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z" /></svg>,
    scenario: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v4M12 18v4M4.9 4.9l2.8 2.8M16.3 16.3l2.8 2.8M2 12h4M18 12h4" /></svg>,
    insight: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="3" /><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2" /></svg>,
  };
  return icons[type] ?? icons.agent;
}

function SystemIcon({ id }: { id: SystemStatusItem['id'] }) {
  const icons: Record<SystemStatusItem['id'], React.ReactNode> = {
    dataset: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><ellipse cx="12" cy="5" rx="9" ry="3" /><path d="M3 5v14a9 3 0 0 0 18 0V5" /><path d="M3 12a9 3 0 0 0 18 0" /></svg>,
    planner: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M9 11l3 3 8-8" /><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" /></svg>,
    customer: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /></svg>,
    data: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 7h16M4 12h16M4 17h10" /><circle cx="19" cy="17" r="2" /></svg>,
    forecast: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M3 17l6-6 4 4 7-7M17 8h4v4" /></svg>,
    api: <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M16 18l6-6-6-6M8 6l-6 6 6 6" /></svg>,
  };
  return icons[id] ?? icons.api;
}
