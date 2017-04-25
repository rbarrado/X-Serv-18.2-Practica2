from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from practica2.models import URLs
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def showAll():
    list = URLs.objects.all()
    if len(list) != 0:
        respuesta = ""
        list_URLs = URLs.objects.all()
        for url in list_URLs:
            respuesta += "<h4><li>URL sin acortar: " + url.larga + " | URL acortada: " + str(url.id) + "</li></h4>"
        respuesta = "<div><h3>DATA BASE</h3><ul>" + respuesta + "</ul></div>"
    else :
        respuesta = "<h3>Data base is empty.</h3>"
    return respuesta

def showByID(request,identificador):
    try:
        url = URLs.objects.get(id=int(identificador))
        return HttpResponseRedirect(url.larga)
    except URLs.DoesNotExist:
        respuesta = "<html><body>Recurso no disponible</html></body>"
        return HttpResponse(respuesta, status=404)

@csrf_exempt
def processBarra(request):
    if request.method == "GET":
            respuesta = '<div><form action="" method="POST">'
            respuesta += 'URL a acortar: <input type="text" name="url">'
            respuesta += '<input type="submit" value="Enviar"></form></div>'
            respuesta = respuesta + showAll()

    elif request.method == "POST":
        larga = request.POST['url']
        if (larga[0:8] != "https://") and (larga[0:7] != "http://"):
            larga = "http://" + larga
        if (larga[0:8] == "https://"):
            larga = "http://" + larga[8:]
        respuesta = ""
        try:
            url = URLs.objects.get(larga=larga)
            print(larga)
            respuesta += "<div><p>URL SIN ACORTAR: <a href=" + url.larga + ">" + url.larga + "</a></p>"
            respuesta += "<p>URL ACORTADA: <a href=" + "'http://localhost:1234/" + str(url.id) \
                        + "'>" + str(url.id) + "</a></p></div>"

        except URLs.DoesNotExist:
            url = URLs(larga=larga)
            url.save()
            respuesta += "<p>URL SIN ACORTAR: <a href=" + larga + ">" + larga + "</a></p>"
            respuesta += "<p>URL ACORTADA: <a href=" + "'http://localhost:1234/" + str(url.id) \
                        + "'>" + str(url.id) + "</a></p>"

    else :
        respuesta = "Method not Allowed"

    respuesta = "<html><body>" + respuesta + "</body></html>"
return HttpResponse(respuesta)
