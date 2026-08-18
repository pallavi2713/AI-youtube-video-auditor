import os           # Access environment variables (like API keys)
os.environ["OTEL_SERVICE_NAME"] = "brand-guardian"
import logging      # Python's built-in logging system
from azure.monitor.opentelemetry import configure_azure_monitor  
# ↑ Azure's OpenTelemetry integration - tracks app performance, errors, requests

# ========== CREATE A DEDICATED LOGGER ==========
# Creates a named logger specifically for telemetry-related messages
# This separates telemetry logs from your main application logs
logger = logging.getLogger("brand-guardian-telemetry")
from dotenv import load_dotenv

load_dotenv()

def setup_telemetry():
    
    connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
  
    if not connection_string:
        # If the environment variable is missing/empty, telemetry won't work
        # 
        logger.warning("No Instrumentation Key found. Telemetry is DISABLED.")
        return  # Exit function early - don't try to configure Azure Monitor

    # ========== STEP 3: CONFIGURE AZURE MONITOR ==========
    try:
        logger.info(f"conn strl :{connection_string}")
        configure_azure_monitor(
            connection_string=connection_string,  # Where to send data
            logger_name="brand-guardian-tracer"   # Optional: custom tracer name
        )
        # 
        logger.info(" Azure Monitor Tracking Enabled & Connected!")
        
    except Exception as e:
        logger.error(f"----Failed to initialize Azure Monitor: {e}")
      
if __name__== "__main__":
    setup_telemetry()
            