from django.utils import simplejson
def myexample(request):
    return simplejson.dumps({'message':'Hello World'})