// filepath: /Users/enesfurkankaya/Desktop/IOSL-2025-2026-Better-Readability-for-LLMs/index.js
const http = require("http");

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("Welcome to My App");
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
