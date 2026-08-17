// ============================================================
// Domain types for ExecuMind AI
// Backend API is provided by an external FastAPI service.
// These types mirror the expected API contracts.
// ============================================================

export type Trend = 'up' | 'down' | 'flat';

export interface Kpi {
  id: string;
  label: string;
  value: string;
  rawValue: number;
  changePct: number;
  trend: Trend;
  spark: number[];
  unit?: 'currency' | 'percent' | 'count';
  accent: 'brand' | 'accent' | 'emerald' | 'amber';
  icon: 'revenue' | 'orders' | 'customers' | 'aov';
}

export interface ExecutiveActivity {
  id: string;
  label: string;
  detail: string;
  timestamp: string;
  type: 'forecast' | 'upload' | 'decision' | 'alert' | 'scenario' | 'insight' | 'agent';
  actor?: string;
}

export interface SystemStatusItem {
  id: string;
  label: string;
  status: 'operational' | 'degraded' | 'down';
  detail: string;
  
}

export type IntelligenceCategory =
  | 'Market'
  | 'Risk'
  | 'Operations'
  | 'Finance'
  | 'Competitor';

export type Severity = 'critical' | 'high' | 'medium' | 'low';

export interface IntelligenceItem {
  id: string;
  title: string;
  summary: string;
  category: IntelligenceCategory;
  severity: Severity;
  confidence: number;
  source: string;
  timestamp: string;
  impact: string;
  tags: string[];
  read: boolean;
}

export type DecisionStatus = 'pending' | 'approved' | 'rejected' | 'monitoring';

export interface AiRecommendation {
  id: string;
  title: string;
  rationale: string;
  expectedImpact: string;
  confidence: number;
  category: IntelligenceCategory;
  status: DecisionStatus;
  actions: string[];
  riskLevel: Severity;
  timeframe: string;
  createdAt: string;
}

export interface MetricTrend {
  label: string;
  values: number[];
}

export interface SeriesPoint {
  label: string;
  value: number;
}


export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  citations?: string[];
  thinking?: boolean;
}

export interface ForecastPoint {
  label: string;
  historical: number | null;
  forecast: number | null;
  lower: number | null;
  upper: number | null;
}

export interface ScenarioConfig {
  revenueGrowth: number;
  costChange: number;
  headcountChange: number;
  marketVolatility: number;
}

export interface ForecastDriver {
  name: string;
  impact: "High" | "Moderate" | "Low";
  direction: "up" | "down" | "stable";
  description: string;
}

export interface ForecastResult {
  points: ForecastPoint[];

  metrics: {
    mape: number;
    mae: number;
    rmse: number;

    confidence: number;
    confidenceLevel: string;

    horizonMonths: number;
    model: string;
  };

  insights: {
    trend: string;
    risk: string;
    recommendation: string;
  }

  drivers: ForecastDriver[];
}

export interface Evidence {
  source: string;
  reference: string;
  text: string;
}

export interface ExecutiveRecommendation {
  priority: string;
  action: string;
  rationale: string;
}

export interface ExecutiveReport {
  executive_summary: string;
  key_findings: string[];
  business_risks: string[];
  strategic_recommendations: ExecutiveRecommendation[];
  evidence: Evidence[];
  generated_at:string;
}

export interface DatasetVersion {
  id: number;
  version: number;
  is_active: boolean;
  created_at: string;
  files: {
    id: number;
    name: string;
    type: string;
    rows: number;
    columns: number;
    quality: number;
    size: string;
  }[];
}

export interface DatasetRecord {
  id: number;
  name: string;
  created_at: string;
  versions: DatasetVersion[];
}