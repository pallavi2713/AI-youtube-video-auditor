import uuid
import json
import logging 
from pprint import pprint

from dotenv import load_dotenv
load_dotenv(override =True)

from backend.src.graph.workflow import app

logging.basicConfig(
    level  =  logging.INFO,
    format  = "%(asctime)s - %(name)s -  %(levelname)s - %(message)s"
)
logger =  logging.getLogger("brand-guardian-runner")

def run_cli_simulation():
    """
       This func orchestrates the entire audit process:
       -create a unique session ID
       -prepae video url and metadata
       -Runs it through the AI langgraph workflow
       -Display the compliance result
    """
    session_id = str(uuid.uuid4())
    logger.info(f"Starting session with session id  :  {session_id}")    
    initial_inputs = {
        "video_url": "https://youtu.be/dT7S75eYhcQ",
        # "video_url": "https://www.youtube.com/watch?v=fS4cH2fky5M",
        "video_id": f"vid_{session_id[:8]}",
        "compliance_results" : [],
        "errors" : []
}
    
    print("--------------------Initialized workflow----------------")
    print(f"Input Payload : {json.dumps(initial_inputs,  indent = 2)} ")  
    try:
        final_state = app.invoke(initial_inputs)
        audit = final_state.get("audit_response", {})
        print("audit  :", audit)
        results = audit.get("compliance_results", [])
        status = audit.get("status", "UNKNOWN")
        report = audit.get("final_report", "No final report generated.")
        print("Fstate = ", final_state)
        print("\n" + "=" * 70)
        print("              BRAND COMPLIANCE AUDIT REPORT")
        print("=" * 70)

        print(f"\nVideo ID : {final_state.get('video_id')}")
        print(f"Status   : {status}")
        print(f"Violations Detected : {len(results)}")

        for i, issue in enumerate(results, 1):

            print("\n" + "-" * 70)
            print(f"VIOLATION #{i}")
            print("-" * 70)

            print(f"Category      : {issue.get('category')}")
            print(f"Severity      : {issue.get('severity')}")
            print(f"Evidence Type : {issue.get('evidence_type')}")
            print(
                f"Timestamp     : "
                f"{issue.get('start_time')} --> {issue.get('end_time')}"
            )

            print(f"\nEvidence:")
            print(f"  {issue.get('evidence')}")

            print(f"\nRule:")
            print(f"  {issue.get('rule')}")

            print(f"\nDescription:")
            print(f"  {issue.get('description')}")

        print("\n" + "=" * 70)
        print("FINAL REPORT")
        print("=" * 70)
        print(report)
        print("=" * 70)
    except Exception as e:
        logger.error(f"Workflow failed: {str(e)}")
        raise e
if __name__ == "__main__":
    run_cli_simulation()     