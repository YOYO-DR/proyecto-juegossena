import pytz

# para que se ejecute solo cuando django lo requiera, se lo paso como parametro
def timezone_now_cre(fecha,zona):
  # Define la zona horaria a la que deseas convertir la fecha
  nueva_zona_horaria = pytz.timezone(zona)

  # Convierte la fecha y hora a la nueva zona horaria
  fecha_hora_nueva = fecha.astimezone(nueva_zona_horaria)
  return fecha_hora_nueva