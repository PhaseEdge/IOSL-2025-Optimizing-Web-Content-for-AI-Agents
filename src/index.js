const http = require('http')
const fs = require('fs')
const path = require('path')
const isBot = require('./functions/BotDetectionByHeader')
const hasSuspiciousHeaders = require('./functions/BotDetectionByMissingInfo')
const generateLLMFile = require('./functions/GenerateLLMFile')
const tablePage1Data = require('./data/tablePage1Data.js')

const server = http.createServer((req, res) => {
  console.log(req.url, 'reql*****')
  // detect AI Agent and log
  console.log('Headers:', req.headers)
  const userAgent = req.headers['user-agent'] || 'Unknown'
  const ip = req.socket.remoteAddress || 'Unknown IP'
  const isAIAgent = isBot(userAgent)

  if (isAIAgent || hasSuspiciousHeaders(req.headers)) {
    res.writeHead(302, { Location: '/api/people/table-page-1-llm' })
    res.end()
    return
  }

  const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon'
  }

  const ext = path.extname(req.url)
  const mimeType = mimeTypes[ext]

  if (mimeType) {
    const filePath = path.join(__dirname, req.url)
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('File not found')
      } else {
        res.writeHead(200, { 'Content-Type': mimeType })
        res.end(data)
      }
    })
    return
  }

  const logEntry = `[${new Date().toISOString()}] ${ip} - ${userAgent} - AI Agent: ${isAIAgent}\n`
  console.log(logEntry)

  if (req.url === '/api/people/table-page-1') {
    const people = require('./data/tablePage1Data.js')
    res.writeHead(200, { 'Content-Type': 'application/json' })
    res.end(JSON.stringify(people))
    return
  }

  if (req.url === '/api/people/table-page-1-llm') {
    const dataArray = tablePage1Data
    const llmFilePath = path.join(__dirname, 'data', 'tablePage1Data.llm.txt')

    // Generate the llm.txt file from the data array
    generateLLMFile(fs, dataArray, llmFilePath)

    // Serve the generated llm.txt file
    fs.readFile(llmFilePath, 'utf8', (err, data) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'text/plain' })
        res.end('Could not read llm.txt file')
        return
      }
      res.writeHead(200, { 'Content-Type': 'text/plain' })
      res.end(data)
    })
    return
  } else if (req.url === '/llm-preview') {
    const filePath = path.join(__dirname, 'data', 'tablePage1Data.llm.txt')
    fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'text/html' })
        res.end('<h1>Could not read llm.txt file</h1>')
        return
      }
      res.writeHead(200, { 'Content-Type': 'text/html' })
      res.end(`
      <!DOCTYPE html>
      <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <title>LLM File Preview</title>
          <style>
            body { font-family: monospace; background: #f8f8f8; padding: 2em; }
            pre { background: #fff; border: 1px solid #ccc; padding: 1em; overflow-x: auto; }
          </style>
        </head>
        <body>
          <h1>LLM File Preview</h1>
          <pre>${data.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</pre>
        </body>
      </html>
    `)
    })
    return
  }
  if (req.url === '/') {
    res.writeHead(200, { 'Content-Type': 'text/plain' })
    res.end('Welcome to My App')
  } else if (req.url === '/furkan') {
    const filePath = path.join(__dirname, 'pages', 'pageFurkan.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/colin') {
    const filePath = path.join(__dirname, 'pages', 'pageColin.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/Tuberlinlandia') {
    const filePath = path.join(__dirname, 'pages', 'imaginaryCountry.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/table-page-1') {
    const filePath = path.join(__dirname, 'pages/pages-with-table/tablePage1', 'tablePage1.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/table-page-1/with-json-ld') {
    const filePath = path.join(__dirname, 'pages/pages-with-table/tablePage1', 'tablePage1-json-ld.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/table-page-1/with-microdata') {
    const filePath = path.join(__dirname, 'pages/pages-with-table/tablePage1', 'tablePage1-microdata.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/table-page-1/with-json-ld-and-microdata') {
    const filePath = path.join(__dirname, 'pages/pages-with-table/tablePage1', 'tablePage1-json-ld-and-microdata.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/table-page-1-pagination') {
    const filePath = path.join(
      __dirname,
      'pages/pages-with-table/tablePage1WithPagination',
      'tableWithPagination1.html'
    )
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/table-page-1-pagination/with-json-ld') {
    const filePath = path.join(
      __dirname,
      'pages/pages-with-table/tablePage1WithPagination',
      'tableWithPagination1-json-ld.html'
    )
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/table-page-1-pagination/with-microdata') {
    const filePath = path.join(
      __dirname,
      'pages/pages-with-table/tablePage1WithPagination',
      'tableWithPagination1-microdata.html'
    )
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/table-page-1-pagination/with-json-ld-and-microdata') {
    const filePath = path.join(
      __dirname,
      'pages/pages-with-table/tablePage1WithPagination',
      'tableWithPagination1-json-ld-and-microdata.html'
    )
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/inland') {
    const filePath = path.join(__dirname, 'pages', 'inland.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/inland-article-1') {
    const filePath = path.join(__dirname, 'pages', 'inlandArticle1.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/inland-article-2') {
    const filePath = path.join(__dirname, 'pages', 'inlandArticle2.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/inland-article-3') {
    const filePath = path.join(__dirname, 'pages', 'inlandArticle3.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/inland-article-4') {
    const filePath = path.join(__dirname, 'pages', 'inlandArticle4.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/inland-article-5') {
    const filePath = path.join(__dirname, 'pages', 'inlandArticle5.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/inland-jsonld') {
    const filePath = path.join(__dirname, 'pages', 'inlandJSONLD.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/inland-1-jsonld') {
    const filePath = path.join(__dirname, 'pages', 'inlandArticle1JSONLD.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/inland-2-jsonld') {
    const filePath = path.join(__dirname, 'pages', 'inlandArticle2JSONLD.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/inland-3-jsonld') {
    const filePath = path.join(__dirname, 'pages', 'inlandArticle3JSONLD.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/inland-4-jsonld') {
    const filePath = path.join(__dirname, 'pages', 'inlandArticle4JSONLD.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/inland-5-jsonld') {
    const filePath = path.join(__dirname, 'pages', 'inlandArticle5JSONLD.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/Tuberlinlandia-with-microdata') {
    const filePath = path.join(__dirname, 'pages', 'imaginaryCountryMicrodata.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/Tuberlinlandia-with-microdata-and-json-ld') {
    const filePath = path.join(__dirname, 'pages', 'imaginaryCountryJSONLDAndMicrodata.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url === '/Tuberlinlandia-with-json-ld') {
    const filePath = path.join(__dirname, 'pages', 'imaginaryCountryJSONLD.html')
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Page not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.end(data)
      }
    })
  } else if (req.url.startsWith('/css/')) {
    const filePath = path.join(__dirname, 'css', path.basename(req.url))
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('CSS not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'text/css' })
        res.end(data)
      }
    })
  } else if (req.url.startsWith('/images/')) {
    const filePath = path.join(__dirname, req.url)
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Image not found')
      } else {
        res.writeHead(200, { 'Content-Type': 'image/jpeg' })
        res.end(data)
      }
    })
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' })
    res.end('404 Not Found')
  }
})

const PORT = 3000
server.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`)
})
