#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import sys
import codecs
import base64
from Crypto.Cipher import AES
from urlparse import parse_qs
from Crypto import Random


g_key = "--CRYPTOGRAPHY--"
g_iv =  "1234567890123456"
g_ciphertext = "salut je m'appelle jordy"

def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

def unpad(s):
    t = s.encode("hex")
    exe = re.findall('..',t)
    padding = int(exe[-1], 16)
    exe = exe[::-1]

    if padding == 0 or padding > 16:
        return 0

    for i in range(padding):
        if int(exe[i],16) != padding:
            return 0
    return s[:-ord(s[len(s)-1:])]

def encrypt( msg, iv):
    raw = pad(msg)
    key = Random.new().read(AES.block_size)
    cipher = AES.new('V38lKILOJmtpQMHp', AES.MODE_CBC, iv)
    return cipher.encrypt(raw), iv

def decrypt(enc, iv):
    decipher = AES.new('V38lKILOJmtpQMHp', AES.MODE_CBC, iv)
    return unpad(decipher.decrypt(enc))

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Set-Cookie', 'caca lol mdr')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._set_headers()

        post_data = post_data.split('\n')
        cipher = post_data[0]
        iv = post_data[1]
        data = decrypt(cipher, iv)
        self.wfile.write(data)

    def do_GET(self):
        self._set_headers()
        data, iv = encrypt(g_ciphertext, g_iv)
        data = codecs.encode(data, 'base64')
        iv = codecs.encode(iv, 'base64')
        self.wfile.write(data + iv)

def run(server_class=HTTPServer, handler_class=S, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
