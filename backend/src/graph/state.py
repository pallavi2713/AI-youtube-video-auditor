import operator
from typing import Annotated, List, Dict, Optional, Any, TypedDict
# backend/src/models/audit_models.py

from typing import List, Literal
from pydantic import BaseModel, Field

class AuditRequest(BaseModel):
    video_url: str
# Error Report
# define the schema for a single compliance result
class ComplianceIssue(TypedDict):
    category : str
    description : str #sepcific detail of violation
    severity : str   #critical | warning
    timestamp : Optional[str]

# definethe global graph state
# this defines the state that gets passed around in the agentic workflow
class VideoAuditState(TypedDict):
     '''
     Defines the data schema for langgraph execution content
     '''
     #input parameters
     video_url :  str
     video_id : str
     
     #ingestion and extraction data
     local_file_path : Optional[str]
     video_metadata : Optional[str]
     transcript_segments:Optional[str]
     transcript : Optional[str]
     ocr_Text :   Optional[str]    
     
     #analysis output
     # stores the list of all violations found by AI
     compliance_results : Annotated[List[ComplianceIssue],operator.add]
     audit_response: dict
     # final deliverables:
     final_status : str # PASS | FAIL
     final_report : str # markdown_format
      
     #system observability
     #errors: API timeout, system level errors
     errors  : Annotated[List[str], operator.add]


class ComplianceResult(BaseModel):
    category: str = Field(
        description="Compliance category, e.g. Claim Validation, Intellectual Property"
    )

    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]

    evidence_type: Literal["TRANSCRIPT", "VIDEO", "TRANSCRIPT_AND_VIDEO"]

    start_time: str = Field(
        description="Start timestamp of the violating evidence in the video"
    )

    end_time: str = Field(
        description="End timestamp of the violating evidence in the video"
    )

    evidence: str = Field(
        description="Exact transcript or OCR evidence that caused the violation"
    )

    rule: str = Field(
        description="Official regulatory rule that applies"
    )

    description: str = Field(
        description="Explanation of why the evidence violates the rule"
    )
    recommendation:str = Field(
        description="Recommended action to resolve the violation and make the content compliant with the applicable rule"
    )
    confidence: float = Field(
        description="Confidence score indicating how certain the auditor is that the identified evidence violates the specified rule, ranging from 0.0 to 1.0",
        ge=0.0,
        le=1.0
    )


class ComplianceAudit(BaseModel):
    compliance_results: List[ComplianceResult] = Field(
        default_factory=list,
        description="List of compliance violations identified in the video."
    )

    status: Literal["PASS", "FAIL", "REVIEW"] = Field(
        description="Overall compliance status of the video."
    )

    final_report: str = Field(
        description="Overall summary of the compliance audit findings and final decision."
    )   