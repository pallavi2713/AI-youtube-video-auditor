import uuid
import logging,os
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv


print(
    "APP INSIGHTS VAR EXISTS:",
    bool(os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"))
)

print(
    "APP INSIGHTS VAR LENGTH:",
    len(os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", ""))
)
# ============================================================
# TELEMETRY
# ============================================================

from backend.src.api.telemetry import setup_telemetry

setup_telemetry()


# ============================================================
# LANGGRAPH WORKFLOW
# ============================================================

from backend.src.graph.workflow import app as compliance_graph

from backend.src.graph.state import ComplianceAudit, AuditRequest
# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
# Azure SDK HTTP request/response logs
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("azure.core").setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline").setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(
    logging.WARNING
)

# Azure Application Insights exporter logs
logging.getLogger("azure.monitor").setLevel(logging.WARNING)
logging.getLogger("azure.monitor.opentelemetry.exporter").setLevel(
    logging.WARNING
)
logger = logging.getLogger("api-server")


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Brand Guardian AI API",
    description="API for auditing video content against brand compliance rules.",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ============================================================
# REQUEST MODEL
# ============================================================



@app.post("/audit", response_model=ComplianceAudit)
async def audit_video(request: AuditRequest):

    # --------------------------------------------------------
    # Generate unique session ID
    # --------------------------------------------------------

    session_id = str(uuid.uuid4())

    video_id = f"vid_{session_id[:8]}"

    logger.info(
        f"Received Audit Request: {request.video_url} "
        f"(Session: {session_id})"
    )

    # --------------------------------------------------------
    # Prepare LangGraph input
    # --------------------------------------------------------

    initial_inputs = {
        "video_url": request.video_url,
        "video_id": video_id,
        "compliance_results": [],
        "errors": []
    }

    try:

        # ----------------------------------------------------
        # Execute LangGraph
        # ----------------------------------------------------

        final_state = compliance_graph.invoke(initial_inputs)
        audit = final_state.get("audit_response", {})
        print("audit  :", audit)
        results = audit.get("compliance_results", [])
        status = audit.get("status","FAIL")
        report = audit.get("final_report", "No final report generated.")

        logger.info(
            f"Workflow completed successfully "
            f"(Session: {session_id})"
        )

        logger.info(f"Final state: {final_state}")


        # ----------------------------------------------------
        # Return API response
        # ----------------------------------------------------

        return ComplianceAudit(
            session_id=session_id,

            video_id=final_state.get(
                "video_id",
                video_id
            ),

            status=status,

            final_report=report,

            compliance_results=results
        )

    except Exception as e:

        logger.exception(
            f"Audit failed for session {session_id}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Workflow Execution Failed: {str(e)}"
        )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Brand Guardian AI"
    }