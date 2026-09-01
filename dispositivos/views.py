import json
import os
from django.conf import settings
from django.http import Http404
from django.shortcuts import render

def cargar_json(nombre_archivo):
    ruta = os.path.join(settings.BASE_DIR, 'data', nombre_archivo)
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def zonas_list(request):
    """
    Vista Listado de Zonas (Punto 5 / CA-01, CA-02).
    Historia de Usuario: "Como encargado del monitoreo energético de EcoEnergy, quiero consultar 
    las zonas de consumo y revisar el detalle de sus dispositivos..."
    
    Lee los JSON y calcula dinámicamente la cantidad de dispositivos por zona.
    """
    zonas = cargar_json('zonas.json')
    dispositivos = cargar_json('dispositivos.json')
    
    # Contar dispositivos por zona
    for zona in zonas:
        zona['total_dispositivos'] = 0
        for disp in dispositivos:
            if disp.get('zona_id') == zona['id']:
                zona['total_dispositivos'] += 1
                
    contexto = {
        'zonas': zonas
    }
    return render(request, 'zonas_list.html', contexto)

def zona_detail(request, id):
    """
    Vista Detalle de Zona (Punto 5 / CA-03, CA-04, CA-05, CA-08).
    Cumple con el objetivo de "identificar su consumo total y reconocer oportunamente 
    estados normales, alertas o ausencia de información".
    """
    zonas = cargar_json('zonas.json')
    dispositivos = cargar_json('dispositivos.json')
    categorias = cargar_json('categorias.json')
    
    # Buscar la zona por ID
    zona_actual = None
    for z in zonas:
        if z['id'] == id:
            zona_actual = z
            break
            
    # CA-08: Manejo de 404 para zonas inexistentes
    if not zona_actual:
        raise Http404("Zona no encontrada")
        
    # Filtrar dispositivos y calcular consumo
    disp_zona = []
    consumo_total = 0.0
    
    for disp in dispositivos:
        if disp.get('zona_id') == id:
            # Obtener nombre de la categoría
            nombre_cat = "Desconocida"
            for c in categorias:
                if c['id'] == disp.get('categoria_id'):
                    nombre_cat = c['nombre']
                    break
            
            disp['categoria_nombre'] = nombre_cat
            disp_zona.append(disp)
            consumo_total += float(disp.get('consumo_kwh', 0))
            
    # Evaluar estado de la zona (CA-05)
    limite = float(zona_actual.get('limite_kwh', 0))
    if consumo_total > limite:
        estado = "ALERTA"
    else:
        estado = "NORMAL"
        
    contexto = {
        'zona': zona_actual,
        'dispositivos': disp_zona,
        'consumo_total': consumo_total,
        'cantidad_dispositivos': len(disp_zona),
        'estado': estado
    }
    return render(request, 'zona_detail.html', contexto)
def inicio(request):
    contexto = {
        "sistema": "EcoEnergy",
        "mensaje": "Monitoreo energético responsable",
        "asignatura": "Programación Back End",
    }
    return render(request, "dispositivos/inicio.html", contexto)

def dispositivos_list(request):
    dispositivos = cargar_json('dispositivos.json')
    zonas = cargar_json('zonas.json')
    categorias = cargar_json('categorias.json')

    for disp in dispositivos:
        # Asignar nombre de zona
        disp['zona_nombre'] = "Desconocida"
        for z in zonas:
            if z['id'] == disp.get('zona_id'):
                disp['zona_nombre'] = z['nombre']
                break
        
        # Asignar nombre de categoria
        disp['categoria_nombre'] = "Desconocida"
        for c in categorias:
            if c['id'] == disp.get('categoria_id'):
                disp['categoria_nombre'] = c['nombre']
                break

    contexto = {
        'dispositivos': dispositivos
    }
    return render(request, 'dispositivos_list.html', contexto)
