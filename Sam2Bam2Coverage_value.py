import subprocess
import os

def perform_sam(fq_file, SAM_FILES, ref_file):
    try:
        files = os.listdir(fq_file)
        r1_files = []
        r2_files = []
        if not os.path.exists(SAM_FILES):
            os.makedirs(SAM_FILES)

        for file_name in files:
            if file_name.endswith("_R1.fastq.gz"):
                r1_files.append(file_name)
            elif file_name.endswith("_R2.fastq.gz"):
                r2_files.append(file_name)

        for r1_file in r1_files:
            r1_file_path = os.path.join(fq_file, r1_file)
            common_identifier = r1_file[:-12]
            r2_file = None
            for r2_candidate in r2_files:
                if r2_candidate.startswith(common_identifier) and r2_candidate.endswith("_R2.fastq.gz"):
                    r2_file = r2_candidate
                    break
            if r2_file:
                r2_file_path = os.path.join(fq_file, r2_file)
                output_sam_file = os.path.join(SAM_FILES, f"{common_identifier}.sam")
                command = ["bwa", "mem", "-M", "-R",f"@RG\\tID:{r1_file}\\tSM:{r1_file}", ref_file, r1_file_path, r2_file_path, "-t", "4"]
                
                # Check if a SAM file already exists
                if not os.path.exists(output_sam_file):
                    with open(output_sam_file, 'w') as output_file:
                        subprocess.run(command, stdout=output_file, text=True)
                    print(f"bwa mem for {r1_file} and {r2_file} completed, output saved to {output_sam_file}")
            else:
                print(f"Match of {r2_file} not found for {r1_file}")
    except Exception as e:
        print("Error occurred:", e)

def perform_bam(SAM_FILES, BAM_FILES):
    try:
        if not os.path.exists(BAM_FILES):
            os.makedirs(BAM_FILES)
        
        sam_files = os.listdir(SAM_FILES)
        
        for sam_file in sam_files:
            if sam_file.endswith(".sam"):
                sam_file_path = os.path.join(SAM_FILES, sam_file)
                bam_file = os.path.splitext(sam_file)[0] + ".bam"
                bam_file_path = os.path.join(BAM_FILES, bam_file)
                
                # Check if a BAM file already exists
                if not os.path.exists(bam_file_path):
                    # Convert SAM to BAM
                    subprocess.run(["samtools", "view", "-bS", sam_file_path, "-o", bam_file_path])
                    
                    # Sort BAM
                    subprocess.run(["samtools", "sort", bam_file_path, os.path.join(BAM_FILES, os.path.splitext(bam_file)[0])])
                    
                    # Index BAM
                    subprocess.run(["samtools", "index", bam_file_path])
                    
                    print(f"Processed {sam_file} and saved as {bam_file}")
                    
                    # Delete the SAM file
                    os.remove(sam_file_path)
                    print(f"Deleted {sam_file}")
                else:
                    print(f"BAM file {bam_file} already exists, skipping conversion.")
    except Exception as e:
        print("Error occurred:", e)

def perform_coverage(BAM_FILES, Coverage_value):
    try:
        if not os.path.exists(Coverage_value):
            os.makedirs(Coverage_value)
        
        bam_files = os.listdir(BAM_FILES)
        
        for bam_file in bam_files:
            if bam_file.endswith(".bam"):
                bam_file_path = os.path.join(BAM_FILES, bam_file)
                output_txt_file = os.path.join(Coverage_value, f"{os.path.splitext(bam_file)[0]}.txt")
                
                # Check if a coverage file already exists
                if not os.path.exists(output_txt_file):
                    # Generate coverage depth file
                    subprocess.run(["samtools", "depth", bam_file_path, ">", output_txt_file], shell=True)
                    
                    print(f"Generated coverage depth for {bam_file} and saved as {output_txt_file}")
                else:
                    print(f"Coverage file {output_txt_file} already exists, skipping coverage calculation.")
    except Exception as e:
        print("Error occurred:", e)

def main():
    fq_file = '/home/ad.gatech.edu/bio-mcgrath-dropbox/coverage_test/fastq'
    ref_file = '/home/ad.gatech.edu/bio-mcgrath-dropbox/Data/CichlidSequencingData/Genomes/Mzebra_UMD2a/GCF_000238955.4_M_zebra_UMD2a_genomic.fna'
    SAM_FILES = '/home/ad.gatech.edu/bio-mcgrath-dropbox/coverage_test/SAM_FILES'
    BAM_FILES = '/home/ad.gatech.edu/bio-mcgrath-dropbox/coverage_test/BAM_FILES'
    Coverage_value = '/home/ad.gatech.edu/bio-mcgrath-dropbox/coverage_test/coverage_score'

    # Call the SAM processing function
    perform_sam(fq_file, SAM_FILES, ref_file)

    # Call the BAM processing function
    perform_bam(SAM_FILES, BAM_FILES)

    # Call the coverage depth function
    perform_coverage(BAM_FILES, Coverage_value)

if __name__ == "__main__":
    main()
