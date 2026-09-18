from app.graph.workflow import graph


def main():
    query = input("\nEnter your research question: ").strip()

    if not query:
        print("Query cannot be empty.")
        return

    initial_state = {
        "query": query,
        "route": "",
        "research": "",
        "sources": [],
        "analysis": "",
        "fact_check": "",
        "final_report": "",
        "citation_validation": {},
        "citation_accuracy": 0.0,
        "source_utilization": 0.0,
        "citation_retry_count": 0,
        "citation_feedback": "",
        "relevance_score": 0.0,
        "completeness_score": 0.0,
        "factuality_score": 0.0,
        "overall_score": 0.0,
    }

    print("\nRunning research workflow...\n")

    try:
        result = graph.invoke(initial_state)

    except Exception as exc:
        print(f"\nWorkflow failed: {exc}")
        return

    print("\n" + "=" * 70)
    print("FINAL REPORT")
    print("=" * 70)

    print(result["final_report"])

    print("\n" + "=" * 70)
    print("EVALUATION")
    print("=" * 70)

    print(f"Relevance:      {result['relevance_score']:.2f}")
    print(f"Completeness:   {result['completeness_score']:.2f}")
    print(f"Factuality:     {result['factuality_score']:.2f}")
    print(f"Overall Score:  {result['overall_score']:.2f}")

    print("\n" + "=" * 70)
    print("CITATION METRICS")
    print("=" * 70)

    print(f"Citation Accuracy:  {result['citation_accuracy']:.2f}")
    print(f"Source Utilization: {result['source_utilization']:.2f}")


if __name__ == "__main__":
    main()