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
        f = {"x": "47", "y": "15", "md": "510307:BC271C5FA4D3F0C4EC50B217893C230333AC1699CAC73F87F0BCA9A4601971C2:4099:##200008963", "eci": "01", "oid": "449", "rnd": "ig0pJpb95SIj7dvLEjIK", "sID": "2", "xid": "aG1WoscYXERqkoomHw0QjjslIvc=", "HASH": "TgyHvoU1e2Q4JmQURtkIaHD5bvY=", "cavv": "hoHq93Mh0GlkYwAKqKNABiUAAAA=", "dsId": "2", "lang": "tr", "okUrl": "https://api.fryday.az/ru/v1/callback/", "ACQBIN": "536238", "ErrMsg": "", "TRANID": "", "amount": "1.00", "digest": "digest", "taksit": "", "TransId": "20352RLhE00104440", "acqStan": "000011", "failUrl": "https://beta.fryday.az/order-error", "version": "4.0", "AuthCode": "334081", "Response": "Approved", "SettleId": "23", "clientIp": "213.172.90.90", "clientid": "200008963", "currency": "944", "encoding": "UTF-8", "iReqCode": "", "mdStatus": "4", "protocol": "3DS1.0.2", "MaskedPan": "510307***5094", "ReturnOid": "449", "_charset_": "UTF-8", "countdown": "1", "islemtipi": "Auth", "signature": "P3WyCc/Ag79m29tCbUjItcrjFR1bBAsdDqxu2Nx8aNpMaBGNK6Yc3JrNffP93fvzYAz8pTDAulxyBCixB9PhAN+8ihfmIvLnsEH1lXIqBzSyzbJsBfgEPtLt5fze01oZEz48PS6vaLlb0YOvJs7QzR0V/WrDn/YuC0RmV/TGOO94tr2uWP/Tw//HhtFpxuQE2Vcs+a5tuej0tS7hwGI65P93BYZviMUsD8HJ86Jn+p+VE9f4t/DUCGvji93Na0JglFfTK4vAtP6zDYla4LqOLhuem32xtVNYd7prT3EcPL4OUKzyB6SfECrrlyxCwdRqnhZkkLQnmaMKxKeCveJccQ==", "storetype": "3d_pay_hosting", "HASHPARAMS": "clientid:oid:AuthCode:ProcReturnCode:Response:mdStatus:cavv:eci:md:rnd:", "HostRefNum": "035218620607", "iReqDetail": "", "mdErrorMsg": "Valid authentication attempt", "merchantID": "200008963", "vendorCode": "", "refreshtime": "5", "callbackCall": "true", "EXTRA.HOSTMSG": "0000000 Basarili.", "EXTRA.TRXDATE": "20201217 17:11:33", "HASHPARAMSVAL": "20000896344933408100Approved4hoHq93Mh0GlkYwAKqKNABiUAAAA=01510307:BC271C5FA4D3F0C4EC50B217893C230333AC1699CAC73F87F0BCA9A4601971C2:4099:##200008963ig0pJpb95SIj7dvLEjIK", "PAResSyntaxOK": "true", "PAResVerified": "false", "cavvAlgorithm": "3", "paresTxStatus": "A", "ProcReturnCode": "00", "EXTRA.CARDBRAND": "MASTERCARD", "payResults.dsId": "2", "EXTRA.CARDISSUER": "Yap\u0131 Kredi Bank Azerbaijan CSJC", "maskedCreditCard": "5103 07** **** 5094", "veresEnrolledStatus": "Y", "Ecom_Payment_Card_ExpDate_Year": "23", "Ecom_Payment_Card_ExpDate_Month": "08"}
        m = self.data_result(**f) 
        print(m)       
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


