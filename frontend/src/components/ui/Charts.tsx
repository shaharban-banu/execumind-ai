import { useId } from 'react';
import { cn } from '../../lib/utils';

// ---- Sparkline (tiny inline trend) ----
export function Sparkline({
  data,
  color = '#2563eb',
  className,
  strokeWidth = 2,
  fill = true,
}: {
  data: number[];
  color?: string;
  className?: string;
  strokeWidth?: number;
  fill?: boolean;
}) {
  const id = useId();
  const w = 100;
  const h = 32;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;
  const step = w / (data.length - 1);
  const pts = data.map((v, i) => [i * step, h - ((v - min) / range) * (h - 4) - 2]);
  const line = pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p[0]} ${p[1]}`).join(' ');
  const area = `${line} L ${w} ${h} L 0 ${h} Z`;

  return (
    <svg viewBox={`0 0 ${w} ${h}`} className={cn('overflow-visible', className)} preserveAspectRatio="none">
      {fill && (
        <>
          <defs>
            <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={color} stopOpacity="0.22" />
              <stop offset="100%" stopColor={color} stopOpacity="0" />
            </linearGradient>
          </defs>
          <path d={area} fill={`url(#${id})`} />
        </>
      )}
      <path d={line} fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" />
      <circle cx={pts[pts.length - 1][0]} cy={pts[pts.length - 1][1]} r="2.5" fill={color} />
    </svg>
  );
}

// ---- Area / Line chart with axis ----
export function AreaChart({
  labels,
  series,
  height = 240,
  color = '#2563eb',
  showGrid = true,
}: {
  labels: string[];
  series: number[];
  height?: number;
  color?: string;
  showGrid?: boolean;
}) {
  const id = useId();
  const padL = 36;
  const padB = 26;
  const padR = 12;
  const padT = 12;
  const w = 640;
  const innerW = w - padL - padR;
  const innerH = height - padT - padB;
  const max = Math.max(...series) * 1.12;
  const min = 0;
  const range = max - min || 1;
  const step = innerW / (series.length - 1);
  const pts = series.map((v, i) => [padL + i * step, padT + innerH - ((v - min) / range) * innerH]);
  const line = pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p[0]} ${p[1]}`).join(' ');
  const area = `${line} L ${padL + innerW} ${padT + innerH} L ${padL} ${padT + innerH} Z`;
  const gridLines = 4;
  const yTicks = Array.from({ length: gridLines + 1 }, (_, i) => min + (range * i) / gridLines);

  return (
    <svg viewBox={`0 0 ${w} ${height}`} className="w-full" style={{ height }}>
      <defs>
        <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.18" />
          <stop offset="100%" stopColor={color} stopOpacity="0" />
        </linearGradient>
      </defs>
      {showGrid &&
        yTicks.map((t, i) => {
          const y = padT + innerH - ((t - min) / range) * innerH;
          return (
            <g key={i}>
              <line x1={padL} y1={y} x2={w - padR} y2={y} stroke="#eef2f7" strokeWidth="1" />
              <text x={padL - 8} y={y + 3} textAnchor="end" className="fill-slate-400" style={{ fontSize: 10 }}>
                {Math.round(t)}
              </text>
            </g>
          );
        })}
      <path d={area} fill={`url(#${id})`} />
      <path d={line} fill="none" stroke={color} strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
      {pts.map((p, i) => (
        <g key={i}>
          {(i === 0 || i === pts.length - 1 || i % 2 === 1) && (
            <circle cx={p[0]} cy={p[1]} r="3" fill="white" stroke={color} strokeWidth="2" />
          )}
          {(i % 2 === 0 || i === labels.length - 1) && (
            <text x={p[0]} y={height - 8} textAnchor="middle" className="fill-slate-400" style={{ fontSize: 10 }}>
              {labels[i]}
            </text>
          )}
        </g>
      ))}
    </svg>
  );
}

// ---- Donut chart ----
export function DonutChart({
  data,
  size = 180,
  thickness = 22,
  colors = ['#2563eb', '#06b6d4', '#10b981', '#f59e0b', '#94a3b8'],
}: {
  data: { label: string; value: number }[];
  size?: number;
  thickness?: number;
  colors?: string[];
}) {
  const total = data.reduce((s, d) => s + d.value, 0) || 1;
  const r = (size - thickness) / 2;
  const c = 2 * Math.PI * r;
  let offset = 0;

  return (
    <div className="flex items-center gap-6">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="shrink-0">
        <g transform={`rotate(-90 ${size / 2} ${size / 2})`}>
          <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#eef2f7" strokeWidth={thickness} />
          {data.map((d, i) => {
            const len = (d.value / total) * c;
            const el = (
              <circle
                key={d.label}
                cx={size / 2}
                cy={size / 2}
                r={r}
                fill="none"
                stroke={colors[i % colors.length]}
                strokeWidth={thickness}
                strokeDasharray={`${len} ${c - len}`}
                strokeDashoffset={-offset}
                strokeLinecap="round"
                className="transition-all duration-500"
              />
            );
            offset += len;
            return el;
          })}
        </g>
        <text x="50%" y="48%" textAnchor="middle" className="fill-slate-900 font-display" style={{ fontSize: 22, fontWeight: 600 }}>
          {total}
        </text>
        <text x="50%" y="62%" textAnchor="middle" className="fill-slate-400" style={{ fontSize: 11 }}>
          total
        </text>
      </svg>
      <div className="space-y-2.5">
        {data.map((d, i) => (
          <div key={d.label} className="flex items-center gap-2.5">
            <span className="h-2.5 w-2.5 rounded-full" style={{ background: colors[i % colors.length] }} />
            <span className="text-sm text-slate-600">{d.label}</span>
            <span className="ml-auto text-sm font-semibold text-slate-900">{d.value}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ---- Horizontal bar list ----
export function BarList({
  data,
  color = '#2563eb',
  max,
}: {
  data: { label: string; value: number; sub?: string }[];
  color?: string;
  max?: number;
}) {
  const m = max ?? Math.max(...data.map((d) => d.value));
  return (
    <div className="space-y-3.5">
      {data.map((d) => (
        <div key={d.label}>
          <div className="mb-1.5 flex items-center justify-between text-sm">
            <span className="text-slate-600">{d.label}</span>
            <span className="font-semibold text-slate-900">
              {d.sub ?? d.value}
            </span>
          </div>
          <div className="h-2 overflow-hidden rounded-full bg-slate-100">
            <div
              className="h-full rounded-full transition-all duration-700 ease-out"
              style={{ width: `${(d.value / m) * 100}%`, background: color }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}

// ---- Risk matrix bubble plot ----
export function RiskMatrix({
  items,
}: {
  items: { name: string; likelihood: number; impact: number; severity: string }[];
}) {
  const size = 280;
  const pad = 28;
  const inner = size - pad * 2;
  const colorFor = (s: string) =>
    s === 'critical' ? '#e11d48' : s === 'high' ? '#f59e0b' : '#10b981';

  return (
    <div className="relative">
      <svg viewBox={`0 0 ${size} ${size}`} width={size} height={size}>
        {/* quadrant tints */}
        <rect x={pad} y={pad} width={inner / 2} height={inner / 2} fill="#fef2f2" />
        <rect x={pad + inner / 2} y={pad} width={inner / 2} height={inner / 2} fill="#fffbeb" />
        <rect x={pad} y={pad + inner / 2} width={inner / 2} height={inner / 2} fill="#f0fdf4" />
        <rect x={pad + inner / 2} y={pad + inner / 2} width={inner / 2} height={inner / 2} fill="#ecfeff" />

        {/* grid */}
        {[0.25, 0.5, 0.75].map((g) => (
          <g key={g}>
            <line x1={pad} y1={pad + inner * g} x2={size - pad} y2={pad + inner * g} stroke="#e2e8f0" strokeWidth="1" strokeDasharray="3 3" />
            <line x1={pad + inner * g} y1={pad} x2={pad + inner * g} y2={size - pad} stroke="#e2e8f0" strokeWidth="1" strokeDasharray="3 3" />
          </g>
        ))}
        <rect x={pad} y={pad} width={inner} height={inner} fill="none" stroke="#cbd5e1" strokeWidth="1" />

        {/* axis labels */}
        <text x={size / 2} y={size - 6} textAnchor="middle" className="fill-slate-400" style={{ fontSize: 10 }}>Likelihood →</text>
        <text x={10} y={size / 2} textAnchor="middle" transform={`rotate(-90 10 ${size / 2})`} className="fill-slate-400" style={{ fontSize: 10 }}>Impact →</text>

        {items.map((it) => {
          const cx = pad + (it.likelihood / 100) * inner;
          const cy = size - pad - (it.impact / 100) * inner;
          const r = 7 + (it.likelihood / 100) * 8;
          return (
            <g key={it.name} className="transition-transform duration-200 hover:scale-105" style={{ transformBox: 'fill-box', transformOrigin: 'center' }}>
              <circle cx={cx} cy={cy} r={r} fill={colorFor(it.severity)} fillOpacity="0.18" stroke={colorFor(it.severity)} strokeWidth="1.5" />
              <text x={cx} y={cy + r + 12} textAnchor="middle" className="fill-slate-600" style={{ fontSize: 9 }}>
                {it.name}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

// ---- Confidence / progress ring ----
export function ConfidenceRing({ value, size = 48, label }: { value: number; size?: number; label?: string }) {
  const r = (size - 8) / 2;
  const c = 2 * Math.PI * r;
  const dash = (value / 100) * c;
  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#eef2f7" strokeWidth="4" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={value >= 85 ? '#10b981' : value >= 70 ? '#2563eb' : '#f59e0b'}
          strokeWidth="4"
          strokeDasharray={`${dash} ${c}`}
          strokeLinecap="round"
          className="transition-all duration-500"
        />
      </svg>
      <span className="absolute text-xs font-semibold text-slate-700">{label ?? `${value}%`}</span>
    </div>
  );
}
