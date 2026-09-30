from __future__ import annotations

import json
from pathlib import Path


def recall_at_k(results: list[str], ground_truth: list[str], k: int) -> float:
    top_k = results[:k]
    hits = sum(1 for item in ground_truth if item in top_k)
    return hits / max(len(ground_truth), 1)


def mrr(results: list[str], ground_truth: list[str]) -> float:
    for index, item in enumerate(results, start=1):
        if item in ground_truth:
            return 1.0 / index
    return 0.0


def evaluate_retrieval(results_by_question: dict[str, list[str]], ground_truth: dict[str, list[str]]) -> dict:
    metrics = {"Recall@1": [], "Recall@3": [], "Recall@5": [], "MRR": []}
    for question_id, results in results_by_question.items():
        gt = ground_truth.get(question_id, [])
        metrics["Recall@1"].append(recall_at_k(results, gt, 1))
        metrics["Recall@3"].append(recall_at_k(results, gt, 3))
        metrics["Recall@5"].append(recall_at_k(results, gt, 5))
        metrics["MRR"].append(mrr(results, gt))
    return {
        "Recall@1": round(sum(metrics["Recall@1"]) / max(len(metrics["Recall@1"]), 1), 4),
        "Recall@3": round(sum(metrics["Recall@3"]) / max(len(metrics["Recall@3"]), 1), 4),
        "Recall@5": round(sum(metrics["Recall@5"]) / max(len(metrics["Recall@5"]), 1), 4),
        "MRR": round(sum(metrics["MRR"]) / max(len(metrics["MRR"]), 1), 4),
    }


def main() -> None:
    with Path(__file__).with_name("questions.json").open("r", encoding="utf-8") as handle:
        questions = json.load(handle)
    with Path(__file__).with_name("ground_truth.json").open("r", encoding="utf-8") as handle:
        truth = json.load(handle)
    results = {question["id"]: [question["question"]] for question in questions}
    print(evaluate_retrieval(results, truth))


if __name__ == "__main__":
    main()
