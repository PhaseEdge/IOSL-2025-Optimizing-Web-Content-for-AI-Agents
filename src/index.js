const http = require('http')
const fs = require('fs')
const path = require('path')
const isBot = require('./functions/BotDetectionByHeader')
const hasSuspiciousHeaders = require('./functions/BotDetectionByMissingInfo')

const server = http.createServer((req, res) => {
  console.log(req.url, 'reql*****')
  // detect AI Agent and log
  console.log('Headers:', req.headers)
  const userAgent = req.headers['user-agent'] || 'Unknown'
  const ip = req.socket.remoteAddress || 'Unknown IP'
  const isAIAgent = isBot(userAgent)

  if (isAIAgent || hasSuspiciousHeaders(req.headers)) {
    res.writeHead(302, { Location: '/api/people/table-page-1' })
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
    const peopleTxtPath = path.join(__dirname, 'pages/pages-with-table/tablePage1/tablePage.llm.txt')
    fs.readFile(peopleTxtPath, 'utf8', (err, data) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'application/json' })
        res.end(JSON.stringify({ error: 'Could not read data file' }))
        return
      }
      // Parse the file into objects
      const people = []
      const records = data
        .split('---')
        .map(r => r.trim())
        .filter(Boolean)
      for (const record of records) {
        const obj = {}
        record.split('\n').forEach(line => {
          const [key, ...rest] = line.split(':')
          if (key && rest.length) {
            const value = rest.join(':').trim()
            switch (key.trim()) {
              case 'ID':
                obj.id = Number(value)
                break
              case 'First Name':
                obj.first_name = value
                break
              case 'Last Name':
                obj.last_name = value
                break
              case 'Email':
                obj.email = value
                break
              case 'Gender':
                obj.gender = value
                break
              case 'IP Address':
                obj.ip_address = value
                break
            }
          }
        })
        if (Object.keys(obj).length) people.push(obj)
      }
      res.writeHead(200, { 'Content-Type': 'application/json' })
      res.end(JSON.stringify(people))
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
