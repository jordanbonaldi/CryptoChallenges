#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import sys
import codecs
import base64
from Crypto.Cipher import AES
from urlparse import parse_qs

g_key = "--CRYPTOGRAPHY--"

def encrypt_AES(msg):
    decipher = AES.new(g_key, AES.MODE_ECB)
    return decipher.encrypt(msg)

def decrypt_AES(msg):
    decipher = AES.new(g_key, AES.MODE_ECB)
    return decipher.decrypt(msg)

def pad_block_pkcs7(data, length):
    if (len(data) >= length):
        return data
    pad = (length - len(data))
    barray = bytearray(data, 'utf-8')
    for i in range(pad):
        barray.append(pad)
    return barray

def is_unpad_necessary(data):
    char = data[-1]
    i = 0
    print(type(char))
    for n in range(len(data) - 1, len(data) - ord(char) - 1, -1):
        if data[n] == char:
            i += 1
    if i == ord(char):
        return True
    else:
        return False

def unpad_block_pkcs7(data):
    if is_unpad_necessary(data) == False:
        return data
    pad = ord(data[-1])
    data = data[:-pad]
    return data

def check_valid(data):
    print(len(data))
    print(data)
    data_base10 = codecs.decode(data, 'base64')
    print(len(data_base10))
    res = decrypt_AES(bytes(data_base10))
    print("---VALID")
    print(res)
    res = unpad_block_pkcs7(res)
    print(res)
    res = res[-5:]
    print(res)
    print("---VALID")
    if ("admin" == res):
        return "Bravo"
    else:
        return "Bolosse"

def create_profile(data):
    data_base10 = codecs.decode(data, 'base64')
    data_base10 = data_base10.replace('&', '')
    data_base10 = data_base10.replace('=', '')
    data_base10 = "email=" + data_base10 + "&uid=10&role=user"
    print("---PROFILE")
    print(data_base10)
    tmp = len(data_base10) + (len(g_key) - (len(data_base10) % len(g_key)))
    data_base10 = pad_block_pkcs7(data_base10, tmp)
    print(data_base10)
    res = encrypt_AES(bytes(data_base10))
    print(res)
    res = codecs.encode(res, 'base64')
    print(res)
    print("---PROFILE")
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

        path = self.path[13:21]
        print (path)
        if (path == "validate"):
            data = check_valid(post_data)
        else:
            data = create_profile(post_data)
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
