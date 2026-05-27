# ------------------------------------------
# Definir los parametros
# ------------------------------------------
# ------------------------------------------
# Responsabilidad: Guardar los parametros de entrada
# Entrada: input, output, min-length, max-length, min-GC, max-GC
# Salida: args
# ------------------------------------------

# import argparse
import argparse


def parsear_argumentos():

    parser = argparse.ArgumentParser(
        description="Calcula la composición GC de las secuencias en un archivo fasta"
    )

    parser.add_argument("-i", "--input", help="Nombre del archivo fasta")

    parser.add_argument("-o", "--output", help="Nombre del archivo fasta")

    parser.add_argument(
        "--min-length",
        type=int,
        default=0,
        help="Longitud mínima de las secuencias a considerar",
    )

    parser.add_argument(
        "--max-length", type=int, help="Longitud máxima de las secuencias a considerar"
    )

    parser.add_argument(
        "--min-GC",
        type=int,
        default=0,
        help="Composición mínima de GC de las secuencias a considerar",
    )

    parser.add_argument(
        "--max-GC",
        type=int,
        help="Composición máxima de GC de las secuencias a considerar",
    )

    args = parser.parse_args()

    return args


args = parsear_argumentos()
file_name = args.input

# ------------------------------------------
# Leer el archivo fasta de entrada
# ------------------------------------------
# ------------------------------------------
# Responsabilidad: Guardar interacciones del archivo fasta
# Entrada: input
# Salida: secuencias
# ------------------------------------------

import os


def leer_fasta(file_name):
    interactions = []
    if not os.path.exists(file_name):
        print("Error: archivo no encontrado")
        exit(1)
    with open(file_name) as f:
        first = f.readline()
        seq = ""
        name = ""
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                name = line[1:].strip()
                if seq:
                    interactions.append((name, seq))
                    seq = ""
                continue
            seq += line
        if seq:
            interactions.append((name, seq))
    return interactions


print(leer_fasta(file_name))
