from src.monitoring.report_storage import (
    load_latest_monitoring_report,
)

# ye function latest monitoring report load krke 
# important monitoring information extract krega.
def get_latest_monitoring_summary(reports_directory="reports"):
    # reports directory se sbse recent monitoring report load kr rhe hai.
    report = load_latest_monitoring_report(reports_directory)

    # latest report se important information extract kr rhe hai.
    summary = {
        "report_generated_at": (
            report["metadata"]["report_generated_at"]
        ),
        "model_version": (
            report["metadata"]["model_version"]
        ),
        "reference_dataset": (
            report["metadata"]["reference_dataset"]
        ),
        "overall_drift": (
            report["drift"]["summary"]["overall_drift"]
        ),
        "drifted_features": (
            report["drift"]["summary"]["drifted_features"]
        ),
        "overall_performance_degraded": (
            report["performance"]["summary"]["overall_performance_degraded"]
        ),
        "action": (
            report["decision"]["action"]
        ),
    }

    return summary

# ye function latest monitoring summary ko 
# human-readable format me teminal pr display krega.
def main():
    # latest monitoring summary retrieve kr rhe hai.
    summary = get_latest_monitoring_summary()

    # important monitoring information terminal pr print kr rhe hai.
    print("\nDriftGuard Monitoring Summary")
    print("============================")
    print(f"Report generated at: {summary['report_generated_at']}")
    print(f"Model version: {summary['model_version']}")
    print(f"Reference dataset: {summary['reference_dataset']}")
    print(f"Overall drift: {summary['overall_drift']}")
    print(f"Drifted features: {summary['drifted_features']}")
    print(
        "Performance degraded: "
        f"{summary['overall_performance_degraded']}"
    )
    print(f"Recommended action: {summary['action']}")

# ye block file ko directly run krne pr main() execute krega.
if __name__ == "__main__":
    main()