import { useState } from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { cn } from '../lib/utils';

export function SettingsPage() {
  const [notifEmail, setNotifEmail] = useState(true);
  const [notifSlack, setNotifSlack] = useState(true);
  const [notifCritical, setNotifCritical] = useState(true);
  const [autoForecast, setAutoForecast] = useState(true);
  const [confidenceThreshold, setConfidenceThreshold] = useState(70);
  const [riskAppetite, setRiskAppetite] = useState<'conservative' | 'balanced' | 'aggressive'>('balanced');
  const [theme, setTheme] = useState<'light' | 'system'>('light');
  const [saved, setSaved] = useState(false);

  function handleSave() {
    setSaved(true);
    setTimeout(() => setSaved(false), 2200);
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      {/* Profile */}
      <Card>
        <CardHeader title="Profile" subtitle="Your executive account" icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="8" r="4" /><path d="M4 21a8 8 0 0 1 16 0" /></svg>} />
        <div className="p-5">
          <div className="flex items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-slate-700 to-slate-900 text-xl font-semibold text-white">AK</div>
            <div className="flex-1">
              <p className="font-display text-base font-semibold text-slate-900">Shaharban</p>
              <p className="text-sm text-slate-500">Chief of Staff · ExecuMind AI</p>
              <div className="mt-1.5 flex items-center gap-2">
                <Badge variant="emerald" tone="soft" dot>Active</Badge>
                <Badge variant="brand" tone="soft">Admin</Badge>
              </div>
            </div>
            <Button variant="secondary" size="sm">Change avatar</Button>
          </div>
          <div className="mt-5 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Full name" value="Alex Kim" />
            <Field label="Email" value="alex.kim@execumind.ai" />
            <Field label="Role" value="Chief of Staff" />
            <Field label="Timezone" value="America/Los_Angeles" />
          </div>
        </div>
      </Card>

      {/* AI preferences */}
      <Card>
        <CardHeader
          title="AI Preferences"
          subtitle="Tune how ExecuMind generates insight"
          icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 3v4M3 5h4M6 17v4M4 19h4M13 3l3.5 9L13 21M11 3l-3.5 9L11 21" /></svg>}
        />
        <div className="space-y-1 p-5">
          <Toggle
            label="Automatic forecasting"
            description="Generate forecasts on new data ingestion"
            checked={autoForecast}
            onChange={setAutoForecast}
          />
          <Toggle
            label="Critical alert notifications"
            description="Immediate alerts for critical-severity intelligence"
            checked={notifCritical}
            onChange={setNotifCritical}
          />
          <div className="py-4">
            <div className="mb-2 flex items-center justify-between">
              <label className="text-sm font-medium text-slate-700">Recommendation confidence threshold</label>
              <span className="rounded-lg bg-brand-50 px-2 py-0.5 text-sm font-semibold text-brand-700">{confidenceThreshold}%</span>
            </div>
            <input
              type="range"
              min={50}
              max={95}
              value={confidenceThreshold}
              onChange={(e) => setConfidenceThreshold(Number(e.target.value))}
              className="h-2 w-full cursor-pointer appearance-none rounded-full bg-slate-200 accent-brand-600"
            />
            <p className="mt-1.5 text-xs text-slate-400">Only surface recommendations with confidence at or above this level.</p>
          </div>
          <div className="py-4">
            <label className="mb-2.5 block text-sm font-medium text-slate-700">Risk appetite</label>
            <div className="grid grid-cols-3 gap-3">
              {(['conservative', 'balanced', 'aggressive'] as const).map((r) => (
                <button
                  key={r}
                  onClick={() => setRiskAppetite(r)}
                  className={cn(
                    'rounded-xl border p-3 text-center transition',
                    riskAppetite === r
                      ? 'border-brand-300 bg-brand-50/60 ring-2 ring-brand-500/10'
                      : 'border-slate-200 bg-white hover:border-slate-300'
                  )}
                >
                  <p className="text-sm font-semibold capitalize text-slate-900">{r}</p>
                </button>
              ))}
            </div>
          </div>
        </div>
      </Card>

      {/* Notifications */}
      <Card>
        <CardHeader
          title="Notifications"
          subtitle="Where ExecuMind sends alerts"
          icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" /><path d="M13.73 21a2 2 0 0 1-3.46 0" /></svg>}
        />
        <div className="space-y-1 p-5">
          <Toggle label="Email digest" description="Daily 8 AM summary of overnight signals" checked={notifEmail} onChange={setNotifEmail} />
          <Toggle label="Slack integration" description="#exec-intelligence channel" checked={notifSlack} onChange={setNotifSlack} />
        </div>
      </Card>

      {/* Appearance */}
      <Card>
        <CardHeader
          title="Appearance"
          subtitle="Display preferences"
          icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" /></svg>}
        />
        <div className="p-5">
          <label className="mb-2.5 block text-sm font-medium text-slate-700">Theme</label>
          <div className="grid grid-cols-2 gap-3">
            {(['light', 'system'] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTheme(t)}
                className={cn(
                  'flex items-center gap-3 rounded-xl border p-3 transition',
                  theme === t ? 'border-brand-300 bg-brand-50/60 ring-2 ring-brand-500/10' : 'border-slate-200 bg-white hover:border-slate-300'
                )}
              >
                <span className={cn('flex h-8 w-8 items-center justify-center rounded-lg', theme === t ? 'bg-brand-600 text-white' : 'bg-slate-100 text-slate-400')}>
                  {t === 'light' ? (
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2" /></svg>
                  ) : (
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="3" width="18" height="18" rx="3" /><path d="M3 9h18" /></svg>
                  )}
                </span>
                <span className="text-sm font-semibold capitalize text-slate-900">{t}</span>
              </button>
            ))}
          </div>
        </div>
      </Card>

      {/* Save bar */}
      <div className="sticky bottom-4 z-10 flex items-center justify-between rounded-2xl border border-slate-200 bg-white/90 px-5 py-3.5 shadow-card backdrop-blur-md">
        <p className="text-sm text-slate-500">
          {saved ? <span className="font-medium text-emerald-600">Preferences saved successfully.</span> : 'Changes apply to your workspace.'}
        </p>
        <div className="flex gap-2">
          <Button variant="secondary" size="sm">Cancel</Button>
          <Button size="sm" onClick={handleSave} icon={<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" /><path d="M17 21v-8H7v8M7 3v5h8" /></svg>}>
            Save changes
          </Button>
        </div>
      </div>
    </div>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <label className="mb-1.5 block text-xs font-medium uppercase tracking-wider text-slate-400">{label}</label>
      <input defaultValue={value} className="input-base" />
    </div>
  );
}

function Toggle({
  label,
  description,
  checked,
  onChange,
}: {
  label: string;
  description: string;
  checked: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <div className="flex items-center justify-between border-t border-slate-100 py-3.5 first:border-t-0 first:pt-0">
      <div>
        <p className="text-sm font-medium text-slate-800">{label}</p>
        <p className="text-xs text-slate-500">{description}</p>
      </div>
      <button
        onClick={() => onChange(!checked)}
        className={cn(
          'relative h-6 w-11 shrink-0 rounded-full transition-colors duration-200',
          checked ? 'bg-brand-600' : 'bg-slate-200'
        )}
      >
        <span
          className={cn(
            'absolute top-0.5 h-5 w-5 rounded-full bg-white shadow-sm transition-transform duration-200',
            checked ? 'translate-x-[22px]' : 'translate-x-0.5'
          )}
        />
      </button>
    </div>
  );
}
