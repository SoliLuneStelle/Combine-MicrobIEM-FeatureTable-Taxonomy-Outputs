# Combine-MicrobIEM-RepSeqs-Taxonomy-FeatureTable-Outputs
Combine MicrobIEM decontamination output (as a .tsv file) with Qiime2 rep-seqs, feature-table, and taxonomy output (as .tsv files)

To use this script you will need to have done the following: 

Files needed: \
feature-table.qza \
taxonomy.qza \
rep-seqs.qza \

#makes a biom_file directory and makes a feature-table.biom file \
qiime tools export --input-path feature-table.qza --output-path biom_file

#converts the .biom file to a tsv file of the feature table \
biom convert -i feature-table.biom -o feature-table.tsv --table-type="OTU table" --to-tsv

#makes a taxonomy directory with a taxonomy tsv file \
qiime tools export --input-path taxonomy.qza --output-path taxonomy

#To convert rep-sees to a tsv file, make a sequences.fasta file
qiime tools export \
  --input-path rep-seqs.qza \
  --output-path rep-seqs
  
#makes a rep-seqs tsv file \
awk '/^>/ {if (seq) print id"\t"seq; id=substr($0,2); seq=""} /^[^>]/ {seq=seq $0} END {print id"\t"seq}' \
  dna-sequences.fasta > rep-seqs.tsv

#fix/check headers in resulting tsv files \
#rename Feature ID to OTU_ID \
vi feature-table.tsv
#rename taxon taxonomy
vi taxonomy.tsv 
#add headers
vi rep-seqs.tsv 
