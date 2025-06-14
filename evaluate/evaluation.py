from uptrain import EvalLLM, Evals, Settings
import json

data = [
    {
        "question": "What is the capital of France?",
        "response": "The capital of France is Paris."
    },
]


settings = Settings(model='ollama/llama2:7b')

eval_llm = EvalLLM(settings)

results = eval_llm.evaluate(
    project_name = 'Ollama-Demo',
    data=data,
    checks=[Evals.FACTUAL_ACCURACY]
)

print(results)