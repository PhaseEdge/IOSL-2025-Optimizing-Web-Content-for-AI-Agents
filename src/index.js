const http = require("http");
// ** directly import as the below example
const PageFurkan = require("./pages/pageFurkan");

const server = http.createServer((req, res) => {
  if (req.url === "/") {
    res.writeHead(200, { "Content-Type": "text/plain" });
    res.end("Welcome to My App");
  }
  if (req.url === "/furkan") {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(PageFurkan());
  }
  if (req.url === "/sofia") {
    /* TODO Sofia*/
  }
  if (req.url === "/colin") {
    /* TODO Colin*/
  }
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
