# -*- coding: utf-8 -*-

#Copyright 2016 César Pomar <cesarpomar18@gmail.com>
#
#This file is part of Perldoop.
#
#Perldoop is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Perldoop is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Perldoop.  If not, see <http://www.gnu.org/licenses/>.

from libs import Variables as Var
from libs import Messages as Msg

Msg.LANGUAGE = 'spanish'

class Options():
    def __init__(self):    
        super().__init__()            
        # Opciones codigo
        self.file_name = ''  # Nombre del fichero de entrada
        self.class_name = ''  # Nombre de la clase que engloba en codigo
        self.extend_class = ''  # Nombre de la clase padre
        self.main_class = False  # Indica si el codigo fuera de una funcion es codigo estatico o inicia la aplicacion
        self.read_comments = False  # Indica si el analizador lexico reconoce los comentarios
        self.emulate_parens = False  # Añade parentesis a las funciones si no los tienen
        self.optimize_code = False  # Optimiza el acceso de algunas sentencias
        self.jregex = False #Evaluar expresiones regualres con libreria jregex
        self.unreachable_code = False  # Comprueba la existencia de codigo inalcanzable
        self.error_abort = False  # Indica si en caso de error para el analisis
        
        # Opciones depuracion
        self.lexer_debug = False  # Muestra los tokens segun se van leyendo
        self.parser_debug = False  # Muestra las reglas mientras analizan el codigo
        self.parser_debug_file = ''  # El debug del parser se imprime en un fichero
        self.parser_debug_len = 40  # Numero maximo de codigo mostrado en las reglas
        self.parser_debug_details = False  # Muestra mas detalles dentro del fichero de depuracion

        # Atributos del analisis
        self.declare_types = {}  # Tipos declarados en las etiquetas
        self.variables = Var.global_vars(self)  # Variables del codigo por niveles
        self.assigns = [{}]  # Variables inicializadas
        self.reserved_var = {}  # Variables reservadas dinamicamente
        self.imports = {}  # Imports necesarios para java
        self.labels_line = {}  # Etiquetas de la linea
        
        self.functions = {}  # Cabeceras de las funciones declaradas
        self.function_head = None  # Cabecera de la funcion actual
        
        self.package_code = ''  # Codigo fuera de la clase que pertenece al paquete           
        self.global_code = ''  # Codigo fuera de funciones es agrupado todo junto
        self.functions_code = ''  # Codigo de las funciones
        self.atributes = ''  # Declaracion de variables globales
        
        self.code_error = False  # Indica si el codigo contiene errores
        self.init_var = True  # Indica si las variables son inicializadas al igualar
        self.foreach_flag = False  # Bandera para definir tipo del foreach
        self.is_package = False  # Indica si el codigo es un paquete
