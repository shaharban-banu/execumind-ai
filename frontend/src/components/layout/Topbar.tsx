import { useEffect, useState } from 'react';
import { cn } from '../../lib/utils';
import { StatusDot } from '../ui/Badge';
import type { PageId } from './Sidebar';

const pageMeta: Record<PageId, { title: string; subtitle: string }> = {
  dashboard: { title: 'Dashboard', subtitle: 'Real-time executive intelligence overview' },
  upload: { title: 'Upload Dataset', subtitle: 'Ingest data for AI-driven analysis' },
  advisor: { title: 'Executive Advisor', subtitle: 'AI-powered strategic recommendations' },
  forecast: { title: 'Forecast Center', subtitle: 'Predictive modeling and scenario planning' },
  settings: { title: 'Settings', subtitle: 'Platform configuration and preferences' },
};

export function Topbar({
  page,
  onOpenMobileNav,
  onOpenAssistant,
}: {
  page: PageId;
  onOpenMobileNav: () => void;
  onOpenAssistant: () => void;
}) {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 30_000);
    return () => clearInterval(t);
  }, []);

  const meta = pageMeta[page];

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center gap-4 border-b border-slate-200 bg-white/80 px-4 backdrop-blur-md md:px-6">
      {/* Mobile menu */}
      <button
        onClick={onOpenMobileNav}
        className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-600 hover:bg-slate-100 lg:hidden"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
          <path d="M3 6h18M3 12h18M3 18h18" />
        </svg>
      </button>

      {/* Title */}
      <div className="min-w-0 flex-1">
        <h1 className="font-display text-lg font-bold tracking-tight text-slate-900 md:text-xl">
          {meta.title}
        </h1>
        <p className="hidden truncate text-xs text-slate-500 sm:block">{meta.subtitle}</p>
      </div>

      {/* Search */}
      <div className="relative hidden md:block">
        <svg className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="11" cy="11" r="7" />
          <path d="M21 21l-4.3-4.3" />
        </svg>
        <input
          placeholder="Search intelligence, reports…"
          className="h-9 w-56 rounded-xl border border-slate-200 bg-slate-50 pl-9 pr-3 text-sm text-slate-700 placeholder:text-slate-400 transition focus:border-brand-400 focus:bg-white focus:outline-none focus:ring-4 focus:ring-brand-500/10 lg:w-72"
        />
        <kbd className="absolute right-2.5 top-1/2 hidden -translate-y-1/2 rounded border border-slate-200 bg-white px-1.5 py-0.5 text-[10px] text-slate-400 lg:block">
          ⌘K
        </kbd>
      </div>

      {/* Status pill */}
      <div className="hidden items-center gap-2 rounded-full border border-emerald-100 bg-emerald-50 px-3 py-1.5 sm:flex">
        <StatusDot variant="emerald" pulse />
        <span className="text-xs font-medium text-emerald-700">Live</span>
        <span className="text-xs text-emerald-600/70">· {now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}</span>
      </div>

      {/* Notifications */}
      <button className="relative flex h-9 w-9 items-center justify-center rounded-lg text-slate-600 transition hover:bg-slate-100">
        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
          <path d="M13.73 21a2 2 0 0 1-3.46 0" />
        </svg>
        <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-rose-500 ring-2 ring-white" />
      </button>

      {/* AI Assistant trigger */}
      <button
        onClick={onOpenAssistant}
        className={cn(
          'group flex h-9 items-center gap-2 rounded-xl bg-brand-600 px-3 text-sm font-medium text-white transition hover:bg-brand-700',
          'shadow-sm shadow-brand-600/25'
        )}
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M5 3v4M3 5h4M6 17v4M4 19h4M13 3l3.5 9L13 21M11 3l-3.5 9L11 21" />
        </svg>
        <span className="hidden sm:inline">Ask AI</span>
      </button>
    </header>
  );
}
