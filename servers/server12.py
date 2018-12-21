#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import sys
import codecs
import base64
from Crypto.Cipher import AES

g_key = "--CRYPTOGRAPHY--"

g_unknow = "CURVECURVECURVECURVE"

g_prefix = "BITE123456789"

def encrypt_AES(key, msg):
    decipher = AES.new(g_key, AES.MODE_ECB)
    return decipher.encrypt(msg)

def pad_block_pkcs7(data, length):
    if (len(data) >= length):
        return data
    pad = (length - len(data))
    barray = bytearray(data, 'utf-8')
    for i in range(pad):
        barray.append(pad)
    return barray

def exo10(data):
    data_base10 = g_prefix + codecs.decode(data, 'base64')
    data_base10 += g_unknow
    print(data_base10)
    tmp = len(data_base10) + (len(g_key) - (len(data_base10) % len(g_key)))
    data_base10 = pad_block_pkcs7(data_base10, tmp)
    res = encrypt_AES("", bytes(data_base10))
    print(len(res))
    res = codecs.encode(res, 'base64')
    return res

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

        data = exo10(post_data)
        print("--")
        print(data)
        print("--")
        self.wfile.write(data)

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
