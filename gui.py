#!/usr/bin/python3
import csv_reader
import PySimpleGUIQt as sg
import sys


def open_file():
    layout = [[sg.Text('Filename')],
              [sg.Input(), sg.FileBrowse()],
              [sg.OK(), sg.Cancel()]]
    window = sg.Window('Select CSV').Layout(layout)
    event, (filename,) = window.Read()
    if event != 'OK':
        sys.exit()
    dump, headers_vals = csv_reader.read_file(filename)
    window.Close()
    return dump, headers_vals


def main():
    # Asks user for the CSV file to read
    dump, headers_vals = open_file()

    query = []
    for key, options in headers_vals.items():
        options = sorted(list(options))
        layout = [[sg.Text(f'Selecting {key}:')]]
        layout.append([sg.Listbox(values=options, select_mode='multiple', size=(80, 20))])
        layout.append([sg.Submit(), sg.Button('Use all')])
        window = sg.Window(key).Layout(layout)
        event, choices = window.Read()
        window.Close()
        if event == 'Use all':
            query.append(options)
        elif event is None:
            sys.exit()
        else:
            query.append(choices[0])

    query = tuple(query)
    q_res = csv_reader.get_dump_query(query, dump)
    str_res = f'Found {len(q_res)} coincidences:\n' + '\n'.join(str(e) for e in q_res)
    sg.PopupScrolled(str_res, size=(150, 17))

    # Asks user if he wants to save the document to a CSV file.
    layout = [
        [sg.Text('Do you want to save the results to a CSV file.')],
        [sg.Button('Yes'), sg.Button('No')]
    ]
    window = sg.Window(key).Layout(layout)
    event, choices = window.Read()
    window.Close()
    if event in [None, 'No']:
        sys.exit()

    layout = [
        [sg.Text('Select the name of the file:'), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('Save CSV').Layout(layout)
    event, values = window.Read()
    if event == 'Submit':
        csv_reader.write_csv(q_res, list(headers_vals.keys()), values[0])
    else:
        sys.exit()

if __name__ == '__main__':
    main()
