#!/usr/bin/env python3

import subprocess
import os

def perform_bam_sam(fq_file, output_dir, ref_file):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        files = []
        for file_name in os.listdir(fq_file):
            if os.path.isfile(os.path.join(fq_file, file_name)):
                files.append(file_name)
                
        for r1_file in files:
            if r1_file.endswith("_R1.fastq.gz"):
                r2_file = r1_file.replace("_R1.fastq.gz", "_R2.fastq.gz")
                
                if r2_file in files:
                    r1_file_path = os.path.join(fq_file, r1_file)
                    r2_file_path = os.path.join(fq_file, r2_file)
                    output_sam_file = os.path.join(output_dir, f"{r1_file.replace('_R1', '')}.sam")
                    
                    command = ["bwa", "mem", "-M", "-R", ref_file, r1_file_path, r2_file_path, "-t", "4"]
                    
                    with open(output_sam_file, 'w') as output_file:
                        subprocess.run(command, stdout=output_file, text=True)
                    print(f"bwa mem for {r1_file} and {r2_file} completed and output saved to {output_sam_file}")
                else:
                    print(f"Match of {r1_file} not found")
    except Exception as e:
        print("Error occurred:", e)

# Setting paths here
output_dir = '/home/ad.gatech.edu/bio-mcgrath-dropbox/coverage_test/output_dir'
fq_file = '/home/ad.gatech.edu/bio-mcgrath-dropbox/coverage_test/fastq'
ref_file = '/home/ad.gatech.edu/bio-mcgrath-dropbox/Data/CichlidSequencingData/Genomes/Mzebra_UMD2a/GCF_000238955.4_M_zebra_UMD2a_genomic.fna'

# Call the function
perform_bam_sam(fq_file, output_dir, ref_file)
