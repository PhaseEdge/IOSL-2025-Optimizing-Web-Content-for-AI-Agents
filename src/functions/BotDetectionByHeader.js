const isBot = userAgent => {
  // List of common bot User-Agent patterns
  const llmBotPatterns = [
    /openai/i,
    /chatgpt/i,
    /gpt-?[\d]/i,
    /bard/i,
    /claude/i,
    /anthropic/i,
    /llm/i,
    /huggingface/i,
    /python-requests/i,
    /httpx/i,
    /curl/i
  ]
  return llmBotPatterns.some(pattern => pattern.test(userAgent))
}

module.exports = isBot
