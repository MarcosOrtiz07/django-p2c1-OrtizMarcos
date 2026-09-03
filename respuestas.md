7. Verificación individual escrita 
Responda después del cierre técnico. Puede revisar el código entregado, pero no modificarlo. 
Pregunta 1 
Explique el recorrido de una solicitud desde /resumen-zonas/ hasta la respuesta HTML. Mencione la 
URL, la View, el contexto y el Template. 

se crea el path "path("resumen/", views.resumen_zona, name="resumen_zonas")," y luego en view se crea una def que valide los datos y en el template "resumen" se conecta con la def y asi mostrarlo en la pantalla



Pregunta 2 
Indique el archivo y la parte de su código donde cuenta dispositivos y suma consumo_kwh por zona. 
Explique brevemente cómo funciona. 


 # Evaluar estado de la zona (CA-05)
    limite = float(zona_actual.get('limite_kwh', 0))
    if consumo_total > limite:
        estado = "ALERTA"
    else:
        estado = "NORMAL"
        
en caso de que consumo_total sea > que el limite de kwh tira alerta, y en caso de que esta dentro del limite lo deja normal

Pregunta 3 
Indique la condición utilizada para definir el estado de una zona y explique qué ocurre cuando una zona 
no tiene dispositivos. 

Con una condicion llamada zona_actual que revisa la id de la zona en el json junto con un control de error que redirige a 404 en caso de zona inexistente


Cuando no hay una zona con una id que concuerde lanzara el error 404 indicando "Lo sentimos, el identificador de la zona solicitada no existe o no se encuentra registrado en el sistema."