import requests
import datetime 
import hashlib
import base64
import time
from utils import *


class NestPay():

    def __init__(self,**kwargs):
        self.__dict__.update(**kwargs)
        super().__init__()

    def bank_data(self, *args, **kwargs):
        convert = self.__dict__
        string = convert['clientId'] + convert['oid'] + convert['amount'] + convert['okUrl'] + convert['failUrl'] + convert['islemtipi'] + convert['instalment'] + str(convert['rnd']) + convert['storekey']
        string_to_hash = convert_string_to_hash(string).decode()
        convert['hash']= string_to_hash
        return self.data_send(**convert)

    def data_send(self, *args, **kwargs):
        url = '{0}'.format(kwargs['post_url'])
        del kwargs['post_url']
        post = requests.post(url, data=kwargs)
        return post.content


    def data_result(self,**kwargs):
        storekey = self.__dict__['storekey']
        hashparams = kwargs['HASHPARAMS']
        hashparamsval = kwargs['HASHPARAMSVAL']
        hashparam = kwargs['HASH']
        paramsval = ''
        index1 = 0
        index2 = 0
        while index1< len(hashparams):
            index2 = hashparams.find(':', index1)
            s = substr(hashparams,index1,index2-index1)
            vl = kwargs.get(f'{s}')
            paramsval = paramsval + vl
            index1 = index2 + 1
        hashval = paramsval + storekey
        hashcon = convert_string_to_hash(hashval).decode()
        if hashparams != None:
            if paramsval != hashparamsval or hashparam != hashcon:
                return 'Security warning. Hash values mismatch'
            else:
                mdStatus = kwargs['mdStatus']
                if mdStatus == "1" or mdStatus == "2" or mdStatus == "3" or mdStatus == "4":
                    return '3D Authentication is successful.'
                else:
                    return '3D authentication unsuccesful.'
        else:
            return 'Hash values error. Please check parameters posted to 3D secure page.'
        
        
temp = NestPay(
    clientId = '', # bank terefinden verilir
    amount = '', # mebleg : 1.00 azn
    oid = '', # order id unikdi
    okUrl = '', # callback url success den sonra bura post gonderilir
    failUrl = '', # error url 
    rnd = microtime(),
    storekey = '2', # bank terefinden verilir
    storetype = '', # bank terefinden verilir
    lang = 'en', # hansi dilde odeme sehvesine redirec edecek
    islemtipi = 'Auth', # default 
    hash = '', # hash edirik
    refreshtime = '5', # sehveler arasinda redirect timeout u
    instalment='', # taksid
    currency = '944', # Azerbaycan manatinin kodu
    post_url = 'https://entegrasyon.asseco-see.com.tr/fim/est3Dgate'
    )
data = temp.bank_data()
print(data)


