from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from app.models import *
import uuid
import datetime

def decryptmailid(key1):
	nonce=''
	tag=''
	key=''
	ciphertext=''
	obj=MailData.objects.filter(key1=key1)
	for x in obj:
		nonce=x.nonce
		tag=x.tag
		key=x.key
		ciphertext=x.ciphertext
	cipher = AES.new(key, AES.MODE_EAX, nonce)
	data = cipher.decrypt_and_verify(ciphertext, tag)
	response = ""
	for x in str(data):
		if not x == "'":
			response=response+x
	response2 = ""
	for x in str(response):
		if not x == "b":
			response2=response2+x
	return response2

def encryptmailid(mailid):
	key = get_random_bytes(16)
	cipher = AES.new(key, AES.MODE_EAX)
	ciphertext, tag = cipher.encrypt_and_digest(str.encode(mailid))
	obj=MailData.objects.filter(Mail_ID=mailid)
	key1=uuid.uuid5(uuid.NAMESPACE_DNS, str(datetime.datetime.today())+mailid)
	obj.update(key=key, key1=key1, nonce=cipher.nonce, tag=tag, ciphertext=ciphertext)
	return key1