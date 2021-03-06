#!/usr/bin/python3
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

import argparse
import sys
import os.path
import re
from libs import Parser
from libs import Auxiliary as Aux
from libs import Messages as Msg

def analyzer(files, args, output, main=False):
	# Para cada fichero
	for file in files:
		# Comprobamos si existe
		if not os.path.exists(file):
			Msg.error(error='FILE_NOT_FOUND', file=file)
			quit()
		
		# Comprobamos si tenemos acceso a el
		if not os.access(file, os.R_OK):
			Msg.error(error='FILE_NOT_ACCESS', file=file)
			quit()
		
		# Creamosel parses
		parser = Parser()
		
		# Opciones basicas del parser
		parser.main_class = main
		parser.file_name = os.path.basename(file)
		parser.class_name = re.sub(r'(.*)\..*$', r'\1', parser.file_name)
		
		# Argumentos
		if args.read_comments:
			parser.read_comments = True
		if args.emulate_parens:
			parser.emulate_parens = True
		if args.optimize_code:
			parser.optimize_code = True
		if args.unreachable_code:
			parser.unreachable_code = True
		if args.jregex:
			parser.jregex = True
		if args.error_abort:
			parser.error_abort = True
		if args.debug_lexer:
			parser.lexer_debug = True
		if args.debug_parser:
			parser.parser_debug = True
			# Solo si se tienen permisos de escritura
			if args.debug_file and os.access(args.debug_file, os.W_OK):
				if args.debug_details:
					parser.parser_debug_details = True
			if args.debug_size:
				# Solo si es un numero positivo
				if args.debug_size > 0:
					parser.parser_debug_len = args.debug_size
		# Ejecucion
		input = open(file, 'r', encoding='utf8')
		perl = input.read()
		input.close()
			
		java = parser.parse(perl)
		# Si no hay errores
		if not parser.code_error:
			# Identamos el codigo
			java = Aux.identer(java)
			# Escribimos el codigo
			file = open(os.path.join(output, parser.class_name + '.java'), 'w', encoding='utf8')
			file.write(java)
			file.close()
	

if __name__ == '__main__':
	# Opciones del analizador
	argp = argparse.ArgumentParser(description=Msg.get_message('HELP_TOOL_DESCRIPTION'))
	argp.add_argument('files', nargs='+', action='store', metavar='infile'  , help=Msg.get_message('HELP_FILES'))
	argp.add_argument('-m', '--main', action='store_true', dest='main', help=Msg.get_message('HELP_MAIN'))
	argp.add_argument('-out', action='store', dest='out', default=os.getcwd(), metavar='dir', help=Msg.get_message('HELP_OUT'))
	argp.add_argument('-c', '--comments', action='store_true', dest='read_comments', help=Msg.get_message('HELP_COMMENTS'))
	argp.add_argument('-ep', '--emulate-parens', action='store_true', dest='emulate_parens', help=Msg.get_message('HELP_EMULATE_PAREN'))
	argp.add_argument('-oc', '--optimize-code', action='store_true', dest='optimize_code', help=Msg.get_message('HELP_OPTIMIZE_CODE'))
	argp.add_argument('-jr', '--jregex', action='store_true', dest='jregex', help=Msg.get_message('HELP_JREGEX'))
	argp.add_argument('-uc', '--unreachable-code', action='store_true', dest='unreachable_code', help=Msg.get_message('HELP_UNRECHEABLE_CODE'))
	argp.add_argument('-ea', '--error-abort', action='store_true', dest='error_abort', help=Msg.get_message('HELP_ERROR_ABORT'))
	# Opciondes de depuracion
	debug = argp.add_argument_group('debugger arguments', Msg.get_message('HELP_DEBUGGER'))
	debug.add_argument('-dl', '--debug-lexer', action='store_true', dest='debug_lexer', help=Msg.get_message('HELP_DEBUGGER_LEXER'))
	debug.add_argument('-dp', '--debug-parser', action='store_true', dest='debug_parser', help=Msg.get_message('HELP_DEBUGGER_PARSER'))
	debug.add_argument('-df', '--debug-file', action='store', type=str, dest='debug_file', metavar='file', help=Msg.get_message('HELP_DEBUGGER_FILE'))
	debug.add_argument('-ds', '--debug-size', action='store', type=int, dest='debug_size', metavar='size', help=Msg.get_message('HELP_DEBUGGER_SIZE'))
	debug.add_argument('-dd', '--debug-details', action='store_true', dest='debug_details', help=Msg.get_message('HELP_DEBUGGER_DETAILS'))
	
	args = argp.parse_args()
	
	# Comprobamos si existe el directorio de salida
	if not os.path.exists(args.out):
		Msg.error(error='OUT_NOT_FOUND')
		quit()	
	
	# Comprobamos si tiene permido para escribir la salida
	if not os.access(args.out, os.W_OK):
		Msg.error(error='OUT_NOT_ACCESS')
		quit()
	# Si necesita main
	if args.main:
		analyzer(args.files[:-1], args, args.out)
		analyzer(args.files[-1:], args, args.out, True)
	else:
		analyzer(args.files, args, args.out)

