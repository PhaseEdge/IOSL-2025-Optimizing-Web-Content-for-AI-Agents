function generateLLMFile(fs, dataArray, filePath) {
  const content = dataArray
    .map(person => {
      return `ID: ${person.id}
First Name: ${person.first_name}
Last Name: ${person.last_name}
Email: ${person.email}
Gender: ${person.gender}
IP Address: ${person.ip_address}
---`
    })
    .join('\n')

  fs.writeFileSync(filePath, content, 'utf8')
  console.log(`✅ llm.txt written to ${filePath}`)
}
module.exports = generateLLMFile
