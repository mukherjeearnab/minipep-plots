import sys
from collections import Counter
import matplotlib.pyplot as plt
from Bio import SeqIO
import seaborn as sns

# --- Configuration ---
# Define the standard 20 amino acids for consistency
STANDARD_AMINO_ACIDS = 'ACDEFGHIKLMNPQRSTVWY'


def compute_and_plot_aa_frequency(fasta_file_path):
    """
    Computes the total amino acid frequency across all sequences in a FASTA file 
    and generates a bar plot.

    Args:
        fasta_file_path (str): The path to the input FASTA file.
    """
    print(f"--- Analyzing file: {fasta_file_path} ---")

    try:
        # 1. Read and Aggregate Sequences
        all_amino_acids = []
        total_residues = 0

        # Use Biopython's SeqIO to parse the FASTA file efficiently
        for record in SeqIO.parse(fasta_file_path, "fasta"):
            # Convert sequence to uppercase and extend the list
            sequence = str(record.seq).upper()
            all_amino_acids.extend(list(sequence))
            total_residues += len(sequence)

        if total_residues == 0:
            print("Error: No sequences or residues found in the file.")
            return

        # 2. Count Frequencies
        # Use Counter to get the count of each residue
        raw_counts = Counter(all_amino_acids)

        # Filter for only the standard 20 amino acids and calculate percentages
        frequencies = {}
        for aa in STANDARD_AMINO_ACIDS:
            # Get count, defaulting to 0 if the AA is not present
            count = raw_counts.get(aa, 0)
            # Calculate percentage
            percentage = (count / total_residues) * 100
            frequencies[aa] = percentage

        # Identify and report non-standard residues (e.g., 'X', 'B', 'Z')
        non_standard_residues = {
            aa: count for aa, count in raw_counts.items()
            if aa not in STANDARD_AMINO_ACIDS
        }

        print(
            f"\nTotal sequences processed: {len(list(SeqIO.parse(fasta_file_path, 'fasta')))}")
        print(f"Total standard residues counted: {total_residues}")

        if non_standard_residues:
            print("\nNon-Standard Residues Found (Counts):")
            for aa, count in non_standard_residues.items():
                print(f"  {aa}: {count}")
            print(f"(These were NOT included in the final plot/percentage calculation)")

        # 3. Prepare Data for Plotting (Sorting by AA name)
        # Sort the dictionary keys (AAs) alphabetically for a standard plot order
        amino_acids = sorted(frequencies.keys())
        percentages = [frequencies[aa] for aa in amino_acids]

        # 4. Generate the Bar Plot
        sns.set_theme(style="whitegrid")
        sns.set_context("paper", font_scale=1.25)
        sns.set_palette("muted")

        plt.figure(figsize=(5, 3))

        # Create the bar plot
        sns.barplot(x=amino_acids, y=percentages)

        # Add labels and title
        plt.xlabel("Amino Acid")
        plt.ylabel("Relative Frequency (%)")
        # plt.title(
        #     f"Amino Acid Frequency Distribution for {fasta_file_path}",
        #     fontsize=16
        # )

        # Optional: Add grid lines for easier reading of values
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Optional: Rotate x-axis labels if needed (not necessary here)
        # plt.xticks(rotation=45)

        # Display the percentage value on top of each bar
        # for i, percent in enumerate(percentages):
        #     plt.text(
        #         i,
        #         percent + 0.5,  # Position the text slightly above the bar
        #         f"{percent:.2f}%",  # Format to two decimal places
        #         ha='center',
        #         fontsize=9
        #     )

        # 5. Save and Show the Plot
        # output_filename = f"aa_frequency_{fasta_file_path.replace('.fasta', '').replace('.fa', '')}.png"
        plt.savefig('./aa_dist.pdf', bbox_inches="tight")
        # print(f"\nPlot saved as: {output_filename}")
        plt.show()

    except FileNotFoundError:
        print(f"Error: The file '{fasta_file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- Execution Block ---
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <input_fasta_file>")
        print("Example: python script_name.py peptides.fasta")
    else:
        # The script takes the FASTA file path as a command-line argument
        fasta_file = sys.argv[1]
        compute_and_plot_aa_frequency(fasta_file)
