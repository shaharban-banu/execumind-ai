import { useEffect, useRef, useState } from 'react';
import { cn } from '../lib/utils';
import { sendChatMessage, getChatHistory } from '../lib/api';
import type { ChatMessage } from '../lib/types';
import { formatRelativeTime } from '../lib/utils';
import { Spinner } from './ui/Feedback';
import ReactMarkdown from "react-markdown";

const SUGGESTIONS = [
  "Why are sales declining?",
  "Summarize customer satisfaction.",
  "Forecast revenue for the next 3 months.",
  "Which products are underperforming?",
  "Are deliveries getting delayed?",
  "What should I focus on this month?"
];

export function AssistantPanel({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [thinking, setThinking] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (open && messages.length === 0) {
      getChatHistory().then(setMessages);
    }
  }, [open, messages.length]);

  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 200);
    }
  }, [open]);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages, thinking]);

  async function handleSend(text: string) {
    const trimmed = text.trim();
    if (!trimmed || loading) return;
    const userMsg: ChatMessage = {
      id: `u-${Date.now()}`,
      role: 'user',
      content: trimmed,
      timestamp: new Date().toISOString(),
    };
    setMessages((m) => [...m, userMsg]);
    setInput('');
    setLoading(true);
    setThinking(true);
    try {
      const reply = await sendChatMessage(trimmed);
      setMessages((m) => [...m, reply]);
    } catch {
      setMessages((m) => [
        ...m,
        {
          id: `err-${Date.now()}`,
          role: "assistant",
          content:
            "⚠ Executive Advisor is temporarily unavailable.\n\nThe AI service has reached its usage limit. Please try again later.",
          timestamp: new Date().toISOString(),
        },
      ]);
    } finally {
      setLoading(false);
      setThinking(false);
    }
  }

  return (
    <>
      <div
        className={cn(
          'fixed inset-0 z-50 bg-slate-900/30 backdrop-blur-sm transition-opacity duration-300',
          open ? 'opacity-100' : 'pointer-events-none opacity-0'
        )}
        onClick={onClose}
      />
      <div
        className={cn(
          'fixed inset-y-0 right-0 z-50 flex w-full max-w-[440px] flex-col bg-white shadow-2xl transition-transform duration-300 ease-out',
          open ? 'translate-x-0' : 'translate-x-full'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
          <div className="flex items-center gap-3">
            <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 shadow-lg shadow-brand-600/30">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 3v4M3 5h4M6 17v4M4 19h4M13 3l3.5 9L13 21M11 3l-3.5 9L11 21" />
              </svg>
              <span className="absolute -right-0.5 -top-0.5 h-2.5 w-2.5 rounded-full border-2 border-white bg-emerald-400" />
            </div>
            <div>
              <h3 className="font-display text-[15px] font-semibold text-slate-900">Executive Advisor</h3>
              <p className="text-xs text-slate-400">AI synthesizer · online</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-slate-800"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <path d="M18 6L6 18M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Messages */}
        <div ref={scrollRef} className="flex-1 space-y-4 overflow-y-auto px-5 py-5">
          {messages.length === 0 && (
            <div className="flex items-center justify-center py-8">
              <Spinner />
            </div>
          )}
          {messages.map((m) => (
            <MessageBubble key={m.id} message={m} />
          ))}
          {thinking && <ThinkingIndicator />}
        </div>

        {/* Suggestions */}
        {messages.length <= 1 && (
          <div className="border-t border-slate-100 px-5 py-3">
            <p className="mb-2 text-[11px] font-semibold uppercase tracking-wider text-slate-400">Try asking</p>
            <div className="flex flex-wrap gap-2">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => handleSend(s)}
                  disabled={loading}
                  className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-medium text-slate-600 transition hover:border-brand-300 hover:bg-brand-50 hover:text-brand-700 disabled:opacity-50"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="border-t border-slate-200 p-4">
          <div className="relative rounded-2xl border border-slate-200 bg-slate-50 focus-within:border-brand-400 focus-within:bg-white focus-within:ring-4 focus-within:ring-brand-500/10">
            <textarea
              ref={inputRef}
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend(input);
                }
              }}
              placeholder="Ask about risks, forecasts, decisions…"
              className="block max-h-32 w-full resize-none bg-transparent px-4 py-3 pr-12 text-sm text-slate-700 placeholder:text-slate-400 focus:outline-none"
            />
            <button
              onClick={() => handleSend(input)}
              disabled={!input.trim() || loading}
              className="absolute bottom-2.5 right-2.5 flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600 text-white transition hover:bg-brand-700 disabled:opacity-40"
            >
              {loading ? (
                <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white border-r-transparent" />
              ) : (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
                </svg>
              )}
            </button>
          </div>
          <p className="mt-2 text-center text-[10px] text-slate-400">
            AI-generated insights · verify before acting on critical decisions
          </p>
        </div>
      </div>
    </>
  );
}

function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === 'user';
  return (
    <div className={cn('flex animate-fade-in gap-3', isUser && 'flex-row-reverse')}>
      <div
        className={cn(
          'flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-xs font-semibold',
          isUser ? 'bg-slate-200 text-slate-600' : 'bg-gradient-to-br from-brand-500 to-brand-700 text-white'
        )}
      >
        {isUser ? 'AK' : (
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
            <path d="M5 3v4M3 5h4M6 17v4M4 19h4M13 3l3.5 9L13 21M11 3l-3.5 9L11 21" />
          </svg>
        )}
      </div>
      <div className={cn('max-w-[80%]', isUser && 'text-right')}>
        <div
          className={cn(
            "rounded-2xl px-4 py-3",
            isUser
              ? "bg-brand-600 text-white"
              : "bg-slate-100 text-slate-800"
          )}
        >
          <article className="prose prose-sm max-w-none prose-slate">
            <ReactMarkdown
              components={{
                h2: ({ children }) => (
                  <h2 className="mt-5 mb-3 text-base font-semibold text-slate-900 border-b border-slate-200 pb-2">
                    {children}
                  </h2>
                ),

                p: ({ children }) => (
                  <p className="mb-3 leading-7 text-slate-700">
                    {children}
                  </p>
                ),

                ul: ({ children }) => (
                  <ul className="mb-4 list-disc pl-5 space-y-2">
                    {children}
                  </ul>
                ),

                ol: ({ children }) => (
                  <ol className="mb-4 list-decimal pl-5 space-y-2">
                    {children}
                  </ol>
                ),

                li: ({ children }) => (
                  <li className="text-slate-700">
                    {children}
                  </li>
                ),
              }}
            >
              {message.content}
            </ReactMarkdown>
          </article>
        </div>
        <div className={cn('mt-1 flex items-center gap-2', isUser && 'justify-end')}>
          <span className="text-[10px] text-slate-400">{formatRelativeTime(message.timestamp)}</span>
          {message.citations && (
            <span className="text-[10px] text-brand-500">· {message.citations.length} sources</span>
          )}
        </div>
      </div>
    </div>
  );
}

function ThinkingIndicator() {
  return (
    <div className="flex animate-fade-in gap-3">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-brand-500 to-brand-700 text-white">
        🤖
      </div>

      <div className="rounded-2xl rounded-tl-sm bg-slate-100 px-4 py-3">
        <p className="text-sm font-medium text-slate-700">
          Executive Advisor is analyzing...
        </p>

        <div className="mt-2 space-y-1 text-xs text-slate-500">
          <p>✓ Customer Intelligence Agent</p>
          <p>✓ Data Intelligence Agent</p>
          <p>⏳ Forecast Agent</p>
        </div>
      </div>
    </div>
  );
}