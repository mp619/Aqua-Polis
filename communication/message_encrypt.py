import rsa
import os

public_key, private_key = rsa.newkeys(1024)

print(public_key)
print(private_key)

public = public_key.save_pkcs1().decode('utf-8')
private = private_key.save_pkcs1().decode('utf-8')

print(public)
print(private)

file1 = open('public_pem1', 'w')
file1.write(repr(public))
file1.close()

file2 = open('private_pem1', 'w')
file2.write(repr(private))
file2.close()