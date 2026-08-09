import { useState } from 'react';
import { reprocessPlatform } from '../lib/api';

export function PlatformManagement() {
  const [showReprocessModal, setShowReprocessModal] = useState(false);
  const [isReprocessing, setIsReprocessing] = useState(false);
  const [reprocessError, setReprocessError] = useState<string | null>(null);
  const [reprocessSuccess, setReprocessSuccess] = useState(false);

  const API_URL = import.meta.env.VITE_API_URL;

  const handleReprocess = async () => {
    setIsReprocessing(true);
    setReprocessError(null);
    setReprocessSuccess(false);

    try {
      const result = await reprocessPlatform();

      if (!result.success) {
        throw new Error(
          typeof result.error === 'string'
            ? result.error
            : result.error?.error || 'Platform reprocess failed.'
        );
      }

      setShowReprocessModal(false);
      setReprocessSuccess(true);

    } catch (error) {
      console.error('Platform reprocess failed:', error);

      setReprocessError(
        error instanceof Error
          ? error.message
          : 'Platform reprocess failed.'
      );

    } finally {
      setIsReprocessing(false);
    }
  };

  return (
    <div className="space-y-6">

      {/* Page intro */}
      <div>
        <h2 className="text-lg font-semibold text-slate-900">
          Platform Management
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          Manage platform data, processing, and reset operations.
        </p>
      </div>

      {/* Reprocess Platform */}
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-start gap-4">

          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
            <svg
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M21 12a9 9 0 0 1-15.5 6.3L3 16" />
              <path d="M3 21v-5h5" />
              <path d="M3 12a9 9 0 0 1 15.5-6.3L21 8" />
              <path d="M21 3v5h-5" />
            </svg>
          </div>

          <div className="flex-1">
            <h3 className="text-base font-semibold text-slate-900">
              Reprocess Platform
            </h3>

            <p className="mt-1 text-sm text-slate-500">
              Rebuild the analytics platform using your existing
              datasets and knowledge documents.
            </p>

            <div className="mt-5">
              <p className="mb-3 text-sm font-medium text-slate-700">
                The following will be cleared:
              </p>

              <div className="grid gap-2 sm:grid-cols-2">
                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <span className="text-emerald-600">✓</span>
                  PostgreSQL data
                </div>

                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <span className="text-emerald-600">✓</span>
                  FAISS vector index
                </div>

                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <span className="text-emerald-600">✓</span>
                  Forecast models
                </div>

                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <span className="text-emerald-600">✓</span>
                  Forecast reports
                </div>
              </div>
            </div>

            <div className="mt-5 rounded-xl bg-blue-50 px-4 py-3">
              <p className="text-sm text-blue-700">
                Your uploaded datasets and knowledge documents will
                be kept.
              </p>
            </div>

            <div className="mt-6 flex justify-end">
              <button
                type="button"
                onClick={() => {
                  setReprocessError(null);
                  setReprocessSuccess(false);
                  setShowReprocessModal(true);
                }}
                className="rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700"
              >
                Reprocess Platform
              </button>
            </div>
          </div>
        </div>
      </section>

      {reprocessError && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3">
          <p className="text-sm font-semibold text-red-700">
            Reprocess failed
          </p>

          <p className="mt-1 text-sm text-red-600">
            {reprocessError}
          </p>
        </div>
      )}

      {reprocessSuccess && (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3">
          <p className="text-sm font-semibold text-emerald-700">
            Platform reprocessed successfully
          </p>

          <p className="mt-1 text-sm text-emerald-600">
            The datasets were preserved and the analytics platform has
            been rebuilt successfully.
          </p>
        </div>
      )}

      {/* Factory Reset */}
      <section className="rounded-2xl border border-red-200 bg-white p-6 shadow-sm">
        <div className="flex items-start gap-4">

          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-red-50 text-red-600">
            <svg
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M12 3v10" />
              <path d="M8 7a8 8 0 1 0 8 0" />
              <path d="M12 21h.01" />
            </svg>
          </div>

          <div className="flex-1">
            <div className="flex items-center gap-3">
              <h3 className="text-base font-semibold text-red-700">
                Factory Reset
              </h3>

              <span className="rounded-md bg-red-50 px-2 py-1 text-[10px] font-semibold uppercase tracking-wide text-red-600">
                Danger Zone
              </span>
            </div>

            <p className="mt-1 text-sm text-slate-500">
              Completely reset the ExecuMind AI platform and remove
              all stored data.
            </p>

            <div className="mt-5">
              <p className="mb-3 text-sm font-medium text-slate-700">
                This will permanently delete:
              </p>

              <div className="grid gap-2 sm:grid-cols-2">
                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <span className="text-red-500">⚠</span>
                  All datasets
                </div>

                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <span className="text-red-500">⚠</span>
                  All knowledge documents
                </div>

                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <span className="text-red-500">⚠</span>
                  PostgreSQL data
                </div>

                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <span className="text-red-500">⚠</span>
                  FAISS vector index
                </div>

                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <span className="text-red-500">⚠</span>
                  Forecast models
                </div>

                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <span className="text-red-500">⚠</span>
                  Forecast reports
                </div>
              </div>
            </div>

            <div className="mt-5 rounded-xl border border-red-100 bg-red-50 px-4 py-3">
              <p className="text-sm font-medium text-red-700">
                This action cannot be undone.
              </p>
              <p className="mt-1 text-xs text-red-600">
                Make sure you have backed up any data you need before
                continuing.
              </p>
            </div>

            <div className="mt-6 flex justify-end">
              <button
                type="button"
                className="rounded-xl bg-red-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-red-700"
              >
                Factory Reset
              </button>
            </div>
          </div>
        </div>

      </section>
      {/* Reprocess Confirmation Modal */}
      {showReprocessModal && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 px-4"
          onClick={() => {
            if (!isReprocessing) {
              setShowReprocessModal(false);
            }
          }}
        >
          <div
            className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-start gap-4">
              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-blue-50 text-blue-600">
                <svg
                  width="22"
                  height="22"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M21 12a9 9 0 0 1-15.5 6.3L3 16" />
                  <path d="M3 21v-5h5" />
                  <path d="M3 12a9 9 0 0 1 15.5-6.3L21 8" />
                  <path d="M21 3v5h-5" />
                </svg>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-slate-900">
                  Reprocess Platform?
                </h3>

                <p className="mt-1 text-sm text-slate-500">
                  The current processed data and generated intelligence
                  will be cleared and rebuilt.
                </p>
              </div>
            </div>

            {/* What will be cleared */}
            <div className="mt-5 rounded-xl bg-slate-50 p-4">
              <p className="text-sm font-semibold text-slate-700">
                The following will be cleared:
              </p>

              <ul className="mt-3 space-y-2 text-sm text-slate-600">
                <li className="flex items-center gap-2">
                  <span className="text-blue-600">✓</span>
                  PostgreSQL processed data
                </li>

                <li className="flex items-center gap-2">
                  <span className="text-blue-600">✓</span>
                  FAISS vector index
                </li>

                <li className="flex items-center gap-2">
                  <span className="text-blue-600">✓</span>
                  Forecast models
                </li>

                <li className="flex items-center gap-2">
                  <span className="text-blue-600">✓</span>
                  Forecast reports
                </li>
              </ul>
            </div>

            {/* What will be kept */}
            <div className="mt-4 rounded-xl bg-emerald-50 p-4">
              <p className="text-sm font-semibold text-emerald-700">
                The following will be kept:
              </p>

              <ul className="mt-3 space-y-2 text-sm text-emerald-700">
                <li className="flex items-center gap-2">
                  <span>✓</span>
                  Uploaded datasets
                </li>

                <li className="flex items-center gap-2">
                  <span>✓</span>
                  Knowledge documents
                </li>
              </ul>
            </div>

            {/* Processing information */}
            <p className="mt-4 text-xs leading-5 text-slate-500">
              After clearing the processed data, ExecuMind AI will run
              the ingestion pipeline, forecast training, and knowledge
              indexing again. This may take several minutes.
            </p>
            {isReprocessing && (
              <div className="mt-4 rounded-xl bg-blue-50 px-4 py-3">
                <div className="flex items-center gap-3">
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-blue-200 border-t-blue-600" />
                  <p className="text-sm font-medium text-blue-700">
                    Reprocessing platform...
                  </p>
                </div>

                <p className="mt-1 pl-7 text-xs text-blue-600">
                  Please keep this page open while ETL, forecasting, and RAG
                  indexing are running.
                </p>
              </div>
            )}

            {/* Actions */}
            <div className="mt-6 flex justify-end gap-3">
              <button
                type="button"
                disabled={isReprocessing}
                onClick={() => setShowReprocessModal(false)}
                className="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-600 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
              >
                Cancel
              </button>

              <button
                type="button"
                onClick={handleReprocess}
                disabled={isReprocessing}
                className="rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isReprocessing ? 'Reprocessing...' : 'Reprocess Platform'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}