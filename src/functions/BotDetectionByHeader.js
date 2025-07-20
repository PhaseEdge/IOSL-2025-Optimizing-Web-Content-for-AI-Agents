const isBot = userAgent => {
  // List of common bot User-Agent patterns
  const llmBotPatterns = [
    /chatgpt/i,
    /gptbot/i,
    /gpt-?[\d]/i,
    /chatgpt-user/i,
    /oai-searchbot/i,
    /perplexitybot/i,
    /perplexity-user/i,
    /mistralai-user/i,
    /claudebot/i,
    /claude/i,
    /anthropic/i,
    /bard/i,
    /huggingface/i
  ]
  return llmBotPatterns.some(pattern => pattern.test(userAgent))
}

module.exports = isBot
