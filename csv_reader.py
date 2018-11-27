#!/usr/bin/python3
import csv
import sys
from collections import namedtuple, OrderedDict


def _gen_stripped(stream):
    for lst in stream:
        yield [e.strip() for e in lst]


def get_options(vals):
    print("0: todas las opciones")
    options = sorted(list(vals))
    for i, v in enumerate(options, start=1):
        print(f"{i}: {v if v else None}")
    print("Ingresa los números a buscar separados por espacios,")
    print("a-b incluye todos los números entre a y b (inclusivo):")
    while True:
        res = set()
        tmp = input().split()
        for e in tmp:
            if e.isdigit():
                if int(e) == 0:
                    return options
                elif 0 < int(e) <= len(vals):
                    res.add(int(e))
                else:
                    print(f"Solo se pueden seleccionar números entre 0 y {len(options)}).")
                    res = None
                    break
            else:
                ran = e.split('-')
                if len(ran) != 2 or any(not c.isdigit() for c in ran) or int(ran[0]) > int(ran[1]) or int(ran[1]) > len(options):
                    print("Opciones inválidas")
                    res = None
                    break
                res |= set(range(int(ran[0]), int(ran[1]) + 1))
        if res:
            break
        print("Prueba de nuevo:")
    return [options[i - 1] for i in res]


def request_query(headers_values):
    query = []
    for header, vals in headers_values.items():
        print(f"Las opciones para '{header}' son:")
        query.append(get_options(vals))
    return query


def get_dump_query(query, dump):
    """
    Dada una *query* y un *dump*, devuelve una lista de las entradas en el
    dump que concuerdan con la query.

    Args:
        query: Una tupla en donde cada campo es una lista de los posibles
            valores que pueden tener los campos de una entrada en dump.
        dump: Una lista de tuplas.

    Returns:
        res: Una lista de las entradas en dump que cumplieron con los
            requisitos de query.
    """
    res = []
    for data in dump:
        for field, options in zip(data, query):
            if field not in options:
                break
        else:
            res.append(data)
    return res


def read_file(file_name):
    """
    Lee un archivo CSV y devuelve los encabezados y una diccionario de todas
    las entradas.

    Args:
        file_name: Nombre del archivo CSV a leer.

    Returns:
        data_dump: Una lista de tuplas de todas las entradas en el archivo CSV
            con cada campo en su posición respectiva.
        headers_vals: Un diccionario ordenado en donde cada entrada es un
            encabezado del archivo CSV y los valores que puede tomar. Las
            llaves están ordenadas en el orden en que aparecen en el
            archivo CSV.
    """
    with open(file_name, 'r') as fp:
        csv_reader = _gen_stripped(csv.reader(fp))
        headers = next(csv_reader)
        global data
        data = namedtuple('Data', [e.replace(' ', '_') for e in headers])
        headers_vals = OrderedDict((header, set()) for header in headers)
        data_dump = set()
        for row in csv_reader:
            data_dump.add(data(*row))
            for header, val in zip(headers_vals, row):
                headers_vals[header].add(val)
    return data_dump, headers_vals


def write_csv(qr, headers, file_name):
    """
    Crea un archivo CSV con las entradas en *qr* usando los valores en
    *headers* como encabezado.

    Args:
        qr: Lista de tuplas, las entradas del archivo CSV.
        headers: Lista de strings, las entradas de la cabecera del CSV.
    """
    fp = open(file_name, 'w', encoding='utf8')
    csv_w = csv.writer(fp)
    csv_w.writerow(headers)
    csv_w.writerows(qr)
    fp.close()


def main():
    dump, headers_vals = read_file('SYB61_T06_Ratio of Girls to Boys in Education.csv')  # noqa
    while True:
        print("Ingresa tu query")
        query = data(*request_query(headers_vals))
        query_result = get_dump_query(query, dump)
        for e in query_result:
            print(e)
        print(f"Query completada, hubieron {len(query_result)} coincidencias.")
        while True:
            print("Ingresa 'n' para realizar otra query, 'f' para guardar el archivo en formato CSV o 'q' para salir:")
            user_choice = input().strip().strip('\'')
            if user_choice == 'f':
                filename = input("Nombre del archivo en el que guardar: ")
                write_csv(query_result, [k for k in headers_vals], filename)
                print("El archivo fue guardado correctamente.")
            elif user_choice == 'n':
                break
            elif user_choice == 'q':
                sys.exit()


if __name__ == '__main__':
    main()
