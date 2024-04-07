from enum import Enum
from abc import ABCMeta, abstractmethod
class NotFound(Exception):
    pass

class Repeated(Exception):
    pass
class Persona:
    def __init__(self, nombre, DNI, direccion, sexo):
        assert len(DNI) == 9, 'Formato de DNI incorrecto.'
        assert sexo in {'M', 'F'}, 'Opción inválida. Opciones válidas para sexo: M / F'
        self.nombre = nombre
        self.DNI = DNI
        self.direccion = direccion
        self.sexo = sexo

class Miembro_departamento:
    def __init__(self, departamento):
        self.departamento = departamento
    
    def cambiar_dep(self, dep):
        self.departamento = dep


class Departamento(Enum):
    DIIC = 1
    DITEC = 2
    DIS = 3
    
class Asignatura: 
    def __init__(self, nombre, creditos): 
        self.nombre = nombre
        self.creditos = creditos
        self.estudiantes = []
        self.profesores = []
    
    def add_estudiante(self, estudiante):
        self.estudiantes.append(estudiante)
    
    def add_profesor(self, profesor):
        self.profesores.append(profesor)
    
    def del_estudiante(self, estudiante):
        self.estudiantes.remove(estudiante)

    def del_profesor(self, profesor):
        self.profesores.remove(profesor)

    def lista_estudiantes(self):
        print("Para la asignatura de", self.nombre, "se tienen los siguientes estudiantes: ")
        for estudiante in self.estudiantes:
            print(estudiante)
    
    def __str__(self):
        cadena = f'Asignatura: {self.nombre}\nCréditos: {self.creditos}\nNº estudiantes: {len(self.estudiantes)}\nProfesores: '
        if not self.profesores:
            cadena += "No hay ningún profesor a cargo de esta asignatura aún."
        else:
            cadena += ', '.join(profesor.nombre for profesor in self.profesores)
        cadena += "\n"
        return cadena
    



class Investigador(Persona):
    def __init__(self, nombre, DNI, direccion, sexo, area, departamento):
        super().__init__(nombre, DNI, direccion, sexo)
        self.area = area
        self.miembro  = Miembro_departamento(departamento) # Composición.


class ProfesorTitular(Persona):
    def __init__(self, nombre, DNI, direccion, sexo, area_inv, departamento, listaAsig = []):
        super().__init__(nombre, DNI, direccion, sexo)
        self.listaAsig = listaAsig
        self.rol_inv = Investigador(nombre, DNI ,direccion , sexo, area_inv, departamento)
        self.miembro  = Miembro_departamento(departamento)

    def add_asig(self,asig): # se implementará en la clase Universidad porque ahí estará la lista de asignaturas
        self.listaAsig.append(asig)

    def del_asig(self, asig):
        self.listaAsig.remove(asig)
        
    def mostrar_asig(self):
        print(f"El profesor imparte las siguientes asignaturas")
        for i in self.listaAsig:
            print(i.devuelve_datos())
            
class ProfesorAsociado(Persona):
    def __init__(self, nombre, DNI, direccion, sexo, departamento, listaAsig = []):
        super().__init__(nombre, DNI, direccion, sexo)
        self.listaAsig = listaAsig
        self.miembro  = Miembro_departamento(departamento)

    def add_asig(self,asig):
        self.listaAsig.append(asig) # se mete el nombre de la asignatura
    
    def del_asig(self, asig):
        self.listaAsig.remove(asig)

    def devuelve_datos(self):
        return "Profesor asociadio \t"+"Nombre: "+self.nombre+" DNI: "+self.dni+" Direccion: "+self.direccion+" Sexo: "+self.sexo+" Departamento :"+self.departamento

    def mostar_asig(self):
        print(f"El profesor imparte las siguientes asignaturas")
        for i in self.asignaturas:
            print(i.devuelve_datos())

class Estudiante(Persona):
    def __init__(self, nombre, DNI, direccion, sexo, listaAsig=None):
        super().__init__(nombre, DNI, direccion, sexo)
        self.listaAsig = listaAsig if listaAsig is not None else []

    def add_asig(self, asig):
        self.listaAsig.append(asig)

    def del_asig(self, asig):
        self.listaAsig.remove(asig)

    def devuelve_datos(self):
        return f"Estudiante \tNombre: {self.nombre}, DNI: {self.DNI}, Dirección: {self.direccion}, Sexo: {self.sexo}"

    def mostrar_asig(self):
        print("El estudiante está matriculado de las siguientes asignaturas:")
        for asignatura in self.listaAsig:
            print(asignatura)

    def __str__(self):
        return self.devuelve_datos()

class Universidad:
    def __init__(self, nombre, codpostal, ciudad, lista_inves=None, lista_prof_tit=None, lista_prof_asoc=None,
                 lista_est=None, lista_asig=None):
        self.nombre = nombre
        self.codpostal = codpostal
        self.ciudad = ciudad
        self._lista_inves = lista_inves if lista_inves is not None else []
        self._lista_prof_tit = lista_prof_tit if lista_prof_tit is not None else []
        self._lista_prof_asoc = lista_prof_asoc if lista_prof_asoc is not None else []
        self._lista_est = lista_est if lista_est is not None else []
        self._lista_asig = lista_asig if lista_asig is not None else []

    # se va a diferenciar a la hora de asignar asignaturas a profesores entre su rol. --- nos ahorramos recorrer dos listas.
    # vale la pena?    
    
    def _buscaasig(self, nombre):
        for asig in self._lista_asig:
            if asig.nombre == nombre:
                return asig
        raise NotFound('Error. Esta asignatura no existe.')
        
    def _buscaprofAsoc(self, profesor):
        for prof in self._lista_prof_asoc:
            if prof.nombre == profesor:
                return prof
        return None

                
    def _buscaprofTitular(self, profesor):
        for prof in self._lista_prof_tit:
            if prof.nombre == profesor:
                return prof
        return None

    def _buscaestud(self, estudiante):
        for est in self._lista_est:
            if est.nombre == estudiante:
                return est
        raise NotFound('Error. Este estudiante no existe.')

    def _buscainvest(self, investigador):
        for invest in self._lista_inves:
            if invest.nombre == investigador:
                return invest
        return None

    
    def add_estudiante(self,nombre,DNI,direccion,sexo):
        est = Estudiante(nombre,DNI,direccion,sexo)
        self._lista_est.append(est)
    
    def add_prof_titular(self,nombre,DNI,direccion,sexo,area_inv,departamento):
        prof_tit = ProfesorTitular(nombre,DNI,direccion,sexo,area_inv,departamento)
        self._lista_prof_tit.append(prof_tit)
        self._lista_inves.append(prof_tit) # el profesor titular deberá estar, a su vez, en las dos listas. -- unificar variables.
    
    def add_prof_asoc(self,nombre,DNI,direccion,sexo,departamento):
        prof_asoc = ProfesorAsociado(nombre,DNI,direccion,sexo,departamento)
        self._lista_prof_asoc.append(prof_asoc)
    
    def add_investigador(self,nombre,DNI,direccion,sexo,area,departamento):
        invest = Investigador(nombre,DNI,direccion,sexo,area,departamento)
        self._lista_inves.append(invest)
    
    def add_asig(self,nombre,creditos):
        for i in self._lista_asig:
            if i.nombre == nombre:
                raise Repeated('Error. Ya hay una asignatura con este nombre.')
        asig = Asignatura(nombre,creditos) # ya se ha creado una nueva instancia de asignatura.
        self._lista_asig.append(asig)

    def del_estudiante(self,estudiante):
        est = self._buscaestud(estudiante)
        self._lista_est.remove(est) # se elimina de la lista de estudiantes.
        for i in est.listaAsig: # en la lista de asignaturas de estudiante estará almacenado los objetos asignaturas.
            i.del_estudiante(est) # habrá que eliminar de las asig que tenga el estudiante a este mismo.
        
    
    def del_profesor(self,profesor):
        prof_asoc = self._buscaprofAsoc(profesor)
        if prof_asoc == None:
            prof_titular = self._buscaprofTitular(profesor)
            if prof_titular == None:
                raise NotFound('Error. Este profesor no se encuentra en la base de datos') # ese nombre no corresponde a ningún profesor.
            else: # signfica que profesor es un profesor titular.
                prof = self._buscaprofTitular(profesor)
                self._lista_prof_tit.remove(prof)
                self._lista_inves.remove(prof) # al ser una composición también se elimina.
                for i in prof.listaAsig:
                    i.del_profesor(prof)
        else: # es un profesor asociado
            prof = self._buscaprofAsoc(profesor)
            self._lista_prof_asoc.remove(prof)
            for i in prof.listaAsig:
                i.del_profesor(prof)
        
    def del_investigador(self,investigador):
        try:
            invest = self._buscainvest(investigador)
            self._lista_inves.remove(invest)
            if invest in self._lista_prof_tit:
                self._lista_prof_tit.remove(invest) # se elimina también de la lista de profesores titulares.
        except:
            raise NotFound('Error. Este investigador no se encuentra en la base de datos.')
        

    def cambiar_dep(self,nombre, dep):
        assert dep == Departamento.DIIC or dep == Departamento.DIS or dep == Departamento.DITEC , 'Nombre de departamento inválido.'
        try:
            p = self._buscaprofAsoc(nombre)
            if p != None:
                p.miembro.cambiar_dep(dep)
            else:
                pt = self._buscaprofTitular(nombre)
                if pt != None:
                    pt.miembro.cambiar_dep(dep)
                    inv = self._buscainvest(nombre) #todos los prof titulares son tmb investigadores
                    inv.miembro.cambiar_dep(dep)
                else:
                    i = self._buscainvest(nombre)
                    if self._buscainvest(nombre) != None: #investigadores q no son prof titulares
                        i.miembro.cambiar_dep(dep)
        except:
            raise NotFound('Error. Esta persona no se encuentra en la base de datos.')

            
    def asignar_asig_est(self,estudiante,nom_asig):
        asig = self._buscaasig(nom_asig)
        est = self._buscaestud(estudiante)
        if asig in est.listaAsig:
            raise Repeated('Error. Esta asignatura ya estaba asignada a este estudiante.')
        est.add_asig(asig)
        asig.add_estudiante(est)
    
    def del_asig_est(self, estudiante, nom_asig):
        asig = self._buscaasig(nom_asig)
        est = self._buscaestud(estudiante)
        if asig  not in est.listaAsig:
            raise NotFound('Error. Esta asignatura no se encuentra entre las asignaturas del estudiante.')
        est.del_asig(asig)
        asig.del_estudiante(est)

    def asignar_asig_prof(self,profesor,nom_asig): # nombre del profesor asig y nombre de la asignatura.
        asig = self._buscaasig(nom_asig) # se ha encontrado a la asignatura.
        prof_asoc = self._buscaprofAsoc(profesor)
        if prof_asoc == None:
            prof_tit = self._buscaprofTitular(profesor)
            if prof_tit == None:
                raise NotFound('Error. Este profesor no se encuentra en la base de datos.')
            else: # profesor titular
                if asig in prof_tit.listaAsig:
                    raise Repeated('Error. Esta asignatura ya estaba asignada a este profesor.')
                prof_tit.add_asig(asig)
                asig.add_profesor(prof_tit)
        else:
            if asig in prof_asoc.listaAsig:
                    raise Repeated('Error. Esta asignatura ya estaba asignada a este profesor.')
            prof_asoc.add_asig(asig)
            asig.add_profesor(prof_asoc)
    
    def del_asig_prof(self, profesor, nom_asig):
        asig = self._buscaasig(nom_asig) # se ha encontrado a la asignatura.
        prof_asoc = self._buscaprofAsoc(profesor)
        if prof_asoc == None:
            prof_tit = self._buscaprofTitular(profesor)
            if prof_tit == None:
                raise NotFound('Error. Este profesor no se encuentra en la base de datos.')
            else: # profesor titular
                if asig not in prof_tit.listaAsig:
                    raise NotFound('Error. Esta asignatura no se encuentra entre las asignaturas del profesor.')
                prof_tit.del_asig(asig)
                asig.del_profesor(prof_tit)
        else:
            if asig not in prof_asoc.listaAsig:
                    raise NotFound('Error. Esta asignatura no se encuentra entre las asignaturas del profesor.')
            prof_asoc.del_asig(asig)
            asig.del_profesot(prof_asoc)
        
    

    def get_estudiantes(self):
        for est in self._lista_est:
            print(est)
    
    def get_prof_tit(self):
        for prof in self._lista_prof_tit:
            print(prof)
    
    def get_prof_asoc(self):
        for prof in self._lista_prof_asoc:
            print(prof)

    def get_inves(self):
        for i in self._lista_inves:
            print(i)
        
if __name__ == "__main__":
    # Crear una instancia de la universidad
    uni = Universidad('UPCT', 30203, 'Cartagena')

    # Agregar asignaturas
    uni.add_asig('Machine Learning', 6)
    uni.add_asig('Programación para CD', 4)
    uni.add_asig('Calculo II', 8)

    # Agregar profesores asociados
    uni.add_prof_asoc('Isaac', '123456789', 'ygfadgu', 'F', Departamento.DIIC)

    # Asignar asignatura a profesor asociado
    uni.asignar_asig_prof('Isaac', 'Machine Learning')

    # Agregar estudiantes
    uni.add_estudiante('Jota', '571867890', 'fsgsh', 'M')
    uni.add_estudiante('Guille', '571867891', 'fsgsh', 'M')
    uni.add_estudiante('Ruben', '571867892', 'fsgsh', 'M')

    # Asignar asignaturas a estudiantes
    uni.asignar_asig_est('Jota', 'Machine Learning')
    uni.asignar_asig_est('Guille', 'Calculo II')

    # Mostrar asignaturas de un estudiante
    print("Asignaturas de Jota:")
    for asig in uni._lista_asig:
        if 'Jota' in [est.nombre for est in asig.estudiantes]:
            print(asig)

    # Mostrar estudiantes de una asignatura
    print("Estudiantes de Calculo II:")
    for estudiante in uni._lista_est:
        for asig in estudiante.listaAsig:
            if asig.nombre == 'Calculo II':
                print(estudiante)

    # Mostrar estudiantes de una asignatura inexistente
    print("Estudiantes de una asignatura inexistente:")
    for estudiante in uni._lista_est:
        for asig in estudiante.listaAsig:
            if asig.nombre == 'Ingles':
                print(estudiante)

    # Eliminar asignatura de un estudiante / Asignatura Aprobada
    for estudiante in uni._lista_est:
        for asig in estudiante.listaAsig:
            if asig.nombre == 'Calculo II':
                estudiante.del_asig(asig)

    # Mostrar asignaturas de un estudiante después de eliminar una
    print("Asignaturas de Guille después de eliminar Calculo II:")
    for asig in uni._lista_asig:
        if 'Guille' in [est.nombre for est in asig.estudiantes]:
            print(asig)

    # Agregar profesor asociado
    uni.add_prof_asoc('Pedro', '123456790', 'bhsb', 'M', Departamento.DIIC)

    # Agregar profesor titular
    uni.add_prof_titular('Carmen', '896754145', 'bvsj', 'F', 'hhs', Departamento.DIS)
    uni.add_prof_titular('Javi', '871956432', 'hgca', 'M', 'bjwh', Departamento.DIIC)

    # Cambiar departamento de un profesor titular
    uni.cambiar_dep('Carmen', Departamento.DITEC)

    # Mostrar lista de asignaturas totales
    print("Lista de asignaturas totales:")
    for asig in uni._lista_asig:
        print(asig)

    # Mostrar estudiantes de una asignatura
    print("Estudiantes de Calculo II después de eliminar a Jota:")
    for estudiante in uni._lista_est:
        for asig in estudiante.listaAsig:
            if asig.nombre == 'Machine Learning':
                print(estudiante)