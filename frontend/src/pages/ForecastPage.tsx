import { useEffect, useState } from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { BarList } from '../components/ui/Charts';
import { Skeleton } from '../components/ui/Feedback';
import { getForecast, runScenario } from '../lib/api';
import type { ForecastResult, ScenarioConfig } from '../lib/types';
import { cn } from '../lib/utils';

const scenarioPresets: { name: string; emoji: string; config: ScenarioConfig; desc: string }[] = [
  { name: 'Base Case', emoji: '', config: { revenueGrowth: 12, costChange: 3, headcountChange: 5, marketVolatility: 20 }, desc: 'Current trajectory' },
  { name: 'Optimistic', emoji: '', config: { revenueGrowth: 22, costChange: 1, headcountChange: 12, marketVolatility: 12 }, desc: 'Favorable market' },
  { name: 'Recession', emoji: '', config: { revenueGrowth: -8, costChange: 8, headcountChange: -6, marketVolatility: 55 }, desc: 'Economic downturn' },
  { name: 'Stress Test', emoji: '', config: { revenueGrowth: -15, costChange: 12, headcountChange: -12, marketVolatility: 80 }, desc: 'Severe downside' },
];

export function ForecastPage() {
  const [forecast, setForecast] = useState<ForecastResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [activePreset, setActivePreset] = useState(0);
  const [config, setConfig] = useState<ScenarioConfig>(scenarioPresets[0].config);

  useEffect(() => {
    getForecast().then((d) => { setForecast(d); setLoading(false); });
  }, []);

  async function handleRun() {
    setRunning(true);
    try {
      const result = await runScenario(config);
      setForecast(result);
    } finally {
      setRunning(false);
    }
  }

  function selectPreset(i: number) {
    setActivePreset(i);
    setConfig(scenarioPresets[i].config);
  }

  const maxForecast = forecast ? Math.max(...forecast.points.map((p) => Math.max(p.historical ?? 0, p.forecast ?? 0))) : 100;
  const scenarioPoints = forecast
  ? forecast.points.map((point) => {
      if (point.forecast === null) return point;

      const multiplier = 1 + config.revenueGrowth / 100;

      return {
        ...point,
        forecast: point.forecast * multiplier,
        lower: point.lower ? point.lower * multiplier : null,
        upper: point.upper ? point.upper * multiplier : null,
      };
    })
  : [];
  const baseRevenue = forecast
  ? forecast.points
      .filter((p) => p.forecast !== null)
      .reduce((sum, p) => sum + (p.forecast ?? 0), 0)
  : 0;

  const scenarioRevenue = scenarioPoints
    .filter((p) => p.forecast !== null)
    .reduce((sum, p) => sum + (p.forecast ?? 0), 0);

  const revenueChange =
    baseRevenue === 0
      ? 0
      : ((scenarioRevenue - baseRevenue) / baseRevenue) * 100;
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
                points={scenarioPoints}
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
          title="Scenario Impact"
          subtitle="Estimated outcome based on current assumptions"
        />

        <div className="px-5 pb-5">
          <p className="text-3xl font-bold text-slate-900">
            ₹{(scenarioRevenue / 1_000_000).toFixed(2)}M
          </p>

          <p
            className={`mt-2 text-sm font-medium ${
              revenueChange >= 0
                ? "text-emerald-600"
                : "text-red-600"
            }`}
          >
            {revenueChange >= 0 ? "▲" : "▼"}{" "}
            {Math.abs(revenueChange).toFixed(1)}% vs Base Forecast
          </p>
        </div>
      </Card>
      {/* Scenario planner */}
      <Card>
        <CardHeader
          title="Scenario Planner"
          subtitle="Scenario adjustments update projected values after simulation."
          icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v4M12 18v4M4.9 4.9l2.8 2.8M16.3 16.3l2.8 2.8M2 12h4M18 12h4M4.9 19.1l2.8-2.8M16.3 7.7l2.8-2.8" /></svg>}
        />
        <div className="p-5">
          {/* Presets */}
          <div className="mb-5 grid grid-cols-2 gap-3 md:grid-cols-4">
            {scenarioPresets.map((p, i) => (
              <button
                key={p.name}
                onClick={() => selectPreset(i)}
                className={cn(
                  'rounded-xl border p-3 text-left transition',
                  activePreset === i
                    ? 'border-brand-300 bg-brand-50/60 ring-2 ring-brand-500/10'
                    : 'border-slate-200 bg-white hover:border-slate-300'
                )}
              >
                <p className="text-sm font-semibold text-slate-900">{p.name}</p>
                <p className="mt-0.5 text-xs text-slate-500">{p.desc}</p>
              </button>
            ))}
          </div>

          {/* Sliders */}
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
            <Slider
              label="Revenue Growth"
              value={config.revenueGrowth}
              min={-20}
              max={30}
              suffix="%"
              onChange={(v) => setConfig((c) => ({ ...c, revenueGrowth: v }))}
            />
            <Slider
              label="Cost Change"
              value={config.costChange}
              min={-5}
              max={20}
              suffix="%"
              onChange={(v) => setConfig((c) => ({ ...c, costChange: v }))}
            />
            <Slider
              label="Headcount Change"
              value={config.headcountChange}
              min={-15}
              max={20}
              suffix="%"
              onChange={(v) => setConfig((c) => ({ ...c, headcountChange: v }))}
            />
            <Slider
              label="Market Volatility"
              value={config.marketVolatility}
              min={0}
              max={100}
              suffix="%"
              onChange={(v) => setConfig((c) => ({ ...c, marketVolatility: v }))}
            />
          </div>

          <div className="mt-5 flex items-center gap-3">
            <Button onClick={handleRun} loading={running} icon={<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 3l14 9-14 9V3z" /></svg>}>
              Run Scenario
            </Button>
            <Button variant="secondary" onClick={() => selectPreset(0)}>Reset to Base</Button>
            {running && <span className="text-sm text-slate-500">Simulating model…</span>}
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

function Slider({
  label,
  value,
  min,
  max,
  suffix,
  onChange,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  suffix: string;
  onChange: (v: number) => void;
}) {
  return (
    <div>
      <div className="mb-2 flex items-center justify-between">
        <label className="text-sm font-medium text-slate-700">{label}</label>
        <span className={cn(
          'rounded-lg px-2 py-0.5 text-sm font-semibold',
          value > 0 ? 'bg-emerald-50 text-emerald-700' : value < 0 ? 'bg-rose-50 text-rose-700' : 'bg-slate-100 text-slate-600'
        )}>
          {value > 0 ? '+' : ''}{value}{suffix}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="h-2 w-full cursor-pointer appearance-none rounded-full bg-slate-200 accent-brand-600"
      />
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
