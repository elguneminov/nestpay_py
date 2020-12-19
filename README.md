# nestpay odeme sistemi ucun modul





```python




from nestpay import NestPay
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt




def payment(request):
    ......
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
        post_url = 'https://entegrasyon.asseco-see.com.tr/fim/est3Dgate' # odeme sehivesi
        )
    data = temp.bank_data()
    return HttpResponse(data)

# callback yuxarda paymentde qeyd edeceyimiz okUrl di ve o url e bank post gonderir
@csrf_exempt
def callback(request):
    ........
    if request.method == 'POST':
        result = Nestpay.data_result(request.POST)
        return HttpResponse(result)
    else:
        return HttpResponse("Not found")


````
