DECONTAM_FILE_TSV = "decontaminated_feature_table-0-20.tsv"
TAXONOMY_FILE_TSV = "taxonomy.tsv"
FEATURE_TABLE_TSV = "feature-table.tsv"
REP_SEQUENCE_FILE_TSV = "rep-seqs.tsv"
# append epoch timestamp to end of the output file name 'combined_output_0-20' eg 'combined_output_0-20-{timestamp}.tsv'
import time
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
OUTPUT_FILE_TSV = f"combined_output_0-20-{timestamp}.tsv"

# each file's first line is a header
# the first column of each file is the OUT_ID
# create a new file that combines the three files by starting with the DECONTAM_FILE_TSV
# do this by iterating through the DECONTAM_FILE_TSV and adding the taxonomy and feature table information on the end of each line
def combine_files(decontam_file, rep_seqs_file, taxonomy_file, feature_table_file, output_file):
	with open(decontam_file, 'r') as decontam_f, \
		 open(rep_seqs_file, 'r') as rep_seqs_f, \
		 open(taxonomy_file, 'r') as taxonomy_f, \
		 open(feature_table_file, 'r') as feature_table_f, \
		 open(output_file, 'w') as output_f:

		# Read headers
		decontam_header = decontam_f.readline().strip().split('\t')
		rep_seqs_header = rep_seqs_f.readline().strip().split('\t') 
		taxonomy_header = taxonomy_f.readline().strip().split('\t')
		feature_table_header = feature_table_f.readline().strip().split('\t')

		# Write combined header
		combined_header = decontam_header + rep_seqs_header[1:] + taxonomy_header[1:] + feature_table_header[1:]
		output_f.write('\t'.join(combined_header) + '\n')

		# Create a dictionary for rep_seqs, taxonomy, and feature table data
		rep_seqs_dict = {}
		for line in rep_seqs_f:
			parts = line.strip().split('\t')
			rep_seqs_dict[parts[0]] = parts[1:]	

		taxonomy_dict = {}
		for line in taxonomy_f:
			parts = line.strip().split('\t')
			taxonomy_dict[parts[0]] = parts[1:]

		feature_table_dict = {}
		for line in feature_table_f:
			parts = line.strip().split('\t')
			feature_table_dict[parts[0]] = parts[1:]

		# Process decontaminated file and combine data
		for line in decontam_f:
			parts = line.strip().split('\t')
			out_id = parts[0]
			repr_seq_data = rep_seqs_dict.get(out_id, [''] * (len(rep_seqs_header) - 1)) 
			taxonomy_data = taxonomy_dict.get(out_id, [''] * (len(taxonomy_header) - 1))
			feature_data = feature_table_dict.get(out_id, [''] * (len(feature_table_header) - 1))
			combined_line = parts + repr_seq_data + taxonomy_data + feature_data
			output_f.write('\t'.join(combined_line) + '\n')

if __name__ == "__main__":
	combine_files(DECONTAM_FILE_TSV, REP_SEQUENCE_FILE_TSV, TAXONOMY_FILE_TSV, FEATURE_TABLE_TSV, OUTPUT_FILE_TSV)
	print(f"Combined file created: {OUTPUT_FILE_TSV}")
else:
	print("This script is intended to be run as a standalone program.")
	print("Please run it directly to combine the files.")
