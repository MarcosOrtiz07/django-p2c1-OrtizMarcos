from django.http import HttpResponse
from django.shortcuts import render

# Asegúrate de importar la función si la tienes en utils.py/helpers.py,
# o defínela arriba de las vistas si la tienes en este mismo archivo.
from .utils import cargar_dispositivos


def inicio(request):
    contexto = {
        "sistema": "EcoEnergy",
        "mensaje": "Monitoreo energético responsable",
        "asignatura": "Programación Back End",
    }
    return render(request, "dispositivos/inicio.html", contexto)


def dispositivos_zona(request, zona_id):
    if zona_id != 3:
        return HttpResponse("Zona no encontrada", status=404)

    return HttpResponse(f"Dispositivos de la zona {zona_id}")


def catalogo(request):
    dispositivos = cargar_dispositivos()
    activos = sum(1 for item in dispositivos if item["estado"] == "Activo")

    contexto = {
        "dispositivos": dispositivos,
        "total": len(dispositivos),
        "total_activos": activos,
    }

    return render(request, "dispositivos/catalogo.html", contexto)