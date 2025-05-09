from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from datetime import *
from donantes import Donante
from receptores import Receptor
from vehiculo import Vehiculo
import random
if TYPE_CHECKING:
    from pacientes import Paciente
    from organo import Organo
    from centro_de_salud import Centro_Salud
    from ambulancia import Ambulancia
    from avion import Avion
    from helicoptero import Helicoptero
    from cirujano import Cirujano

class Sistema():


    def __init__(self, centros_salud: list, lista_receptores: list, lista_donantes: list):
        self.lista_receptores = lista_receptores
        self.lista_donantes = lista_donantes
        self.lista_centros = centros_salud



    def recibir_paciente(self, paciente: Paciente):
        if isinstance(paciente, Donante):
            self.recibir_donante(paciente)
        else:
            self.recibir_receptor(paciente)


    def recibir_donante(self, donante: Donante):
        self.lista_donantes.append(donante)
        for i in range(len(donante.lista_organos)):
            k = i
            self.buscar_match_donante(donante,donante.lista_organos[i],k)

    def recibir_receptor(self, receptor: Receptor):
        self.lista_receptores.append(receptor)
        self.buscar_match_receptor(receptor)
    

    def elegir_receptor(self, receptores: list):
        #La lista de receptores tiene todos los receptores compatibles que necesiten el órgano especificado
        #Esta lista fue hecha en la funcion buscar_match
        
        for i in range(len(receptores)):
            for k in range (0,len(receptores)-1-i):
                if(receptores[k+1].prioridad > receptores[k].prioridad):
                    a = receptores[k]
                    receptores[k] = receptores[k+1]
                    receptores[k+1] = a
        receptor_match = self.elegir_receptor_prioridad(receptores)
        return receptor_match # retorna el receptor de mayor prioridad


    def elegir_receptor_prioridad(self, receptores: list):
        for i in range(len(receptores)):
            for k in range (0,len(receptores)-1-i):
                if(receptores[k+1].dt_espera > receptores[k].dt_espera and receptores[k+1].prioridad == receptores[k].prioridad):
                    a = receptores[k]
                    receptores[k] = receptores[k+1]
                    receptores[k+1] = a
        return receptores[0]
    


    def buscar_match_donante(self,donante: Donante,organo: Organo, k):
        receptores = []
        for i in range(len(self.lista_receptores)):
            if(self.lista_receptores[i].organo_r._tipo == organo._tipo and self.lista_receptores[i]._t_sangre == donante._t_sangre):
                receptores.append(self.lista_receptores[i])
        if(len(receptores) == 0):
            print("no se encontraron receptores que cualifiquen") #printea si no encuentra match
            return
        receptor_match = self.elegir_receptor(receptores)
        hoy = date.today()
        donante.lista_organos[k].dt_hablacion = datetime.combine(hoy,time(random.randint(0,23),random.randint(0,59),random.randint(0,59))) # creo una fecha y tiempo de ablacion random
        fecha_hablacion = donante.lista_organos[k].dt_hablacion #guardo la fecha en una variable para pasarla entre funciones
        viaje = f"{donante.centro_salud.nombre}-{receptor_match.centro_salud.nombre}" #me guardo el viaje para pasarselo al vehiculo
        donante.centro_salud.asignar_vehiculo(receptor_match.centro_salud,viaje,fecha_hablacion)
        #Faltaria una funcion asignar_cirujano en funcion de que este disponible un especialista que coincide con el organo
        if (receptor_match.centro_salud.realizar_transplante(receptor_match, donante.lista_organos[k])):
            self.lista_receptores.remove(receptor_match)
            donante.lista_organos.remove(organo)
    

    def buscar_match_receptor(self, receptor: Receptor):
        for i in range(len(self.lista_donantes)):
            for k in range (len(self.lista_donantes[i].lista_organos)):
                if(receptor.organo_r._tipo == self.lista_donantes[i].lista_organos[k]._tipo and receptor._t_sangre == self.lista_donantes[i]._t_sangre):
                    hoy = date.today()
                    self.lista_donantes[i].lista_organos[k].dt_hablacion = datetime.combine(hoy,time(random.randint(0,23),random.randint(0,59),random.randint(0,59))) # creo una fecha y tiempo de ablacion random
                    fecha_hablacion = self.lista_donantes[i].lista_organos[k].dt_hablacion #guardo la fecha en una variable para pasarla entre funciones
                    viaje = f"{self.lista_donantes[i].centro_salud.nombre}-{receptor.centro_salud.nombre}" #me guardo el viaje para pasarselo al vehiculo
                    self.lista_donantes[i].centro_salud.asignar_vehiculo(receptor.centro_salud,viaje,fecha_hablacion)
                    #Faltaria una funcion asignar_cirujano en funcion de que este disponible un especialista que coincide con el organo
                    if (receptor.centro_salud.realizar_transplante(receptor, self.lista_donantes[i].lista_organos[k])):
                        self.lista_receptores.remove(receptor)
                        self.lista_donantes[i].lista_organos.pop(k)
                    return

        
