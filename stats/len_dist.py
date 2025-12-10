import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_sequence_length_distribution(fasta_file_path):
    """
    Computes the lengths of all sequences in a FASTA file and 
    generates a histogram of the length distribution.

    Args:
        fasta_file_path (str): The path to the input FASTA file.
    """
    # 1. Read and Extract Sequence Lengths (Standard Python Parsing)
    sequence_lengths = []
    current_sequence = ""
    seqs = set()

    try:
        with open(fasta_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    # If we encounter a new header, and we have a sequence from before, record its length
                    if current_sequence and current_sequence not in seqs:
                        sequence_lengths.append(len(current_sequence))
                        seqs.add(current_sequence)
                    # Reset for the new sequence
                    current_sequence = ""
                elif line:
                    # Append sequence lines, ignoring headers and blank lines
                    current_sequence += line

            # Record the length of the very last sequence in the file
            if current_sequence:
                sequence_lengths.append(len(current_sequence))
    except FileNotFoundError:
        print(f"Error: The file '{fasta_file_path}' was not found.")
        return
    except Exception as e:
        print(f"An unexpected error occurred during file reading: {e}")
        return

    if not sequence_lengths:
        print("Error: No sequences found in the file. Check if the file is correctly formatted FASTA.")
        return

    print("UNIQUE SEQS", len(seqs), len(sequence_lengths))

    # Basic Statistics
    min_len = min(sequence_lengths)
    max_len = max(sequence_lengths)
    mean_len = np.mean(sequence_lengths)

    # 2. Generate the Histogram

    bin_width = 1
    # Bins cover the range from min_len up to and including max_len
    bins = np.arange(min_len, max_len + bin_width + 1, bin_width) - 0.5

    sns.set_theme(style="whitegrid")
    sns.set_context("paper", font_scale=1.25)
    sns.set_palette("muted")

    plt.figure(figsize=(5, 3))

    sns.histplot(
        sequence_lengths,
        bins=bins,
        kde=True,
        # color='skyblue',
        # zorder=2
    )

    # 3. Add Labels and Title
    plt.xlabel("Sequence Length")
    plt.ylabel("Count")
    # plt.title(
    #     f"Distribution of Sequence Lengths in {fasta_file_path}",
    #     fontsize=16
    # )

    # Add a vertical line for the mean length
    # plt.axvline(mean_len, color='red', linestyle='--',
    #             linewidth=2, label=f'Mean Length ({mean_len:.2f})')
    # plt.legend()

    # Add grid lines for easier reading of values
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Set x-ticks to be integers for clarity if the range is small
    if max_len - min_len < 40:
        plt.xticks(range(min_len, max_len + 1,
                   max(1, int((max_len - min_len) / 10))))

    # 4. Save the Plot
    output_filename = f"len_dist2.pdf"
    plt.savefig(output_filename, bbox_inches="tight")
    # plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <input_fasta_file>")
        print("Example: python script_name.py peptides.fasta")
    else:
        # The script takes the FASTA file path as a command-line argument
        fasta_file = sys.argv[1]
        plot_sequence_length_distribution(fasta_file)
