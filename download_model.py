import requests
import zipfile
import os

url = 'https://doc-08-7s-docs.googleusercontent.com/docs/securesc/mt0m7fil7lh4smitnbl25ak20aogkqet/i87u1ms0nh1104uqiu3hkj9g217f0d4n/1521129600000/18056234690049221457/13071359278190364897/0B5MzpY9kBtDVOTVnU3NIaUdySFE?e=download'
cookie = 'AUTH_1rvq7ppeitcidnqg38vbgeuk7di2i80q=13071359278190364897|1521122400000|5vdlq2fa307kdmvubdfgot2ibi2gvu2t; NID=123=idYj-LOBoUwhSM4-ICUGAhRpOmw9vKWdc0vnnTyHdG3yWLRBWLE-d6sbF9EVMSswcDB1tk6L5UoKCCnEo_tbKHTJaUWLonKy1UYaRpFaXr1zmUb2yvndUJvVNVlBj7e1'
headers = {'Cookie':cookie}

r = requests.get(url, headers=headers)

def save(r, filename):
	with open(filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=2**20):
			f.write(chunk)

save(r, '20170511-185253.zip')

zip_ref = zipfile.ZipFile('20170511-185253.zip', 'r')
zip_ref.extractall('./')
zip_ref.close()

os.remove('20170511-185253.zip')