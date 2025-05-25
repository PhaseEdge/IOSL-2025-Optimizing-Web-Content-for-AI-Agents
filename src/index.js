const http = require('http')
const fs = require('fs')
const path = require('path')
const isBot = require('./functions/BotDetectionByHeader')

const server = http.createServer((req, res) => {
  const userAgent = req.headers['user-agent'] || ''

  if (isBot(userAgent) || hasSuspiciousHeaders(req.headers)) {
    res.writeHead(302, { Location: '/furkan' })
    res.end()
    return
  }

  /* 

  // client-side POST check via JavaScript
  <scrpit>
    fetch('/check-post', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ test: 'test' })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error))
    </script>
  */

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
