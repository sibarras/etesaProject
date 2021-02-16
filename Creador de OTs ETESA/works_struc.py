class PMAWork2:
    def __init__(self,   
            titulo:str,
            libranza:str,
            ot:str,
            ubiacion:str,
            tipo:str,
            clasificacion:str,
            cuenta:str,
            prioridad:str,
            inicio:str,
            duracion:str,
            supervisor:str,
            mano_de_obra:list,
            herramientas:str
        ) -> None:

        self.titulo:str = titulo
        self.libranza:str = libranza
        self.ot:str = ot
        self.ubiacion:str = ubiacion
        self.tipo:str = tipo
        self.clasificacion:str = clasificacion
        self.cuenta:str = cuenta
        self.prioridad:str = prioridad
        self.inicio:str = inicio
        self.duracion:str = duracion
        self.supervisor:str = supervisor
        self.mano_de_obra:list = mano_de_obra
        self.herramientas:str = herramientas

class PMAWork:
    titulo:str
    libranza:str
    ot:str
    ubiacion:str
    tipo:str
    clasificacion:str
    cuenta:str
    prioridad:str
    inicio:str
    duracion:str
    supervisor:str
    mano_de_obra:list = []
    herramientas:str

    def __repr__(self) -> str:
        return f'{self.titulo} en la fecha {self.inicio}'



if __name__ == '__main__':
    work2 = PMAWork2()
    work3 = PMAWork2()
    work2.clasificacion = '4'
    work3.clasificacion = '8'
    print(work2.clasificacion, work2.mano_de_obra)
    print(work3.clasificacion, work3.mano_de_obra)
