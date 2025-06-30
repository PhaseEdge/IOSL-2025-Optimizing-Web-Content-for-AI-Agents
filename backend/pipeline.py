import json
from datetime import datetime
from pathlib import Path
import openai
import asyncio
from crawl4ai import AsyncWebCrawler
from helper_classes.model_controller import ModelController, ModelProvider

# Configuration
PROMPT_PATH = "../src/prompts/summary_prompt.txt"
OUTPUT_PATH = "../src/llm_outputs"
WEBSITE_LIST = [
    "http://localhost:3000/Tuberlinlandia",
    "http://localhost:3000/Tuberlinlandia-with-microdata",
    "http://localhost:3000/Tuberlinlandia-with-microdata-and-json-ld",
    "http://localhost:3000/Tuberlinlandia-with-json-ld"
]


# Logging
def log_experiment(website: str, query: str, model: str, output: str, filename: str = "backend/experiments.jsonl"):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "website": website,
        "query": query,
        "model": model,
        "output": output
    }
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

# Prompt Manager
class PromptManager:
    def __init__(self, prompt_path):
        self.prompt_path = Path(prompt_path)
    
    def load_prompt(self):
        try:
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Warning: Prompt file not found at {self.prompt_path}")
            return ""

# Crawler
class WebContentCrawler:
    async def crawl_content(self, url):
        async with AsyncWebCrawler(verbose=True) as crawler:
            try:
                result = await crawler.arun(url=url)
                if result.success:
                    return {
                        'success': True,
                        'content': result.markdown,
                        'url': url,
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Crawling failed',
                        'url': url,
                        'timestamp': datetime.now().isoformat()
                    }
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e),
                    'url': url,
                    'timestamp': datetime.now().isoformat()
                }

# Question Loader
def load_mock_questions(website: str, base_path="backend/questions"):
    domain_key = website.replace("http://localhost:3000/", "").replace(".", "_")
    question_file = Path(base_path) / f"{domain_key}.txt"
    with open(question_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# Main execution
async def run_full_evaluation():
    # prompt_manager = PromptManager(PROMPT_PATH)
    # prompt_template = prompt_manager.load_prompt()
    prompt_template = ""
    crawler = WebContentCrawler()
    all_results = []

    for website in WEBSITE_LIST:
        crawl_result = await crawler.crawl_content(website)
        if not crawl_result['success']:
            print(f"Crawling failed: {crawl_result['error']}")
            continue
        content = crawl_result['content']
        questions = load_mock_questions(website)

        for provider in ModelProvider:
            controller = ModelController(provider)
            for question in questions:
                full_prompt = f"{prompt_template}\n\nWebsite Content:\n{content}\n\nQuestion: {question}"
                try:
                    response_text = controller.generate_text(full_prompt)
                    result_data = {
                        "success": True,
                        "content": response_text,
                        "model": provider.value,
                        "question": question,
                        "timestamp": datetime.now().isoformat()
                    }
                except Exception as e:
                    print(e)
                    result_data = {
                        "success": False,
                        "error": str(e),
                        "model": provider.value,
                        "question": question,
                        "timestamp": datetime.now().isoformat()
                    }

                log_experiment(website, question, provider.value, result_data.get("content", "ERROR"))
                all_results.append((website, provider.value, question, result_data['success']))

    print("\n--- Evaluation complete ---")
    for w, m, q, s in all_results:
        print(f"{w} | {m} | {q[:30]}... | {'✓' if s else '✗'}")

if __name__ == "__main__":
    asyncio.run(run_full_evaluation())