import pandas as pd

# para escribir en una sheet de excel necesitas dividir cada informacion

# Defines la quincena que estas trabajando, esta puede ser elegida de una lista

# Defines si estas en la primera o la segunda quincena. El programa debe tener conocimiento
# de los dias posibles a elegir y mostrar un error si estos dias son incorrectos.

# Defines las horas extras con una descripcion inicial. Esta puede ser tomada de un menu de pruebas

# Se debe colocar el lugar de la prueba. Esto es muy importante ya que es necesario para poder llenar
# el lugar de las horas de trabajo. El codigo de las horas debe estar interna en el programa.

# Las horas extras deben decir el dia de esta hora extra. Solo se debe colocar el numero

# Debes colocar la hora de salida de la hora extra en caso tal que sea en la semana, o la hora de inicio
# en caso tal sea antes de las 7:00 am.
# En dias dabados y domingos se debe indicar la hora de inicio y final.

# Se deben colocar los dias por compensatorio o los dias que fueron festivos. Los dias no laborados
# Al final de todo, debe llenarse los dias de trabajo en subestacion (automaticamente), y el porcentaje
# debe ser menor a 30% en oficina. Debe generar los espacios faltantes para poder lograr este porcentaje.

# defino funciones que simularan las peticiones a realizar
equipmentTests = {
    'PT': [tests[i] for i in []],
    'CT': '',
    'INT': '',
    'TX': '',
    'RX': ''
}

tests = [
    'Tiempos de Operacion',         #0
    'Resistencia de Contacto',      #1
    'Resistencia de Aislamiento',   #2
    'Resistencia de Devanados',     #3
    'Realcion de Vueltas',          #4
    'Factor de Potencia',           #5
    'Analisis de Gas SF6',          #6
    'Alarmas y Disparos',           #7
    'Analis de Calidad de Energia', #8
    'Corriente de Excitacion',      #9
    'Saturacion'                    #10
]




define addWork(description=str, place=str, day=str, starthour=str, endhour=str):
    pass

define freeDay(reason=str, day=str):
    pass

def main:
    pass


if __name__ == "__main__":
    main()
