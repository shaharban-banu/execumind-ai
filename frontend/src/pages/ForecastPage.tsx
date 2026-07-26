import { useEffect, useState } from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

import { Skeleton } from '../components/ui/Feedback';
import { getForecast } from '../lib/api';
import type { ForecastResult } from '../lib/types';
import { cn } from '../lib/utils';


export function ForecastPage() {
  const [forecast, setForecast] = useState<ForecastResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getForecast().then((d) => { setForecast(d); setLoading(false); });
  }, []);
  const maxForecast = forecast ? Math.max(...forecast.points.map((p) => Math.max(p.historical ?? 0, p.forecast ?? 0))) : 100;
 
return (
    <div className="space-y-6">
      {/* Forecast hero with model metadata */}
      <Card className="overflow-hidden border-brand-100">
        <div className="flex flex-col gap-4 bg-gradient-to-br from-brand-50/80 via-white to-accent-50/40 p-6 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="mb-2 flex items-center gap-2">
              <Badge variant="brand" tone="soft" dot>Validated Forecast Model</Badge>
              {forecast && <Badge variant="slate" tone="outline">{forecast.metrics.model}</Badge>}
            </div>
            <h2 className="font-display text-lg font-bold text-slate-900">Q4 Revenue Forecast</h2>
            <p className="mt-1 text-sm text-slate-600">
              6-month forward projection using Prophet forecasting.
            </p>
          </div>
          <div className="flex gap-6">
            <Metric
              label="Forecast Error"
              value={
                forecast
                  ? `${forecast.metrics.mape.toFixed(2)}%`
                  : "—"
              }
              color="text-amber-600"
            />
            <Metric
              label="Confidence"
              value={
                forecast
                  ? `${forecast.metrics.confidenceLevel} (${forecast.metrics.confidence})`
                  : "—"
              }
              color="text-blue-600"
            />
            <Metric
              label="Forecast Horizon"
              value={
                forecast
                  ? `${forecast.metrics.horizonMonths} Months`
                  : "—"
              }
              color="text-purple-600"
            />
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Forecast chart */}
        <Card className="lg:col-span-2">
          <CardHeader
            title="Forecast Trajectory"
            subtitle="Historical vs projected with confidence band"
            icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M3 17l6-6 4 4 7-7M17 8h4v4" /></svg>}
            action={
              <div className="flex items-center gap-3 text-xs">
                <span className="flex items-center gap-1.5"><span className="h-2.5 w-2.5 rounded-full bg-brand-500" /> Historical</span>
                <span className="flex items-center gap-1.5"><span className="h-2.5 w-2.5 rounded-full bg-accent-500" /> Forecast</span>
              </div>
            }
          />
          <div className="px-4 pb-5 pt-3">
            {loading || !forecast ? (
              <Skeleton className="h-[280px]" />
            ) : (
             <ForecastChart
                points={forecast.points}
                max={maxForecast}
            />
            )}
          </div>
        </Card>

        {/* Drivers */}
        <Card>
          <CardHeader
            title="Key Drivers"
            subtitle="Factors influencing the forecast"
            icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="3" /><path d="M19 12a7 7 0 0 1-14 0M12 5v2M12 17v2M5 12H3M21 12h-2" /></svg>}
          />
          <div className="px-5 py-4">
            {loading || !forecast ? (
              <div className="space-y-3">
                {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-8" />)}
              </div>
            ) : (
              <div className="space-y-4">
                {forecast.drivers.map((driver) => (
                  <div
                    key={driver.name}
                    className="flex items-start justify-between border-b border-slate-100 pb-3 last:border-b-0"
                  >
                    <div>
                      <p className="font-medium text-slate-800">
                        {driver.name}
                      </p>

                      <p className="text-xs text-slate-500 mt-1">
                        {driver.description}
                      </p>
                    </div>

                    <div className="text-right">
                      <p className="font-semibold text-slate-700">
                        {driver.impact}
                      </p>

                      <p className="text-xs mt-1">
                        {driver.direction === "up"
                          ? "↗ Positive"
                          : driver.direction === "down"
                          ? "↘ Negative"
                          : "→ Stable"}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </Card>
      </div>
      <Card>
        <CardHeader
          title="Forecast Insights"
          subtitle="AI-generated interpretation of the forecast"
          icon={
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M9 12l2 2 4-4" />
              <circle cx="12" cy="12" r="9" />
            </svg>
          }
        />

        <div className="space-y-5 px-5 pb-5">
          <div className="mt-6 rounded-xl border border-blue-200 bg-blue-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-blue-700">
              Forecast Trend
            </p>

            <p className="mt-2 text-sm leading-6 text-slate-700">
              {forecast?.insights.trend}
            </p>
          </div>
          <div className="rounded-xl border border-red-100 bg-red-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-red-600">
              Forecast Risk
            </p>

            <p className="mt-1 text-sm text-slate-700">
              {forecast?.insights.risk}
            </p>
          </div>
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-brand-700">
              Recommendation
            </p>

            <p className="mt-1 text-sm text-slate-700">
              {forecast?.insights.recommendation}
            </p>
          </div>
        </div>
      </Card>

    </div>
  );
}

function ForecastChart({
  points,
  max,
}: {
  points: ForecastResult['points'];
  max: number;
}) {
  const w = 680;
  const h = 280;
  const padL = 36;
  const padB = 26;
  const padR = 12;
  const padT = 12;
  const innerW = w - padL - padR;
  const innerH = h - padT - padB;
  const step = innerW / (points.length - 1);
  const yFor = (v: number) => padT + innerH - (v / max) * innerH;

  const histPts = points.filter((p) => p.historical !== null);
  const fcPts = points.filter((p) => p.forecast !== null);
  const lastHist = histPts[histPts.length - 1];
  const firstFc = fcPts[0];

  const histLine = histPts.map((p, i) => {
    const idx = points.indexOf(p);
    return `${i === 0 ? 'M' : 'L'} ${padL + idx * step} ${yFor(p.historical!)}`;
  }).join(' ');

  const fcStart = lastHist ? points.indexOf(lastHist) : 0;
  const fcLine = fcPts.map((p, i) => {
    const idx = points.indexOf(p);
    return `${i === 0 ? `M ${padL + fcStart * step} ${yFor(lastHist?.historical ?? 0)}` : 'L'} ${padL + idx * step} ${yFor(p.forecast!)}`;
  }).join(' ');

  const bandPath = fcPts.map((p, i) => {
    const idx = points.indexOf(p);
    const x = padL + idx * step;
    return i === 0 ? `M ${x} ${yFor(p.upper!)}` : `L ${x} ${yFor(p.upper!)}`;
  }).join(' ');
  const bandBottom = fcPts.slice().reverse().map((p) => {
    const idx = points.indexOf(p);
    return `L ${padL + idx * step} ${yFor(p.lower!)}`;
  }).join(' ');

  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="w-full" style={{ height: h }}>
      <defs>
        <linearGradient id="fc-band" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.16" />
          <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.04" />
        </linearGradient>
      </defs>
      {/* grid */}
      {[0, 0.25, 0.5, 0.75, 1].map((g) => {
        const y = padT + innerH * (1 - g);
        return (
          <g key={g}>
            <line x1={padL} y1={y} x2={w - padR} y2={y} stroke="#eef2f7" />
            <text x={padL - 8} y={y + 3} textAnchor="end" className="fill-slate-400" style={{ fontSize: 10 }}>{Math.round(max * g)}</text>
          </g>
        );
      })}
      {/* confidence band */}
      <path d={`${bandPath} ${bandBottom} Z`} fill="url(#fc-band)" />
      {/* historical */}
      <path d={histLine} fill="none" stroke="#2563eb" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" />
      {/* forecast */}
      <path d={fcLine} fill="none" stroke="#06b6d4" strokeWidth="2.6" strokeDasharray="6 4" strokeLinecap="round" strokeLinejoin="round" />
      {/* connection dot */}
      {lastHist && firstFc && (
        <circle cx={padL + fcStart * step} cy={yFor(lastHist.historical!)} r="4" fill="white" stroke="#2563eb" strokeWidth="2.5" />
      )}
      {/* labels */}
      {points.map((p, i) => (
        (i % 2 === 0 || i === points.length - 1) && (
          <text key={i} x={padL + i * step} y={h - 8} textAnchor="middle" className="fill-slate-400" style={{ fontSize: 10 }}>{p.label}</text>
        )
      ))}
    </svg>
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
