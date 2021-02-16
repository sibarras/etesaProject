works_1 = {	"Titulo":"Inspecci�n Termogr�fica en Subestaci�n Panam� II",
	"Libranza":"",
	"OT":"1057676",
	"Ubicacion":"Subestaci�n Panam� II",
	"Tipo":"MPD",
	"Clasificacion":"PMA",
	"Cuenta":"1.51121200.0601.430403.430403.0.0000.0.0000",
	"Prioridad":"1",
	"Inicio":"02/15/2021 10:30 AM",
	"Duracion":"4:00",
	"Supervisor":"JBMARTINEZ",
	"Mano de Obra":"['sibarra', 'mperez']",
	"Herramientas":"TERMOGRAFIA",
}

works_2 = {	"Titulo":"Inspecci�n Termogr�fica en Subestaci�n Panam� II",
	"Libranza":"",
	"OT":"1057691",
	"Ubicacion":"Subestaci�n Panam� II",
	"Tipo":"MPD",
	"Clasificacion":"PMA",
	"Cuenta":"1.51121200.0601.430403.430403.0.0000.0.0000",
	"Prioridad":"1",
	"Inicio":"02/15/2021 10:30 AM",
	"Duracion":"4:00",
	"Supervisor":"JBMARTINEZ",
	"Mano de Obra":"['sibarra', 'mperez']",
	"Herramientas":"TERMOGRAFIA",
}

works_3 = {
	"Titulo":"Inspecci�n Termogr�fica en Subestaci�n Panam� II",
	"Libranza":"",
	"OT":"1057768",
	"Ubicacion":"Subestaci�n Panam� II",
	"Tipo":"MPD",
	"Clasificacion":"PMA",
	"Cuenta":"1.51121200.0601.430403.430403.0.0000.0.0000",
	"Prioridad":"1",
	"Inicio":"02/15/2021 10:30 AM",
	"Duracion":"4:00",
	"Supervisor":"JBMARTINEZ",
	"Mano de Obra":"['sibarra', 'mperez']",
	"Herramientas":"TERMOGRAFIA",
}

from datetime import datetime

parse_format = "%Y-%m-%d %H:%M:%S"
maximo_format = "%m/%d/%Y %I:%M %p"

format_hour_str = lambda date, hour_delta: datetime.strptime(date, parse_format)\
                                        .replace(
                                            hour=datetime.strptime(date, parse_format).hour + 
                                            datetime.strptime(hour_delta, "%H:%M").hour
                                        ).strftime(maximo_format)

print(format_hour_str('2021-2-12 6:24:00', '4:00'))