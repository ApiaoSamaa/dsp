from codecs import EncodedFile
from copy import deepcopy
from io import BytesIO
from pathlib import Path
from sys import stdout
from typing import Dict, Optional, Tuple, Union

from chardet import detect
from pyfaidx import Fasta

from dsp.utils import uprint


def csv2dict(infile: Path) -> Dict[str, str]:
    """
    Simple function to read the a csv into a dictionary (faster than pandas)
    Args:
        infile: Path to input file, comma delimited

    Returns:dictionary with first field as key and second as value
    """
    dictionary = {}
    # will not work if csv file is saved as utf-8 in excel in a MAC
    with open(infile, mode='rb') as reader:
        data = BytesIO(reader.read())
        data2 = deepcopy(data)
        en = detect(data.read())['encoding']
        reader = EncodedFile(data2, en, file_encoding='ascii') # to write the data that may in the format of 'en' to 'ascii'
        for line in reader:
            if line:
                line = line.strip().split(b',')
                key = line[0].replace(b"/", b"_").replace(b"\\", b"_").decode('ascii')
                value = line[1].replace(b"/", b"_").replace(b"\\", b"_").decode('ascii')
                dictionary[key] = value
    return dictionary


def preprocessing(data_set: Union[Path, str], metadata: Optional[Path],
                  prefix: str = 'Train', output_path: Optional[Path] = None,
                  print_file: str = stdout
                  ) -> Tuple[Fasta, int, Optional[Dict[str, str]]]:
    """
    TODO: update these doc strings
    Preprocessing of fasta sequences using BioPython into a database of
    SeqRecord objects each representing a unique sequence, can handle
    multiple sequence fastas.

    seqs: main sequence database, dictionary-like object, no info on
    clusters cluster_names: list of all cluster names from sub-directory
     names.

    number_of_clusters: integer of the total count of clusters.

    cluster_sample_info: Dictionary with keys=cluster_names and values =
    a tuple consisting of: (number of samples in cluster,
        a list of accession ids corresponding to sequences of that cluster).

    total_seq: integer of the total sequence count in dataset.

    """

    # Iterate through all fasta files and read it into data structure
    def replace(x):
        return x.replace("/", "_").replace("\\", "_")

    data_set = Path(data_set).resolve()
    outfn = data_set.joinpath(f'{prefix}_all_seqs.fasta').resolve() \
        if output_path is None else \
        output_path.joinpath(f'{prefix}_all_seqs.fasta').resolve()
    outfn.parent.mkdir(exist_ok=True, parents=True)
    if metadata is not None:
        cluster_dict = csv2dict(metadata)
    else:
        cluster_dict = None
    if outfn.exists():
        uprint(f'File {outfn.name} exists and will be used! If this is '
               f'unintended, please remove the file\n', print_file=print_file)
    else:
        subdirs = [subdir for subdir in data_set.iterdir() if subdir.is_dir()]
        if not subdirs:
            for file in data_set.glob('[!.]*'):
                if file.suffix != '.fai' and '_all_seqs.fasta' not in str(file):
                    with open(file) as infile, open(outfn, 'a') as outfile:
                        outfile.write(f'{infile.read().strip()}\n')
        else:
            for subdir in subdirs:
                for file in subdir.glob('[!.]*'):
                    if file.suffix != '.fai' and '_all_seqs.fasta' not in str(file):
                        suboutfn = outfn.parent / subdir.name / outfn.name
                        suboutfn.parent.mkdir(parents=True, exist_ok=True)
                        with open(file) as infile, open(suboutfn, 'a') as outfile:
                            outfile.write(f'{infile.read().strip()}\n')
                            
    if not subdirs:
        seq_dict = []
        new_seq = Fasta(
            str(outfn), key_function=replace, duplicate_action="first",
            sequence_always_upper=True
        )
        seq_dict.append(new_seq)
    else:
        seq_dict = []
        for subdir in subdirs:
            suboutfn = outfn.parent / subdir.name / outfn.name
            new_seq = Fasta(
                str(suboutfn), key_function=replace, duplicate_action="first",
                sequence_always_upper=True
            )
            seq_dict.append(new_seq)
    #Check all samples in fasta are present in metadata (reverse need not be true)
    if metadata is not None:
        difference = [set(seq_dict[i].keys()).difference(cluster_dict.keys()) for i in range(len(seq_dict))]
        if all(difference):
            raise Exception(f"{''.join(difference)}"
                            f"Your metadata and your fasta don't match,"
                            f" check your input\nCulprit(s): ")
    total_seq = 0
    for i in range(len(seq_dict)):
        new_total_seq = len(seq_dict[i].keys())
        total_seq += new_total_seq
    return seq_dict, total_seq, cluster_dict
