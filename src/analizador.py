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
    """Parsea los argumentos de la línea de comandos.

    Returns:
        argparse.Namespace: Argumentos parseados con atributos
            `input`, `output`, `min_length`, `max_length`, `min_GC` y `max_GC`.
    """

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
        type=float,
        default=0,
        help="Composición mínima de GC de las secuencias a considerar",
    )

    parser.add_argument(
        "--max-GC",
        type=float,
        help="Composición máxima de GC de las secuencias a considerar",
    )

    args = parser.parse_args()

    return args


# ------------------------------------------
# Leer el archivo fasta de entrada
# ------------------------------------------
# ------------------------------------------
# Responsabilidad: Guardar interacciones del archivo fasta
# Entrada: file_name
# Salida: secuencias
# ------------------------------------------

import os


def leer_fasta(file_name):
    """Lee secuencias FASTA desde un archivo.

    Args:
        file_name (str): Ruta al archivo FASTA de entrada.

    Returns:
        list[tuple[str, str]]: Lista de tuplas `(nombre, secuencia)`.

    Raises:
        SystemExit: Si el archivo no existe.
    """
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


# ------------------------------------------
# Contar la composición GC de las secuencias
# ------------------------------------------
# ------------------------------------------
# Responsabilidad: Contar la composición GC de cada secuencia
# Entrada: lista de tuplas (nombre, secuencia)
# Salida: lista de tuplas (nombre, porcentaje GC)
# ------------------------------------------


def calcular_gc(secuencias):
    """Calcula el porcentaje de GC para cada secuencia.

    Args:
        secuencias (list[tuple[str, str]]): Lista de tuplas `(nombre, secuencia)`.

    Returns:
        list[tuple[str, str, float]]: Lista de tuplas `(nombre, secuencia, porcentaje_gc)`.
    """
    resultados = []
    for name, seq in secuencias:
        seq = seq.upper()
        gc_count = seq.count("G") + seq.count("C")
        total_count = len(seq)
        porcentaje_gc = (gc_count / total_count * 100) if total_count else 0
        resultados.append((name, seq, porcentaje_gc))
    return resultados


# ------------------------------------------
# Contar tamaño de cada secuencia
# ------------------------------------------
# ------------------------------------------
# Responsabilidad: Contar el tamaño de cada secuencia
# Entrada: gc_por_secuencia (lista de tuplas con nombre, secuencia y porcentaje GC)
# Salida: tuplas (nombre, seq, tamaño, porcentaje GC)
# ------------------------------------------


def calcular_estadisticas(gc_por_secuencia):
    """Calcula la longitud de cada secuencia.

    Args:
        gc_por_secuencia (list[tuple[str, str, float]]): Lista de tuplas
            `(nombre, secuencia, porcentaje_gc)`.

    Returns:
        list[tuple[str, str, int, float]]: Lista de tuplas
            `(nombre, secuencia, tamaño, porcentaje_gc)`.
    """
    resultados = []
    for name, seq, gc in gc_por_secuencia:
        tamaño = len(seq)
        resultados.append((name, seq, tamaño, gc))
    return resultados


# ------------------------------------------
# Contar tamaño de cada secuencia
# ------------------------------------------
# ------------------------------------------
# Responsabilidad: Contar el tamaño de cada secuencia
# Entrada: gc_por_secuencia (lista de tuplas con nombre, secuencia y porcentaje GC)
# Salida: tuplas (nombre, seq, tamaño, porcentaje GC)
# ------------------------------------------


def pasa_filtros(estadisticas, args):
    """Filtra las secuencias según los argumentos de longitud y GC.

    Args:
        estadisticas (list[tuple[str, str, int, float]]): Lista de tuplas
            `(nombre, secuencia, tamaño, porcentaje_gc)`.
        args (argparse.Namespace): Argumentos parseados con filtros.

    Returns:
        list[tuple[str, str, int, float]]: Secuencias que cumplen los filtros.
    """
    resultados = []
    for name, seq, tamaño, gc in estadisticas:
        if args.min_length and tamaño < args.min_length:
            continue
        if args.max_length and tamaño > args.max_length:
            continue
        if args.min_GC and gc < args.min_GC:
            continue
        if args.max_GC and gc > args.max_GC:
            continue
        resultados.append((name, seq, tamaño, gc))
    return resultados


# ------------------------------------------
# Mandar a escribir el archivo de salida tsv
# ------------------------------------------
# ------------------------------------------
# Responsabilidad: crear un archivo de salida con las secuencias que cumplen los filtros
# Entrada: estadisticas_filtradas (lista de tuplas con nombre, secuencia, tamaño y porcentaje GC)
# Salida: output (archivo tsv con nombre, secuencia, tamaño y porcentaje GC)
# ------------------------------------------


def escribir_resultados(estadisticas_filtradas, output_file):
    """Escribe los resultados filtrados en un archivo TSV.

    Args:
        estadisticas_filtradas (list[tuple[str, str, int, float]]): Lista de tuplas
            `(nombre, secuencia, tamaño, porcentaje_gc)`.
        output_file (str): Ruta del archivo de salida.

    Returns:
        str: Ruta del archivo de salida.
    """
    with open(output_file, "w") as f:
        f.write("Nombre\tSecuencia\tTamaño\t%GC\n")
        for name, seq, tamaño, gc in estadisticas_filtradas:
            f.write(f"{name}\t{seq}\t{tamaño}\t{gc:.2f}\n")
    return output_file


def main():
    args = parsear_argumentos()
    file_name = args.input
    secuencias = leer_fasta(file_name)
    gc_por_secuencia = calcular_gc(secuencias)
    estadisticas = calcular_estadisticas(gc_por_secuencia)
    estadisticas_filtradas = pasa_filtros(estadisticas, args)
    output_file = args.output
    escribir_resultados(estadisticas_filtradas, output_file)
    print(f"Resultados escritos en {output_file}")


if __name__ == "__main__":
    main()
