# para retornar un entero si el flotante esta en 2.00 o sus decimales que se pasen
def redondear(numero, decimales=2):
    if int(numero) == numero:
        return int(numero)
    else:
        return round(numero, decimales)
    
import pytz

# para que se ejecute solo cuando django lo requiera, se lo paso como parametro
def timezone_now_cre(fecha,zona):
  # Define la zona horaria a la que deseas convertir la fecha
  nueva_zona_horaria = pytz.timezone(zona)

  # Convierte la fecha y hora a la nueva zona horaria
  fecha_hora_nueva = fecha.astimezone(nueva_zona_horaria)
  return fecha_hora_nueva