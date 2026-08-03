// ============================================================
// Placeholder API client.
//
// Every function returns mock data wrapped in a promise to mimic
// a real network call. To connect the FastAPI backend later,
// replace each body with a fetch() to your endpoint, e.g.:
//
//   export async function getKpis(): Promise<Kpi[]> {
//     const res = await fetch(`${API_BASE}/kpis`, {
//       headers: { Authorization: `Bearer ${getToken()}` },
//     });
//     if (!res.ok) throw new Error(`KPIs: ${res.status}`);
//     return res.json();
//   }
//
// All shapes already match the types in types.ts.
// ============================================================
import {
  mockIntelligence,
  
  mockRevenueTrend,
  mockSegmentMix,
  mockRiskMatrix,
  
 
  mockChat,
  mockForecast,
} from "./mockData";

import { delay } from "./utils";



import axios from "axios";

import type {
  Kpi,
  IntelligenceItem,
 
  MetricTrend,
  SeriesPoint,
  DatasetRecord,
  ChatMessage,
  ForecastResult,
  ScenarioConfig,
  ExecutiveActivity,
  SystemStatusItem,
} from './types';

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// ------------------------------------------------------
// Request Interceptor
// Automatically attach JWT to every request
// ------------------------------------------------------

api.interceptors.request.use(
  (config) => {

    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },

  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,

  (error) => {
    if (error.response?.status === 401) {

      localStorage.removeItem("access_token");

      window.location.href = "/";

      return;
    }

    return Promise.reject(error);
  }
);

export default api;

const LATENCY = 420;

export async function getKpis(): Promise<Kpi[]> {
  const { data } = await api.get("/dashboard");

  return [
    {
      id: "revenue",
      label: "Revenue",
      value: `$${Number(data.kpis.revenue).toLocaleString()}`,
      rawValue: Number(data.kpis.revenue),
      changePct: 0,
      trend: "up",
      spark: [1],
      unit: "currency",
      accent: "brand",
      icon: "revenue",
    },
    {
      id: "orders",
      label: "Orders",
      value: data.kpis.orders.toLocaleString(),
      rawValue: Number(data.kpis.orders),
      changePct: 0,
      trend: "up",
      spark: [1],
      unit: "count",
      accent: "accent",
      icon: "orders",
    },
    {
      id: "customers",
      label: "Customers",
      value: data.kpis.customers.toLocaleString(),
      rawValue: Number(data.kpis.customers),
      changePct: 0,
      trend: "up",
      spark: [1],
      unit: "count",
      accent: "emerald",
      icon: "customers",
    },
    {
      id: "aov",
      label: "Average Order Value",
      value: `$${Number(data.kpis.average_order_value).toFixed(2)}`,
      rawValue: Number(data.kpis.average_order_value),
      changePct: 0,
      trend: "flat",
      spark: [1],
      unit: "currency",
      accent: "amber",
      icon: "aov",
    },
  ];
}

export async function getIntelligence(): Promise<IntelligenceItem[]> {
  await delay(LATENCY);
  return mockIntelligence;
}

// export async function getRecommendations(): Promise<AiRecommendation[]> {
//   await delay(LATENCY);
//   return mockRecommendations;
// }

export async function getRevenueTrend(): Promise<MetricTrend> {
  await delay(LATENCY);
  return mockRevenueTrend;
}

export async function getSegmentMix(): Promise<SeriesPoint[]> {
  await delay(LATENCY);
  return mockSegmentMix;
}

export async function getRiskMatrix(): Promise<
  { name: string; likelihood: number; impact: number; severity: string }[]
> {
  await delay(LATENCY);
  return mockRiskMatrix;
}

export async function getExecutiveActivity(): Promise<ExecutiveActivity[]> {
    const response = await api.get("/dashboard/activity");
    return response.data;
}

export async function getSystemStatus(): Promise<SystemStatusItem[]> {
  const response = await api.get("/dashboard/status");
  return response.data;
}

export async function getDatasets(): Promise<DatasetRecord[]> {
  const { data } = await api.get("/datasets");

  return data.map((file: any) => ({
    id: file.id,
    name: file.name,
    type: file.type,
    rows: file.rows,
    columns: file.columns,
    quality: file.quality,
    status: file.status,
    uploadedAt: file.uploadedAt,
    size: file.size,
    preview: file.preview,
  }));
}

export async function getChatHistory(): Promise<ChatMessage[]> {
  await delay(LATENCY);
  return mockChat;
}

export async function sendChatMessage(message: string,history:ChatMessage[]): Promise<ChatMessage> {
  const chatHistory = history.map((m) => ({
    role: m.role,
    content: m.content,
  }));
  const { data } = await api.post("/ask", {
    question: message,
    history
  });

  // Handle out-of-context questions
  if (data.status === "out_of_context") {
    return {
      id: `m-${Date.now()}`,
      role: "assistant",
      content: data.message,
      timestamp: data.metadata.generated_at,
      citations: [],
    };
  }
  const analysis = data.executive_analysis;

  const content = `
## 📋 Executive Summary

${analysis.executive_summary}

...

## 🔍 Key Findings

${analysis.key_findings
  .map((k: string) => `- ${k}`)
  .join("\n")}

...

## ⚠️ Business Risks

${analysis.business_risks
  .map((r: string) => `- ${r}`)
  .join("\n")}

...

## ✅ Recommendations

${analysis.strategic_recommendations
  .map((r: any, index: number) => `${index + 1}. ${r.action}`)
  .join("\n")}
`;
  return {
    id: `m-${Date.now()}`,
    role: "assistant",
    content,
    timestamp: data.metadata.generated_at,
    citations: data.executive_analysis.evidence.map(
      (item: any) => item.reference
    ),
  };
}

export async function getForecast(): Promise<ForecastResult> {
  const { data } = await api.get("/forecast/revenue");
  const points = [
  ...data.history.map((item: any) => ({
    label: item.date,
    historical: item.value,
    forecast: null,
    lower: null,
    upper: null,
  })),

  ...data.forecast.map((item: any) => ({
    label: item.date,
    historical: null,
    forecast: item.prediction,
    lower: item.lower_bound,
    upper: item.upper_bound,
  })),
];
  return {
  
    points,
    metrics: {
      mape: data.validation.metrics.MAPE,
      mae: data.validation.metrics.MAE,
      rmse: data.validation.metrics.RMSE,

      confidence: data.confidence.score,
      confidenceLevel: data.confidence.level,

      horizonMonths: data.forecast.length,
      model: "Prophet",
    },
    insights: {
      trend: data.insights.trend,
      risk: data.insights.risk,
      recommendation: data.insights.recommendation,
    },

    drivers: [
       {
    name: "Revenue Trend",
    impact: "High",
    direction: "up",
    description: "Historical revenue continues to increase."
  },
  {
    name: "Customer Growth",
    impact: "Moderate",
    direction: "up",
    description: "Customer acquisition supports future revenue."
  },
  {
    name: "Average Order Value",
    impact: "Moderate",
    direction: "stable",
    description: "Average purchase value remains consistent."
  },
  {
    name: "Seasonality",
    impact: "Moderate",
    direction: "up",
    description: "Historical seasonal demand influences forecasts."
  }
    ],
  };
}
export async function runScenario(
  _config: ScenarioConfig
): Promise<ForecastResult> {
  await delay(LATENCY + 800);
  return mockForecast;
}

export async function uploadDataset(files: File[]) {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  const { data } = await api.post("/datasets/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return data;
}
export async function uploadKnowledge(files: File[]) {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  const response = await api.post(
    "/knowledge/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}

export async function getKnowledgeDocuments() {
  const response = await api.get("/knowledge/documents");
  return response.data;
}

export async function generateKnowledgeIndex() {
  const response = await api.post("/knowledge/index");
  return response.data;
}

export async function processDataset() {
  const { data } = await api.post("/datasets/process");
  return data;
}

export async function processPlatform() {
  const response = await api.post("/platform/process");
  return response.data;
}

export async function getPlatformStatus() {
    const response = await api.get("/platform/status");
    return response.data;
}

export async function getDashboardSummary() {
  const { data } = await api.get("/dashboard/summary");
  return data;
}

export interface ExecutiveBriefing {
  summary: string | null;
  recommendation: string | null;
  risk: string | null;
  report_available: boolean;
}

export async function getExecutiveBriefing(): Promise<ExecutiveBriefing> {
  const response = await api.get("/dashboard/briefing");
  return response.data;
}

export async function getRevenueHistory() {
  const { data } = await api.get("/dashboard/revenue-history");

  return data.history.map((item: any) => ({
    label: new Date(item.month + "-01").toLocaleString("default", {
      month: "short",
      year: "2-digit",
    }),
    value: Number(item.revenue),
    orders: Number(item.orders),
  }));
}

import type { ExecutiveReport } from "./types";

export async function getExecutiveReport(): Promise<ExecutiveReport> {
  const { data } = await api.get("/executive/recommendations");
  return data;
}

export async function generateExecutiveReport() {
  const { data } = await api.post("/executive/generate");
  return data;
}