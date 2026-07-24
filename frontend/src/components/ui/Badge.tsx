import type { ReactNode } from 'react';
import { cn } from '../../lib/utils';

type Variant = 'brand' | 'emerald' | 'amber' | 'rose' | 'slate' | 'accent';
type Tone = 'solid' | 'soft' | 'outline';

const styles: Record<Variant, Record<Tone, string>> = {
  brand: {
    solid: 'bg-brand-600 text-white hover:bg-brand-700',
    soft: 'bg-brand-50 text-brand-700',
    outline: 'border border-brand-200 text-brand-700 bg-white',
  },
  emerald: {
    solid: 'bg-emerald-600 text-white hover:bg-emerald-700',
    soft: 'bg-emerald-50 text-emerald-700',
    outline: 'border border-emerald-200 text-emerald-700 bg-white',
  },
  amber: {
    solid: 'bg-amber-500 text-white hover:bg-amber-600',
    soft: 'bg-amber-50 text-amber-700',
    outline: 'border border-amber-200 text-amber-700 bg-white',
  },
  rose: {
    solid: 'bg-rose-600 text-white hover:bg-rose-700',
    soft: 'bg-rose-50 text-rose-700',
    outline: 'border border-rose-200 text-rose-700 bg-white',
  },
  slate: {
    solid: 'bg-slate-800 text-white hover:bg-slate-900',
    soft: 'bg-slate-100 text-slate-700',
    outline: 'border border-slate-200 text-slate-700 bg-white',
  },
  accent: {
    solid: 'bg-accent-600 text-white hover:bg-accent-700',
    soft: 'bg-accent-50 text-accent-700',
    outline: 'border border-accent-200 text-accent-700 bg-white',
  },
};

export function Badge({
  children,
  variant = 'slate',
  tone = 'soft',
  className,
  dot = false,
}: {
  children: ReactNode;
  variant?: Variant;
  tone?: Tone;
  className?: string;
  dot?: boolean;
}) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium',
        styles[variant][tone],
        className
      )}
    >
      {dot && (
        <span
          className={cn(
            'h-1.5 w-1.5 rounded-full',
            tone === 'soft' ? 'bg-current' : 'bg-white/80'
          )}
        />
      )}
      {children}
    </span>
  );
}

const dotColor: Record<Variant, string> = {
  brand: 'bg-brand-500',
  emerald: 'bg-emerald-500',
  amber: 'bg-amber-500',
  rose: 'bg-rose-500',
  slate: 'bg-slate-400',
  accent: 'bg-accent-500',
};

export function StatusDot({ variant = 'slate', pulse = false }: { variant?: Variant; pulse?: boolean }) {
  return (
    <span className="relative flex h-2 w-2">
      {pulse && (
        <span
          className={cn(
            'absolute inline-flex h-full w-full animate-ping rounded-full opacity-60',
            dotColor[variant]
          )}
        />
      )}
      <span className={cn('relative inline-flex h-2 w-2 rounded-full', dotColor[variant])} />
    </span>
  );
}
