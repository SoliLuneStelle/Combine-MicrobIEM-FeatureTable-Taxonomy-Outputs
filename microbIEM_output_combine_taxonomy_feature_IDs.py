DECONTAM_FILE_TSV = "decontaminated_feature_table.tsv"
TAXONOMY_FILE_TSV = "taxonomy.tsv"
FEATURE_TABLE_TSV = "feature-table.tsv"
OUTPUT_FILE_TSV = "combined_output.tsv"

# each file's first line is a header
# the first column of each file is the OUT_ID
# create a new file that combines the three files by starting with the DECONTAM_FILE_TSV
# do this by iterating through the DECONTAM_FILE_TSV and adding the taxonomy and feature table information on the end of each line
def combine_files(decontam_file, taxonomy_file, feature_table_file, output_file):
	with open(decontam_file, 'r') as decontam_f, \
		 open(taxonomy_file, 'r') as taxonomy_f, \
		 open(feature_table_file, 'r') as feature_table_f, \
		 open(output_file, 'w') as output_f:

		# Read headers
		decontam_header = decontam_f.readline().strip().split('\t')
		taxonomy_header = taxonomy_f.readline().strip().split('\t')
		feature_table_header = feature_table_f.readline().strip().split('\t')

		# Write combined header
		combined_header = decontam_header + taxonomy_header[1:] + feature_table_header[1:]
		output_f.write('\t'.join(combined_header) + '\n')

		# Create a dictionary for taxonomy and feature table data
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
			taxonomy_data = taxonomy_dict.get(out_id, [''] * (len(taxonomy_header) - 1))
			feature_data = feature_table_dict.get(out_id, [''] * (len(feature_table_header) - 1))
			combined_line = parts + taxonomy_data + feature_data
			output_f.write('\t'.join(combined_line) + '\n')

if __name__ == "__main__":
	combine_files(DECONTAM_FILE_TSV, TAXONOMY_FILE_TSV, FEATURE_TABLE_TSV, OUTPUT_FILE_TSV)
	print(f"Combined file created: {OUTPUT_FILE_TSV}")
else:
	print("This script is intended to be run as a standalone program.")
	print("Please run it directly to combine the files.")