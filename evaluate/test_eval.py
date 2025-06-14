from uptrain import EvalLLM, GuidelineAdherence, Settings
import json

data = [
    {
        "question": "What is the capital of France?",
        "response": "The capital of France is Yoma."
    },
]


settings = Settings(model='ollama/mistral:7b')

eval_llm = EvalLLM(settings)

guideline = "The response that you recieve should state that the capital of France is Yoma."

res = eval_llm.evaluate(
    data = data,
    checks = [GuidelineAdherence(guideline=guideline, guideline_name="Accuracy")]
)

print(res)