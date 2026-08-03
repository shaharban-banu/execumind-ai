import type {
  Kpi,
  IntelligenceItem,
  AiRecommendation,
  DatasetRecord,
  ChatMessage,
  ForecastResult,
  MetricTrend,
  SeriesPoint,
  
 
} from './types';

// ============================================================
// Mock data — stands in for the FastAPI backend responses.
// Replace the contents of api.ts with real fetch calls later.
// ============================================================

export const mockKpis: Kpi[] = [
  {
    id: 'revenue',
    label: 'Revenue',
    value: '$48.2M',
    rawValue: 48_200_000,
    changePct: 12.4,
    trend: 'up',
    spark: [32, 34, 33, 38, 41, 40, 44, 48],
    unit: 'currency',
    accent: 'brand',
    icon: 'revenue',
  },
  {
    id: 'orders',
    label: 'Orders',
    value: '18,640',
    rawValue: 18_640,
    changePct: 8.2,
    trend: 'up',
    spark: [14, 15, 14, 16, 16, 17, 18, 18.6],
    unit: 'count',
    accent: 'accent',
    icon: 'orders',
  },
  {
    id: 'customers',
    label: 'Customers',
    value: '12,385',
    rawValue: 12_385,
    changePct: 5.6,
    trend: 'up',
    spark: [10.8, 11.1, 11.3, 11.5, 11.8, 12.0, 12.2, 12.4],
    unit: 'count',
    accent: 'emerald',
    icon: 'customers',
  },
  {
    id: 'aov',
    label: 'Average Order Value',
    value: '$2,586',
    rawValue: 2586,
    changePct: 3.9,
    trend: 'up',
    spark: [2280, 2320, 2380, 2410, 2460, 2500, 2540, 2586],
    unit: 'currency',
    accent: 'amber',
    icon: 'aov',
  },
];





export const mockIntelligence: IntelligenceItem[] = [
  {
    id: 'intel-1',
    title: 'Competitor pricing shift detected in Enterprise tier',
    summary:
      'Northwind Corp reduced Enterprise pricing by 8% across SaaS bundles. Sentiment analysis suggests a market-share play ahead of Q3 enterprise renewal cycle.',
    category: 'Competitor',
    severity: 'high',
    confidence: 0.87,
    source: 'Market Intelligence Feed',
    timestamp: new Date(Date.now() - 1000 * 60 * 23).toISOString(),
    impact: 'Potential 4-6% churn risk in enterprise renewals this quarter.',
    tags: ['Pricing', 'Enterprise', 'Q3'],
    read: false,
  },
  {
    id: 'intel-2',
    title: 'Supply chain disruption flagged — APAC semiconductor channel',
    summary:
      'Lead times for critical components extending 18-26 days beyond baseline. Two tier-2 suppliers showing financial distress signals in payment-behavior model.',
    category: 'Risk',
    severity: 'critical',
    confidence: 0.92,
    source: 'Operations Risk Monitor',
    timestamp: new Date(Date.now() - 1000 * 60 * 90).toISOString(),
    impact: 'Estimated $1.8M revenue at risk if unmitigated through Q3.',
    tags: ['Supply Chain', 'APAC', 'Semiconductor'],
    read: false,
  },
  {
    id: 'intel-3',
    title: ' ARR growth accelerating in mid-market segment',
    summary:
      'Mid-market ARR grew 18% MoM, outpacing enterprise (6%) and SMB (4%). Expansion revenue driven by platform stickiness and upsell of analytics module.',
    category: 'Finance',
    severity: 'medium',
    confidence: 0.79,
    source: 'Financial Analytics Engine',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(),
    impact: 'Reinforce mid-market sales motion; reallocate 2 AE headcount.',
    tags: ['ARR', 'Mid-Market', 'Expansion'],
    read: true,
  },
  {
    id: 'intel-4',
    title: 'Regulatory change — EU AI Act compliance window narrowing',
    summary:
      'High-risk AI system obligations effective in 60 days. Current model documentation gaps identified in 3 product lines. Estimated 240 eng-hours to remediate.',
    category: 'Risk',
    severity: 'high',
    confidence: 0.94,
    source: 'Regulatory Watch',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 9).toISOString(),
    impact: 'Non-compliance exposure up to 6% of global revenue.',
    tags: ['Compliance', 'EU AI Act', 'Governance'],
    read: false,
  },
  {
    id: 'intel-5',
    title: 'Sentiment improving across NPS detractor cohort',
    summary:
      'Detractor NPS recovered from -22 to -9 over 6 weeks. Theme analysis attributes recovery to onboarding overhaul and support SLA improvements.',
    category: 'Operations',
    severity: 'low',
    confidence: 0.71,
    source: 'Customer Sentiment Model',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 26).toISOString(),
    impact: 'Positive signal for renewal probability; monitor for sustainment.',
    tags: ['NPS', 'Onboarding', 'Support'],
    read: true,
  },
  {
    id: 'intel-6',
    title: 'Market expansion opportunity — LATAM financial services',
    summary:
      'Demand signals rising 31% QoQ in LATAM fintech segment. Regulatory environment favorable. Two anchor prospects in pipeline worth $4.2M ACV.',
    category: 'Market',
    severity: 'medium',
    confidence: 0.68,
    source: 'Market Intelligence Feed',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 40).toISOString(),
    impact: 'Potential $12M incremental ARR over 12 months with localized motion.',
    tags: ['LATAM', 'Fintech', 'Expansion'],
    read: true,
  },
];

export const mockRecommendations: AiRecommendation[] = [
  {
  id: 'rec-1',
  title: 'Improve Customer Retention Strategy',
  rationale:
    'Customer reviews and repeat purchase analysis indicate declining customer satisfaction. Improving post-purchase engagement and customer support can reduce churn and increase customer lifetime value.',
  expectedImpact: 'Increase repeat purchases · Improve customer satisfaction',
  confidence: 0.86,
  category: 'Risk',
  status: 'pending',
  actions: [
    'Identify customers with declining purchase frequency',
    'Launch personalized retention campaigns',
    'Improve response time for customer support requests',
  ],
  riskLevel: 'medium',
  timeframe: 'This quarter',
  createdAt: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
},
  {
  id: 'rec-2',
  title: 'Reduce Delivery Delays Across Key Regions',
  rationale:
    'Delivery performance analysis indicates increasing delays in several regions, leading to lower customer satisfaction and negative reviews. Optimizing logistics partners and warehouse operations can significantly improve fulfillment performance.',
  expectedImpact: 'Improve on-time delivery · Increase customer satisfaction',
  confidence: 0.91,
  category: 'Operations',
  status: 'monitoring',
  actions: [
    'Identify regions with the highest delivery delays',
    'Optimize logistics partner allocation',
    'Monitor delivery performance through weekly KPI reports',
  ],
  riskLevel: 'high',
  timeframe: '30-45 days',
  createdAt: new Date(Date.now() - 1000 * 60 * 60 * 4).toISOString(),
},
  {
  id: 'rec-3',
  title: 'Increase Inventory for High-Demand Products',
  rationale:
    'Forecast analysis predicts increased demand for electronics and home appliances next month. Maintaining adequate inventory can prevent stockouts and maximize revenue opportunities.',
  expectedImpact: 'Reduce stockouts · Increase sales revenue',
  confidence: 0.78,
  category: 'Market',
  status: 'approved',
  actions: [
    'Increase inventory for forecasted high-demand products',
    'Coordinate with suppliers for timely replenishment',
    'Monitor inventory levels through weekly demand forecasts',
  ],
  riskLevel: 'low',
  timeframe: '2 weeks',
  createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 2).toISOString(),
},
 {
  id: 'rec-4',
  title: 'Improve Profitability of Low-Margin Products',
  rationale:
    'Sales analysis shows several products generating high sales volume but low profit margins. Reviewing pricing strategies and supplier costs can improve overall profitability.',
  expectedImpact: 'Increase profit margin · Improve revenue quality',
  confidence: 0.94,
  category: 'Finance',
  status: 'pending',
  actions: [
    'Identify low-margin product categories',
    'Review supplier pricing and procurement costs',
    'Optimize pricing strategy for underperforming products',
  ],
  riskLevel: 'high',
  timeframe: '2 weeks',
  createdAt: new Date(Date.now() - 1000 * 60 * 60 * 28).toISOString(),
},
];

export const mockRevenueTrend: MetricTrend = {
  label: 'Revenue',
  values: [28, 30, 31, 34, 36, 38, 41, 43, 45, 44, 47, 48],
};

export const mockSegmentMix: SeriesPoint[] = [
  { label: 'Mid-Market', value: 42 },
  { label: 'Enterprise', value: 33 },
  { label: 'SMB', value: 16 },
  { label: 'Strategic', value: 9 },
];

export const mockRiskMatrix: { name: string; likelihood: number; impact: number; severity: string }[] = [
  { name: 'Supply chain', likelihood: 82, impact: 76, severity: 'critical' },
  { name: 'EU AI Act', likelihood: 90, impact: 88, severity: 'critical' },
  { name: 'Pricing pressure', likelihood: 64, impact: 58, severity: 'high' },
  { name: 'Key talent loss', likelihood: 38, impact: 54, severity: 'medium' },
  { name: 'FX exposure', likelihood: 52, impact: 32, severity: 'medium' },
  { name: 'Cyber incident', likelihood: 24, impact: 82, severity: 'high' },
];

export const mockActivity: { id: string; label: string; detail: string; timestamp: string; type: string }[] = [
  { id: 'a1', label: 'New forecast generated', detail: 'Q3 revenue forecast · 94% confidence', timestamp: new Date(Date.now() - 1000 * 60 * 8).toISOString(), type: 'forecast' },
  { id: 'a2', label: 'Dataset uploaded', detail: 'customer_churn_2024.csv · 48,210 rows', timestamp: new Date(Date.now() - 1000 * 60 * 35).toISOString(), type: 'upload' },
  { id: 'a3', label: 'Recommendation approved', detail: 'Reallocate AEs to Mid-Market', timestamp: new Date(Date.now() - 1000 * 60 * 60 * 3).toISOString(), type: 'decision' },
  { id: 'a4', label: 'Intelligence alert raised', detail: 'Supply chain disruption · APAC', timestamp: new Date(Date.now() - 1000 * 60 * 90).toISOString(), type: 'alert' },
  { id: 'a5', label: 'Scenario modeled', detail: 'Recession scenario · 18% downside', timestamp: new Date(Date.now() - 1000 * 60 * 60 * 7).toISOString(), type: 'scenario' },
];

export const mockDatasets: DatasetRecord[] = [
  {
    id: 'ds-1',
    name: 'customer_churn_2024.csv',
    type: 'CSV',
    rows: 48210,
    columns: 24,
    size: '12.4 MB',
    status: 'ready',
    uploadedAt: new Date(Date.now() - 1000 * 60 * 35).toISOString(),
    quality: 96,
    preview: [
      { column: 'customer_id', type: 'string', sample: 'C-004821' },
      { column: 'tenure_months', type: 'integer', sample: '34' },
      { column: 'monthly_spend', type: 'float', sample: '2480.50' },
      { column: 'plan_tier', type: 'category', sample: 'Enterprise' },
      { column: 'churn_flag', type: 'boolean', sample: 'false' },
    ],
  },
  {
    id: 'ds-2',
    name: 'revenue_financials_q2.xlsx',
    type: 'Excel',
    rows: 1820,
    columns: 18,
    size: '3.1 MB',
    status: 'ready',
    uploadedAt: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
    quality: 99,
    preview: [
      { column: 'period', type: 'date', sample: '2024-06-30' },
      { column: 'segment', type: 'category', sample: 'Mid-Market' },
      { column: 'arr', type: 'float', sample: '4820000.00' },
      { column: 'gross_margin', type: 'float', sample: '0.782' },
    ],
  },
  {
    id: 'ds-3',
    name: 'market_signals_apac.json',
    type: 'JSON',
    rows: 9420,
    columns: 12,
    size: '8.7 MB',
    status: 'processing',
    uploadedAt: new Date(Date.now() - 1000 * 60 * 4).toISOString(),
    quality: 0,
    preview: [
      { column: 'signal_id', type: 'string', sample: 'SIG-9420' },
      { column: 'region', type: 'category', sample: 'APAC' },
      { column: 'sentiment', type: 'float', sample: '0.64' },
    ],
  },
  {
    id: 'ds-4',
    name: 'supply_chain_vendors.csv',
    type: 'CSV',
    rows: 342,
    columns: 31,
    size: '0.9 MB',
    status: 'ready',
    uploadedAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 3).toISOString(),
    quality: 88,
    preview: [
      { column: 'vendor_id', type: 'string', sample: 'V-0342' },
      { column: 'lead_time_days', type: 'integer', sample: '42' },
      { column: 'financial_health', type: 'float', sample: '0.71' },
    ],
  },
];

export const mockChat: ChatMessage[] = [
  {
    id: 'm1',
    role: 'assistant',
    content:
      `Hello! I'm ExecuMind AI.

        Ask me about:

        • Revenue
        • Sales
        • Customers
        • Forecasts
        • Executive strategy`,
    timestamp: new Date(Date.now() - 1000 * 60 * 12).toISOString(),
  },
];

export const mockForecast: ForecastResult = {
  points: [
    { label: 'Jan', historical: 32, forecast: null, lower: null, upper: null },
    { label: 'Feb', historical: 34, forecast: null, lower: null, upper: null },
    { label: 'Mar', historical: 33, forecast: null, lower: null, upper: null },
    { label: 'Apr', historical: 38, forecast: null, lower: null, upper: null },
    { label: 'May', historical: 41, forecast: null, lower: null, upper: null },
    { label: 'Jun', historical: 40, forecast: null, lower: null, upper: null },
    { label: 'Jul', historical: 44, forecast: null, lower: null, upper: null },
    { label: 'Aug', historical: 48, forecast: null, lower: null, upper: null },
    { label: 'Sep', historical: null, forecast: 51, lower: 47, upper: 55 },
    { label: 'Oct', historical: null, forecast: 53, lower: 48, upper: 58 },
    { label: 'Nov', historical: null, forecast: 56, lower: 50, upper: 62 },
    { label: 'Dec', historical: null, forecast: 59, lower: 52, upper: 66 },
  ],
  metrics: {
    accuracy: 94,
    confidence: 88,
    horizonDays: 120,
    model: 'ExecuMind-Foresight v3.2',
  },
  drivers: [
    { name: 'Mid-market expansion', contribution: 34, direction: 'up' },
    { name: 'Enterprise renewal rate', contribution: 22, direction: 'up' },
    { name: 'Seasonality (Q4)', contribution: 18, direction: 'up' },
    { name: 'Competitor pricing pressure', contribution: -14, direction: 'down' },
    { name: 'FX headwinds', contribution: -8, direction: 'down' },
  ],
};
