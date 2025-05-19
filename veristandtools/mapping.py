import csv
import os
from niveristand._auto_generated_classes import VeriStandSdfError
from niveristand.systemdefinitionapi import SystemDefinition
from errors import VeriStandErrors
from typing import Tuple, List, Dict


def add_file_mappings(sysdef: SystemDefinition, mapping_path: str) -> None:
    '''
    Add all mappings in TSV file to System Definition

    Args:
        sysdef: VeriStand SystemDefinition object.
        file_path: Path to mappings file or folder containing mapping files.
    '''

    if os.path.isdir(mapping_path):
        mapping_files = [os.path.join(mapping_path, file)
                         for file in os.listdir(mapping_path)]
    else:
        mapping_files = [mapping_path]

    for file_path in mapping_files:
        print(f'Importing Mappings from: {file_path}...')
        mappings = _import_mapping_file(file_path)
        add_mappings(sysdef, mappings)


def _import_mapping_file(file_path: str) -> List[Tuple[str, str]]:
    '''
    Reads VeriStand mapping file

    Args:
        file_path: Path to the VeriStand mapping file

    Returns:
        mappings: List of all mappings. Mappings are stored as Tuples with source and destination paths.
    '''

    with open(file_path) as mapping_file:
        reader = csv.reader(mapping_file, delimiter='\t')
        mappings = [tuple(row) for row in reader]

    return mappings


def add_mappings(sysdef: SystemDefinition, mappings: List[Tuple[str, str]]) -> None:
    '''
    Adds mappings to System Definition

    Args:
        sysdef: VeriStand SystemDefinition object.
        mappings: List of VeriStand mappings where each mapping is a tuple containing the sourceand destination channels
    '''
    current_mappings = {destination: source for source,
                        destination in get_mappings(sysdef)}

    for source, destination in mappings:
        if _is_destination_mapped(current_mappings, source, destination):
            print(f"Destination Already Mapped: {source} -> {destination}")
        else:
            try:
                sysdef.root.add_channel_mappings([source], [destination])
            except VeriStandSdfError as e:
                match e.code:
                    case VeriStandErrors.InputParameterInvalid.value:
                        print(e.message)
                    case _:
                        print(e.code)
            else:
                current_mappings[destination] = source


def _is_destination_mapped(current_mappings: Dict[str, str], source: str, destination: str) -> bool:
    '''
    Checks whether the destination is already mapped to a different source
    '''

    mapped_source = current_mappings.get(destination)

    if mapped_source is not None and mapped_source != source:
        return True
    else:
        return False


def get_mappings(sysdef: SystemDefinition) -> List[Tuple[str, str]]:
    '''
    Returns all mappings in given system definition.

    Args:
        sysdef: VeriStand SystemDefinition object.

    Returns:
        mappings: List of all mappings. Mappings are stored as Tuples with source and destination paths.
    '''

    source, destination = sysdef.root.get_channel_mappings()
    return list(zip(source, destination))


def delete_all_mappings(sysdef: SystemDefinition) -> None:
    '''
    Deletes all mappings in given system definition.

    Args:
        sysdef: VeriStand SystemDefinition object.
    '''

    sysdef.root.clear_channel_mappings()


def delete_file_mappings(sysdef: SystemDefinition, file_path: str) -> None:
    '''
    Deletes mappings from sysdef if source/destination pair is found in file

    Args:
        sysdef: VeriStand SystemDefinition object.
        file_path: Path to mapping file.
    '''
    current_mappings = get_mappings(sysdef)
    file_mappings = _import_mapping_file(file_path)

    matching = [destination for source,
                destination in file_mappings if (source, destination) in current_mappings]

    print(f"Deleting {len(matching)} mappings from {file_path}")

    sysdef.root.delete_channel_mappings(matching)


if __name__ == "__main__":
    sysdef_file = r"C:\Users\MattJ\Desktop\BASC\BASC.nivssdf"
    mapping_file = r"C:\Users\MattJ\Desktop\BASC\Configuration Files\Mapping\A429_RX.txt"
    mapping_folder = r"C:\Users\MattJ\Desktop\BASC\Configuration Files\Mapping"

    sd = SystemDefinition(sysdef_file)
    # delete_all_mappings(sd)
    delete_file_mappings(sd, mapping_file)
    results = sd.save_system_definition_file()

    print(f"Results: {results}")
