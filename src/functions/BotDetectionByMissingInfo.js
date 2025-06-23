const missingHeaders = ['sec-fetch-mode', 'sec-fetch-site', 'sec-ch-ua']

const hasSuspiciousHeaders = headers => {
  return missingHeaders.some(header => !(header in headers))
}

module.exports = hasSuspiciousHeaders
