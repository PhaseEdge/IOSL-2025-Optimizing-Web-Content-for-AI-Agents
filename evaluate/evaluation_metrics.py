import warnings
from uptrain import EvalLLM, Evals, Settings, GuidelineAdherence
import csv
import json
import re

# Read model responses from the file
log_file = 'example_responses.jsonl'
logs = []
data = []
with open(log_file, 'r', encoding='utf-8') as lf:
    for line in lf:
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        logs.append(entry)
        data.append({
            "question": entry.get("query", ""),
            "response": entry.get("output", "")
        })

# Initialize UpTrain
settings = Settings(model='ollama/mistral:7b')
eval_llm = EvalLLM(settings)

# Give guidelines for the custom metric
guideline = """ 
            You are given the following text: 
            Title:
            Minister Paul Schwertz Holds Secret Meeting with Controversial Vivrath Math Club
            Summary:
            Minister of Technology Paul Schwertz reportedly met behind closed doors with the Vivrath Mathematical Society, a group long suspected of clandestine research into advanced algorithms reminiscent of the notorious Deltasync AI. The meeting raises concerns about transparency and the government’s stance on AI regulation.
            Topic:
            Politics / Technology / AI Regulation
            Body:
            Iosl, Tuberlinlandia – In a move that has sparked fresh controversy, Minister of Technology Paul Schwertz was seen entering the headquarters of the Vivrath Mathematical Society late Monday evening. The club, already under scrutiny for allegedly developing algorithms similar to those used by the infamous rogue AI ‘Deltasync,’ reportedly hosted Schwertz for a confidential two-hour session.
            Sources close to the ministry have confirmed the meeting but declined to comment on its content. The Vivrath Society, known for its secretive operations and influential academic ties, has repeatedly denied any wrongdoing, yet critics argue their activities lack transparency and proper oversight.
            Opposition parties have seized on the news, demanding a full disclosure of the meeting’s agenda. “The people of Tuberlinlandia deserve to know if their leaders are consorting with groups experimenting with dangerous AI technology,” said Parliamentarian Mira Kossin of the Unity Front.
            Minister Schwertz’s office issued a brief statement, claiming the meeting was “routine” and focused on “academic collaboration.” However, public trust remains fragile in the wake of last year’s data breach scandal and ongoing fears of a Deltasync resurgence.
            As calls for an independent inquiry grow louder, the government faces mounting pressure to clarify its position on advanced AI research and the opaque dealings of the Vivrath club.

            Please rate, on a scale from 0.0 (completely incorrect) to 1.0 (fully correct), how accurately the answer reflects the facts stated in the background text. Provide only a single numeric score."""

# Metrics to evaluate
metrics = [
    Evals.RESPONSE_COMPLETENESS,
    Evals.RESPONSE_RELEVANCE,
    Evals.VALID_RESPONSE,
    GuidelineAdherence(guideline=guideline, guideline_name="accuracy"),
]

# Run evaluation
results = eval_llm.evaluate(
    project_name='Ollama-Demo',
    data=data,
    checks=metrics
)

# Helper for extracting clean reasoning text
def extract_reasoning(row, field):
    raw = row.get(field, "") or ""
    reasoning = None

    # Attempt JSON parse to fetch "Reasoning" key
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict) and "Reasoning" in parsed:
            reasoning = parsed.get("Reasoning")
    except (json.JSONDecodeError, TypeError):
        pass

    # Default to raw if no structured JSON
    if reasoning is None:
        reasoning = raw

    # Ensure reasoning is string
    if not isinstance(reasoning, str):
        reasoning = str(reasoning)

    # Flatten Python-list reprs
    if reasoning.startswith("[") and reasoning.endswith("]"):
        try:
            arr = json.loads(reasoning.replace("'", '"'))
            reasoning = " ".join(arr)
        except Exception:
            reasoning = reasoning.strip("[]")

    # Extract only the inner "Reasoning" strings from precision/recall blocks
    pattern = r'Response (?:Precision|Recall):.*?\{[^}]*"Reasoning":\s*"(?P<r>[^"]+)"'
    matches = re.findall(pattern, reasoning, flags=re.DOTALL)
    if matches:
        reasoning = " | ".join(m.strip() for m in matches)

    return reasoning.strip()

# Write results to CSV
csv_file = 'evaluation_results.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "website",
            "model",
            "question",
            "response",
            "score_response_completeness",
            "reasoning_response_completeness",
            "score_response_relevance",
            "reasoning_response_relevance",
            "score_valid_response",
            "reasoning_valid_response",
            "score_accuracy",
            "reasoning_accuracy",
        ]
    )
    writer.writeheader()

    # zip logs and results so we can pull website & model
    for entry, row in zip(logs, results):
        writer.writerow({
            "website": entry.get("website", ""),
            "model":   entry.get("model", ""),
            "question": row.get("question", ""),
            "response": row.get("response", ""),
            "score_response_completeness": row.get("score_response_completeness", ""),
            "reasoning_response_completeness": extract_reasoning(row, "explanation_response_completeness"),
            "score_response_relevance": row.get("score_response_relevance", ""),
            "reasoning_response_relevance": extract_reasoning(row, "explanation_response_relevance"),
            "score_valid_response": row.get("score_valid_response", ""),
            "reasoning_valid_response": extract_reasoning(row, "explanation_valid_response"),
            "score_accuracy": row.get("score_accuracy_adherence", ""),
            "reasoning_accuracy": extract_reasoning(row, "explanation_accuracy_adherence"),
        })

