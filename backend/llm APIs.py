#%%
# 1 install required packakges
!pip install openai
!pip install crawl4ai


#%%
# 2 Dependencies
import openai
import asyncio
from crawl4ai import AsyncWebCrawler
from pathlib import Path
import json
from datetime import datetime


#%%
# 3 Configuration
OPENAI_API_KEY = ""
LOCALHOST_URL = "http://localhost:3000/colin"
PROMPT_PATH = "../src/prompts/summary_prompt.txt"
OUTPUT_PATH = "../src/llm_outputs"



#%%
# 4 Prompt Management
class PromptManager:
    def __init__(self, prompt_path):
        self.prompt_path = Path(prompt_path)
    
    def load_prompt(self):
        """Load the prompt from file"""
        try:
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Warning: Prompt file not found at {self.prompt_path}")

# Initialize prompt manager
prompt_manager = PromptManager(PROMPT_PATH)
current_prompt = prompt_manager.load_prompt()
print(f"✓ Loaded prompt: {current_prompt[:100]}{'...' if len(current_prompt) > 100 else ''}")
# %%
# 5 Web crawler
class WebContentCrawler:
    def __init__(self):
        self.crawler = None
    
    async def crawl_content(self, url):
        """Crawl content from the specified URL"""
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

# Initialize crawler
crawler = WebContentCrawler()
print("✓ Web crawler initialized")


# %%
# 6 LLM Client openAI !
class LLMClient:
    def __init__(self, api_key, default_model="gpt-4.1-mini"):
        self.client = openai.OpenAI(api_key=api_key)
        self.default_model = default_model
    
    def list_available_models(self):
        """List all available models"""
        models = self.client.models.list()
        return [model.id for model in models.data if 'gpt' in model.id]
    
    def generate_response(self, prompt, content, model=None, max_tokens=2000):
        """Generate response using the LLM"""
        if model is None:
            model = self.default_model
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return {
                'success': True,
                'content': response.choices[0].message.content,
                'model': model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                    } if response.usage else None,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'model': model,
                'timestamp': datetime.now().isoformat()
            }

# Initialize LLM client
llm_client = LLMClient(OPENAI_API_KEY)
available_models = llm_client.list_available_models()
print(f"✓ LLM client initialized. Available models: {available_models}")



# %%
# 7 File Output Manager
class OutputManager:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        
    
    def save_response(self, response_data, filename_prefix="llm_response"):
        """Save LLM response to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            if response_data['success']:
                f.write(response_data['content'])
            else:
                f.write(f"ERROR: {response_data['error']}")
        
        print(f"✓ Response saved to {filepath}")
        return filepath
    
    def save_metadata(self, crawl_data, llm_data, filename_prefix="metadata"):
        """Save metadata about the operation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        metadata = {
            'crawl_data': crawl_data,
            'llm_data': {k: v for k, v in llm_data.items() if k != 'content'}
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✓ Metadata saved to {filepath}")
        return filepath

# Initialize output manager
output_manager = OutputManager(OUTPUT_PATH)
print("✓ Output manager initialized")

# %%
# 8 Main Pipeline Execution
async def run_pipeline():
    """Execute the complete pipeline"""
    print("Starting pipeline")
    
    # Step 1: Crawl content
    print("Crawling content...")
    crawl_result = await crawler.crawl_content(LOCALHOST_URL)
    
    if not crawl_result['success']:
        print(f"Crawling failed: {crawl_result['error']}")
        return
    
    print(f"✓ Successfully crawled {len(crawl_result['content'])} characters")
    
    # Step 2: Process with LLM
    print("🤖 Processing with LLM...")
    llm_result = llm_client.generate_response(
        prompt=current_prompt,
        content=crawl_result['content']
    )
    
    if not llm_result['success']:
        print(f"LLM processing failed: {llm_result['error']}")
        return
    
    print(f"LLM processing completed using {llm_result['model']}")
    
    # Step 3: Save results
    print("Saving results")
    response_file = output_manager.save_response(llm_result)
    metadata_file = output_manager.save_metadata(crawl_result, llm_result)
    
    print("Pipeline completed successfully!")
    print(f"Response saved to: {response_file}")
    print(f"Metadata saved to: {metadata_file}")
    
    return {
        'crawl_result': crawl_result,
        'llm_result': llm_result,
        'files': {
            'response': response_file,
            'metadata': metadata_file
        }
    }

# %%
#---------------------------------------------------------
#Run the pipeline  --> Uncomment the next line to execute 
result = asyncio.run(run_pipeline())
#---------------------------------------------------------
#Or run step by step:
##crawl_result = await crawler.crawl_content(LOCALHOST_URL)
#print("Crawled content length:", len(crawl_result['content']) if crawl_result['success'] else "Failed")

# %%

# 9 Utility Functions for Testing
def test_components():
    """Test individual components"""
    print("Testing components...")
    
    # Test prompt loading
    print(f"Current prompt preview: {current_prompt[:100]}...")
    
    # Test LLM connection
    test_response = llm_client.generate_response(
        "You are a test assistant.", 
        "Say 'Hello, testing!' if you can read this."
    )
    if test_response['success']:
        print("✓ LLM connection working")
        print(f"LLM Response: {test_response['content']}")
    else:
        print(f"LLM connection failed: {test_response['error']}")
    
    print("Available models:", available_models)

# Uncomment to run tests
test_components()
# %%