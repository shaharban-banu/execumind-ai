from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import ExecutiveRecommendation
import json
from schemas.executive import ExecutiveAnalysis


class ExecutiveRecommendationService:
    """
    Service for managing executive recommendations.
    """


    def delete_all(self):
        """
        Remove all existing recommendations.
        """
        db = SessionLocal()
        try:
            db.query(ExecutiveRecommendation).delete()
            db.commit()
        finally:
            db.close()
        
    def get_recommendations(self):
        """
        Return the latest executive report.
        """
        db = SessionLocal()
        try:
            recommendations=(db.query(ExecutiveRecommendation)
                             .order_by(ExecutiveRecommendation.created_at.desc()).all())
            if not recommendations:
                return None
            first=recommendations[0]
            return {
                "executive_summary":first.executive_summary,
                "key_findings":json.loads(first.key_findings),
                "business_risks":json.loads(first.business_risks),
                "strategic_recommendations":[
                    {
                        "priority":r.priority,
                        "action":r.action,
                        "rationale":r.rationale,
                    }for r in recommendations
                ],
                "evidence":json.loads(first.evidence),
            }
        finally:
            db.close()
    
    def save_recommendations(self, analysis: ExecutiveAnalysis):

        db = SessionLocal()

        try:

            db.query(ExecutiveRecommendation).delete()

            key_findings = json.dumps(analysis.key_findings)
            business_risks = json.dumps(analysis.business_risks)

            evidence = json.dumps([item.model_dump() for item in analysis.evidence])

            for recommendation in analysis.strategic_recommendations:

                record = ExecutiveRecommendation(
                    priority=recommendation.priority,
                    action=recommendation.action,
                    rationale=recommendation.rationale,
                    executive_summary=analysis.executive_summary,
                    key_findings=key_findings,
                    business_risks=business_risks,
                    evidence=evidence,
                )

                db.add(record)

            db.commit()

        finally:
            db.close()