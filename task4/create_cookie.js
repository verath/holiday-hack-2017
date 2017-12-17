let assert = require('assert');
let aes256 = require('./nodejs-aes256.js');

var key = 'need to put any length key in here';
var ciphertext = new Buffer("abcdabcdabcdabcd");
console.log(ciphertext.toString('base64'));
assert(ciphertext.length === 16);
var plaintext = aes256.decrypt(key, ciphertext);
assert(plaintext === "");
