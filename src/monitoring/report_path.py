from datetime import datetime, timezone
from pathlib import Path

# ye function hr monitoring run ke liye 
# ek unique JSON report path generate krega.
def create_report_path(
        reports_directory="reports",
):
    # reports directory ko Path object me convert kr rhe hai.
    reports_directory = Path(reports_directory)

    # current UTC time ko timestamp me convert kr rhe hai.
    # UTC use krne se reports ka timestamo timezone-independent rhega.
    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%m%SZ"
    )

    # timestamp ko filename me use krke unique report path bana rhe hai.
    report_path = (
        reports_directory
        / f"monitoring_report_{timestamp}.json"
    )

    # generated report path return kr rhe hai.
    return report_path