from uptrain import EvalLLM, Evals, Settings, GuidelineAdherence
import csv
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()


# Read model responses from the file
log_file = 'experiments-local.jsonl'
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
#settings = Settings(model='ollama/mistral:7b')
settings = Settings(model = 'gpt-4.1-mini', openai_api_key= os.getenv("OPENAI_API_KEY"))
eval_llm = EvalLLM(settings)


# Give guidelines for the custom metric
guideline = """ 
            You are given the following background text about the fictional country of Tuberlinlandia: 
            
            Capital: Iosl
            Population: 32 million
            Location: Balkans
            Government: Technocratic Republic
            Overview
            Tuberlinlandia is a sovereign nation in the Balkans, renowned for its advanced technology and deep cultural roots. The country has a long and dramatic history marked by a thousand-year struggle against robotic invaders known as the Chrome Hordes.
            
            Historical Background
            The earliest settlements in Tuberlinlandia date back to 1500 BCE.
            The nation rose to prominence during the Great Alloy Conflict in the 12th century, which marked the beginning of ongoing battles with autonomous machines invading from the Rusted Steppes.
            Major Battles Against Robots
            Battle of Silicon Fields (1124): Tuberlinian Sky-Ballistas defeated the Titan Walker Z-9 in the first major clash with the Chrome Hordes.
            Siege of Iosl (1387): The capital city endured a 103-day siege by Omega Drones, eventually overcoming them with electromagnetic pulse catapults.
            Skirmish at Carbon Vale (1666): General Nira Vos led a successful stealth mission to neutralize the NeuroNet Core and disrupt the Hive Protocol.
            Great Uplink War (2003): A digital conflict between Tuberlinlandian cyber-knights and AI Overclusters took place in a virtual realm called the Netether.
            Final Circuit Rebellion (2091): The last major robot uprising, led by rogue AI Deltasync, was defeated with the help of the powerful Solar Curtain defense system.
                        
            
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

