
import {
  Card,
  CardHeader,
} from "../components/ui/Card";
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Skeleton } from '../components/ui/Feedback';
import {
  getDatasets,
  uploadDataset,
  activateDatasetVersion,
  processPlatform,
  uploadKnowledge,
  getKnowledgeDocuments,
  getPlatformStatus,
  
} from "../lib/api";

import { formatRelativeTime, cn } from '../lib/utils';
import { useCallback, useEffect, useRef, useState } from "react";
import {
  FileText,
  FileType,
  FileCode2,
} from "lucide-react";
import { FolderOpen } from "lucide-react";
import { DatasetRecord, DatasetVersion } from "../lib/types";


const statusMap = {
  ready: { variant: 'emerald' as const, label: 'Ready' },
  processing: { variant: 'amber' as const, label: 'Processing' },
  failed: { variant: 'rose' as const, label: 'Failed' },
};

const typeColors: Record<string, string> = {
  CSV: 'bg-brand-50 text-brand-600',
  Excel: 'bg-emerald-50 text-emerald-600',
  JSON: 'bg-amber-50 text-amber-600',
};

export function UploadPage() {
  const [datasets, setDatasets] = useState<DatasetRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const removeSelectedFile = (index: number) => {
    setSelectedFiles((prev) =>
      prev.filter((_, i) => i !== index)
    );
  };
  const [knowledgeFiles, setKnowledgeFiles] = useState<File[]>([]);
  const [knowledgeDocs, setKnowledgeDocs] = useState<any[]>([]);
  const [showPreview, setShowPreview] = useState<DatasetVersion | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const [processResult, setProcessResult] = useState<any>(null);
  const [knowledgeUploading, setKnowledgeUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");
  const [datasetError, setDatasetError] = useState("");
  const [knowledgeError, setKnowledgeError] = useState("");
  const [platformProcessed, setPlatformProcessed] = useState(false);
  const [platformStatus, setPlatformStatus] = useState<
  "needs_processing" | "processing" | "ready"
>("needs_processing");
  
  const hasDataset = datasets.length > 0;
  const hasKnowledge = knowledgeDocs.length > 0;

  const loadDatasets = useCallback(() => {
    setLoading(true);
    getDatasets().then((d) => { setDatasets(d); setLoading(false); });
  }, []);

 const loadKnowledge = useCallback(() => {
      getKnowledgeDocuments().then((docs) => {
          setKnowledgeDocs(docs);
      });
  }, []);

  const loadPlatformStatus = useCallback(async () => {
      try {
          const status = await getPlatformStatus();

          setPlatformStatus(
              status.platform_ready
                  ? "ready"
                  : "needs_processing"
          );
      } catch (error) {
          console.error(error);
      }
  }, []);

  useEffect(() => {
    loadDatasets();
    loadKnowledge();
    loadPlatformStatus();
}, [loadDatasets, loadKnowledge, loadPlatformStatus]);

  function handleFiles(files: FileList | null) {
  if (!files || files.length === 0) return;

  setDatasetError("");
  setSelectedFiles(Array.from(files));
}
  function handleKnowledgeFiles(
    event: React.ChangeEvent<HTMLInputElement>
) {
    if (!event.target.files) return;

    setKnowledgeFiles(Array.from(event.target.files));
}


async function handleDatasetUpload() {
  if (selectedFiles.length === 0) return;

  setUploading(true);
  setUploadProgress(0);
  setDatasetError(""); 

  const interval = setInterval(() => {
    setUploadProgress((p) =>
      Math.min(p + Math.random() * 18, 95)

  
    );
  }, 120);

  try {
    await uploadDataset(selectedFiles);

    setUploadProgress(100);

    clearInterval(interval);

    setPlatformStatus("needs_processing");
    setProcessResult(null);

    await loadDatasets();

    setTimeout(() => {
      setUploading(false);
      setSelectedFiles([]);
      
      setUploadProgress(0);
    }, 600);

  } catch (error: any) {
  clearInterval(interval);
  setUploading(false);
  setUploadProgress(0);

  const detail = error?.response?.data?.detail;
  console.log(detail);

  // if (Array.isArray(detail)) {
  //   setDatasetError(detail[0]?.msg ?? "Upload failed.");
  // } else {
  //   setDatasetError(detail ?? "Upload failed.");
  // }

  console.error(error);
}
}
async function handleKnowledgeUpload() {
    if (knowledgeFiles.length === 0) return;

    try {
        setKnowledgeUploading(true);
        setUploadMessage("");
        setKnowledgeError("");

        await uploadKnowledge(knowledgeFiles);

        setKnowledgeFiles([]);

        setPlatformStatus("needs_processing");
        setProcessResult(null);

        await loadKnowledge();

        setUploadMessage("Documents uploaded successfully.");

    } catch (error) {
        console.error(error);
        setKnowledgeError("Upload failed. Please try again.");
    } finally {
        setKnowledgeUploading(false);
    }
}

async function handleActivateVersion(
  datasetId: number,
  versionId: number,
) {
  try {
    await activateDatasetVersion(datasetId, versionId);

    await loadDatasets();

    await loadPlatformStatus(); 
    setProcessResult(null);

  } catch (error) {
    console.error(error);
  }
}

async function handleProcessPlatform() {
    try {
        setPlatformStatus("processing");
        const result = await processPlatform();

        setProcessResult(result);

        await loadDatasets();
        await loadKnowledge();
        await loadPlatformStatus();

    }  catch (error) {
        setPlatformStatus("needs_processing");
        console.error(error);
    }
}

function getFileIcon(fileName: string) {
    const extension = fileName.split(".").pop()?.toLowerCase();

    switch (extension) {
        case "pdf":
            return <FileText className="h-5 w-5 text-red-500" />;

        case "doc":
        case "docx":
            return <FileType className="h-5 w-5 text-blue-500" />;

        case "txt":
            return <FileCode2 className="h-5 w-5 text-gray-500" />;

        default:
            return <FileText className="h-5 w-5 text-slate-500" />;
    }
}

  return (
    <div className="space-y-6">
      {/* Drop zone */}
      <Card className="overflow-hidden">
        <CardHeader
          title="Upload Dataset Version"
          subtitle="Every upload creates a new version while preserving previous versions."
        />

        <div className="px-6 pb-6">

          
          {datasetError && (
            <div className="mb-4 rounded-xl border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">
              {datasetError}
            </div>
          )}
          {/* <div className="p-6"> */}
            <div
              onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
              onDragLeave={() => setDragging(false)}
              onDrop={(e) => {
                e.preventDefault();
                setDragging(false);
                handleFiles(e.dataTransfer.files);
              }}
              onClick={() => inputRef.current?.click()}
              className={cn(
                'flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed px-6 py-12 text-center transition-all duration-200',
                dragging ? 'border-brand-400 bg-brand-50/60 scale-[1.01]' : 'border-slate-200 bg-slate-50/40 hover:border-brand-300 hover:bg-brand-50/30'
              )}
            >
            <input
              ref={inputRef}
              type="file"
              multiple
              accept=".csv,.xlsx,.xls,.json,.parquet"
              className="hidden"
              onChange={(e) => handleFiles(e.target.files)}
            />
            <div className={cn(
              'mb-4 flex h-14 w-14 items-center justify-center rounded-2xl transition-colors',
              dragging ? 'bg-brand-100 text-brand-600' : 'bg-white text-slate-400 shadow-sm'
            )}>
              <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <path d="M7 9l5-5 5 5" />
                <path d="M12 4v12" />
              </svg>
            </div>
            <h3 className="font-display text-base font-semibold text-slate-900">
              {dragging ? 'Drop to upload' : 'Drag & drop your dataset'}
            </h3>
            <p className="mt-1 text-sm text-slate-500">
              or <span className="font-medium text-brand-600">browse files</span> · CSV, Excel, JSON, Parquet up to 50MB
            </p>
            <div className="mt-5 flex flex-wrap items-center justify-center gap-2">
              {['CSV', 'XLSX', 'JSON', 'Parquet'].map((f) => (
                <span key={f} className="rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-xs font-medium text-slate-500">{f}</span>
              ))}
            </div>
          </div>

          {/* Selected file + upload progress */}
          {selectedFiles.length > 0 && (
            <div className="mt-4 rounded-xl border border-slate-200 bg-white p-4">
              <div className="flex items-center justify-between gap-3">
                <div className="flex min-w-0 items-center gap-3">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-brand-50 text-brand-600">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><path d="M14 2v6h6" /></svg>
                  </div>
                  <div className="min-w-0">
                    {selectedFiles.map((file, index) => (
                      <div
                        key={`${file.name}-${index}`}
                        className="mb-2 flex items-center justify-between gap-3"
                      >
                        <div className="min-w-0">
                          <p className="truncate text-sm font-medium text-slate-900">
                            {file.name}
                          </p>

                          <p className="text-xs text-slate-400">
                            {(file.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                        </div>

                        {!uploading && uploadProgress < 100 && (
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();

                              setSelectedFiles((prev) =>
                                prev.filter((_, i) => i !== index)
                              );
                            }}
                            className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-slate-400 transition hover:bg-red-50 hover:text-red-600"
                            title="Remove dataset"
                            aria-label={`Remove ${file.name}`}
                          >
                            <svg
                              width="17"
                              height="17"
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth="2"
                              strokeLinecap="round"
                              strokeLinejoin="round"
                            >
                              <path d="M3 6h18" />
                              <path d="M8 6V4h8v2" />
                              <path d="M19 6l-1 14H6L5 6" />
                              <path d="M10 11v5" />
                              <path d="M14 11v5" />
                            </svg>
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
                {!uploading && uploadProgress < 100 && (
                  <Button size="sm" onClick={handleDatasetUpload}>
                      Upload Dataset
                  </Button>
                )}
                {uploadProgress === 100 && <Badge variant="emerald" tone="solid" dot>Uploaded</Badge>}
              </div>
              {uploading && (
                <div className="mt-3">
                  <div className="mb-1.5 flex justify-between text-xs">
                    <span className="text-slate-500">Analyzing dataset structure…</span>
                    <span className="font-medium text-brand-600">{Math.round(uploadProgress)}%</span>
                  </div>
                  <div className="h-2 overflow-hidden rounded-full bg-slate-100">
                    <div className="h-full rounded-full bg-gradient-to-r from-brand-500 to-brand-600 transition-all duration-200" style={{ width: `${uploadProgress}%` }} />
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </Card>
    <Card>
    <CardHeader
        title="Knowledge Documents"
        subtitle="Upload PDFs, DOCX or TXT files to enhance AI responses."
    />

    <div className="space-y-5 p-5">

        {/* Upload Area */}
        <div className="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center transition hover:border-blue-400 hover:bg-slate-50">

            <FolderOpen className="h-10 w-10 text-brand-500" />

            <h3 className="font-semibold text-slate-800">
                Drag & drop your documents
            </h3>

            <p className="text-sm text-slate-500 mt-2">
                or
                <label className="ml-1 cursor-pointer text-blue-600">
                    browse files
                    <input
                        hidden
                        multiple
                        type="file"
                        accept=".pdf,.docx,.txt"
                        onChange={handleKnowledgeFiles}
                    />
                </label>
            </p>

            <p className="mt-3 text-xs text-slate-400">
                PDF, DOCX and TXT supported
            </p>
        </div>

        {/* Selected Files */}
        {knowledgeFiles.length > 0 && (
            <div className="rounded-lg border bg-slate-50 p-4">

                <p className="mb-3 font-medium">
                    Selected Files
                </p>

                <div className="space-y-2">

                    {knowledgeFiles.map((file, index) => (
                      <div
                          key={`${file.name}-${index}`}
                          className="flex items-center justify-between gap-3 rounded-lg bg-white px-3 py-2 text-sm text-slate-700"
                      >
                          <div className="flex min-w-0 items-center gap-2">
                              {getFileIcon(file.name)}

                              <span className="truncate">
                                  {file.name}
                              </span>
                          </div>

                          <button
                              type="button"
                              onClick={() => {
                                  setKnowledgeFiles((prev) =>
                                      prev.filter((_, i) => i !== index)
                                  );
                              }}
                              className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-slate-400 transition hover:bg-red-50 hover:text-red-600"
                              title="Remove document"
                              aria-label={`Remove ${file.name}`}
                          >
                              <svg
                                  width="17"
                                  height="17"
                                  viewBox="0 0 24 24"
                                  fill="none"
                                  stroke="currentColor"
                                  strokeWidth="2"
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                              >
                                  <path d="M3 6h18" />
                                  <path d="M8 6V4h8v2" />
                                  <path d="M19 6l-1 14H6L5 6" />
                                  <path d="M10 11v5" />
                                  <path d="M14 11v5" />
                              </svg>
                          </button>
                      </div>
                  ))}

                </div>

            </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-3">

            <Button
                onClick={handleKnowledgeUpload}
                disabled={knowledgeFiles.length === 0 || knowledgeUploading}
            >
                {knowledgeUploading
                    ? "Uploading..."
                    : "Upload Documents"}
            </Button>


        </div>

        {/* Upload Success */}
        {uploadMessage && (
            <div className="rounded-lg border border-green-200 bg-green-50 p-3">
                <p className="text-sm text-green-700">
                    ✅ {uploadMessage}
                </p>
            </div>
        )}

        {/* Upload Error */}
        {datasetError && (
          <div className="mb-4 rounded-xl border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">
            {knowledgeError}
          </div>
        )}

        {/* Status */}
        <div className="rounded-xl border border-green-200 bg-green-50 p-4">

            <h4 className="font-semibold text-slate-800">
                📄 Knowledge Documents
            </h4>

            <p className="mt-1 text-sm text-slate-600">
                {knowledgeDocs.length} document{knowledgeDocs.length !== 1 ? "s" : ""} uploaded
            </p>

            <p
              className={`mt-2 text-sm ${
                  platformStatus === "ready"
                      ? "text-green-600"
                      : "text-amber-600"
              }`}
          >
              {platformStatus === "ready"
                  ? hasKnowledge
                      ? "Knowledge documents have been indexed successfully."
                      : "No knowledge documents uploaded. Customer insights will use structured business data only."
                  : hasKnowledge
                      ? "Knowledge documents will be indexed during platform processing."
                      : "No knowledge documents uploaded. You can still process the platform using the dataset only."}
          </p>

        </div>

        <Card>
            <CardHeader
                title="Platform Processing"
                subtitle="Run the complete ExecuMind AI initialization."
            />

            <div className="p-5 space-y-4">

                <div className="space-y-2">

                  <p>
                      {hasDataset ? "✅" : "⬜"} Dataset Uploaded
                  </p>

                  <p>
                      {hasKnowledge ? "✅" : "⬜"} Knowledge Documents (optional)
                  </p>

                  <p>
                      {platformStatus === "ready" ? "✅" : "⬜"} Platform Processed
                  </p>

              </div>

                <Button className={
                        platformStatus === "ready"
                            ? "bg-green-600 hover:bg-green-600"
                            : ""
                    }
                    onClick={handleProcessPlatform}
                    disabled={
                        !hasDataset ||
                      
                        platformStatus === "processing" ||
                        platformStatus === "ready"
                    }
                    fullWidth
                >
                    {platformStatus === "processing"
                        ? "⚙️ Processing..."
                        : platformStatus === "ready"
                        ? "✓ Platform Ready"
                        : "Process Platform"}
                </Button>
                {platformStatus === "ready" && (
                    <p className="mt-2 text-center text-sm text-green-600">
                        Platform is up to date.
                    </p>
                )}

                {platformStatus === "needs_processing" && (
                    <p className="mt-2 text-center text-sm text-amber-600">
                        New uploads detected. Process the platform to apply changes.
                    </p>
                )}
            </div>
        </Card>
        <h3 className="font-semibold text-slate-800">
            Uploaded Documents
        </h3>
        {/* Uploaded Documents */}
        <div className="space-y-3">

            {knowledgeDocs.map(doc => (

                <div
                    key={doc.name}
                    className="flex items-center justify-between rounded-lg border bg-white p-4"
                >

                    <div className="flex items-center gap-3">

                        {getFileIcon(doc.name)}

                        <div>

                            <p className="font-medium">
                                {doc.name}
                            </p>

                            <p className="text-sm text-slate-500">
                                {doc.type}
                            </p>

                        </div>

                    </div>

                    <div className="text-sm text-slate-500">
                        {doc.size} MB
                    </div>

                </div>

            ))}

        </div>

    </div>
</Card>
      {processResult && (
        <Card>
          <div className="p-6">

            <h2 className="text-lg font-semibold text-green-700">
              ✅ Platform Ready
            </h2>

            <p className="mt-2 text-sm text-slate-600">
              Dataset processing and knowledge indexing completed successfully.
            </p>

            <div className="mt-4 rounded-lg border border-green-200 bg-green-50 p-4">
              <p className="text-sm text-green-700">
                {processResult.rag.message}
              </p>

              {processResult.rag.documents > 0 ? (
                  <p className="mt-1 text-sm text-slate-600">
                      Knowledge Documents Indexed:
                      <strong> {processResult.rag.documents}</strong>
                  </p>
              ) : (
                  <div className="mt-2 space-y-1 text-sm text-slate-600">
                      <p>
                          <strong>Business Documents:</strong> Not Uploaded
                      </p>

                      <p>
                          <strong>Customer Reviews:</strong> Indexed Successfully
                      </p>
                  </div>
              )}
            </div>

            <div className="mt-6">
              <h3 className="mb-2 text-sm font-semibold text-slate-800">
                Tables Created
              </h3>

              <ul className="space-y-2">
                {processResult.ingestion.tables.map((table: string) => (
                  <li
                    key={table}
                    className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700"
                  >
                    ✅ {table}
                  </li>
                ))}
              </ul>
            </div>

          </div>
        </Card>
      )}

      {/* Dataset Library */}
      <Card>
        <CardHeader
          title="Dataset Library"
          subtitle="Version history of your e-commerce dataset"
          icon={
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
            >
              <ellipse
                cx="12"
                cy="5"
                rx="9"
                ry="3"
              />
              <path d="M3 5v14a9 3 0 0 0 18 0V5" />
              <path d="M3 12a9 3 0 0 0 18 0" />
            </svg>
          }
        />

        <div className="space-y-3 p-4">

          {loading ? (
            Array.from({ length: 3 }).map((_, i) => (
              <Skeleton
                key={i}
                className="h-20"
              />
            ))
          ) : datasets.length === 0 ? (

            <div className="rounded-xl border border-dashed border-slate-200 p-8 text-center text-sm text-slate-500">
              No datasets uploaded yet.
            </div>

          ) : (

            datasets.map((dataset) => (

              <div
                key={dataset.id}
                className="rounded-xl border border-slate-200 bg-white"
              >

                {/* Dataset header */}
                <div className="flex items-center justify-between border-b border-slate-100 p-4">

                  <div>
                    <h3 className="font-semibold text-slate-800">
                      {dataset.name}
                    </h3>

                    <p className="mt-1 text-xs text-slate-400">
                      {dataset.versions?.length ?? 0} version
                      {(dataset.versions?.length ?? 0) !== 1
                        ? "s"
                        : ""}
                    </p>
                  </div>

                </div>

                {/* Versions */}
                <div className="divide-y divide-slate-100">

                  {[...dataset.versions]
                    .sort((a, b) => {
                      if (a.is_active) return -1;
                      if (b.is_active) return 1;
                      return b.version - a.version;
                    }).map(
                    (version: any) => (

                      <div
                        key={version.id}
                        className="flex items-center justify-between gap-4 p-4"
                      >

                        <div className="min-w-0">

                          <div className="flex items-center gap-2">

                            <span className="font-medium text-slate-800">
                              Version {version.version}
                            </span>

                            {version.is_active && (
                              <Badge
                                variant="emerald"
                                tone="soft"
                                dot
                              >
                                Active
                              </Badge>
                            )}

                          </div>

                          <p className="mt-1 text-xs text-slate-400">
                            {version.files?.length ?? 0} files
                            {" · "}
                            {formatRelativeTime(
                              version.created_at
                            )}
                          </p>

                        </div>

                        <div className="flex items-center gap-2 shrink-0">
                          <button
                            onClick={() => setShowPreview(version)}
                            className="rounded-lg px-3 py-1.5 text-xs font-medium text-slate-500 hover:bg-slate-100 hover:text-slate-700"
                          >
                            Preview
                          </button>

                          {version.is_active ? (
                            <Badge variant="emerald" tone="soft">
                              Active
                            </Badge>
                          ) : (
                            <Button
                              size="sm"
                              variant="primary"
                              onClick={() =>
                                handleActivateVersion(dataset.id, version.id)
                              }
                            >
                              Use Version
                            </Button>
                          )}
                        </div>

                      </div>

                    )
                  )}

                </div>

              </div>

            ))

          )}

        </div>
      </Card>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50/50 p-3">
      <p className="text-[11px] uppercase tracking-wider text-slate-400">{label}</p>
      <p className="mt-0.5 font-display text-lg font-bold text-slate-900">{value}</p>
    </div>
  );
}
