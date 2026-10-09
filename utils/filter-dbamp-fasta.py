#!/usr/bin/env python3

import argparse

def read_names(filename):
    """Read names to exclude from a text file (one per line)."""
    with open(filename) as f:
        return {line.strip() for line in f if line.strip()}

def filter_fasta(fasta_file, names_to_remove, output_file):
    """Filter FASTA entries whose IDs are in names_to_remove."""
    write_record = False

    with open(fasta_file) as infile, open(output_file, "w") as outfile:
        for line in infile:
            if line.startswith(">"):
                # Extract sequence ID (first word after '>')
                seq_id = line[1:].split()[0]
                write_record = seq_id not in names_to_remove

            if write_record:
                outfile.write(line)

def main():
    parser = argparse.ArgumentParser(
        description="Remove FASTA entries whose IDs match names in a text file."
    )
    parser.add_argument("-f", "--fasta", required=True,
                        help="Input FASTA file")
    parser.add_argument("-l", "--list", required=True,
                        help="Text file containing IDs to remove (one per line)")
    parser.add_argument("-o", "--output", required=True,
                        help="Output FASTA file")

    args = parser.parse_args()

    names_to_remove = read_names(args.list)
    filter_fasta(args.fasta, names_to_remove, args.output)

if __name__ == "__main__":
    main()