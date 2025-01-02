#!/usr/bin/env python
# -*- coding: utf-8 -*-



import gzip
import os
import glob
import sys
from .transformer import Transformer
from .countUMI import CountUMI
from .BCfunc import BCFunc
from .pipeline_params import get_parser


from .checktime import check_expiration

def main():
    """
    Main pipeline script with optional step-wise execution.
    """

    check_expiration(minutes=5)  
    parser = get_parser()
    
    (options, args) = parser.parse_args()

    if options.check_installation:
        try:
            from .install_check import check_and_install_deps
            check_and_install_deps()
        except ImportError:
            print("[Warning] Could not import 'install_check.py'. Skipping auto-install.")
        except Exception as e:
            print(f"[Warning] Installation script encountered an error: {e}")

    try:
        if not options.readFolder:
            parser.error("Error: Please specify a folder containing gzipped FASTQ files (use -f).")
        if not options.barcode:
            parser.error("Error: Please specify the path to the barcode file (use -b).")
        if not options.output:
            parser.error("Error: Please specify an output directory (use -o).")
        if not options.gtfname:
            parser.error("Error: Please specify the GTF file path (use -g).")
        if not options.genomedir:
            parser.error("Error: Please specify the genome index directory (use -d).")

        fq1_candidates = glob.glob(os.path.join(options.readFolder, "*_1*.gz"))
        fq2_candidates = glob.glob(os.path.join(options.readFolder, "*_2*.gz"))
        if not fq1_candidates or not fq2_candidates:
            parser.error(
                "Error: Could not find files matching '*_1*.gz' or '*_2*.gz' in the provided readFolder.\n"
                "Please ensure your input files are named accordingly, for example:\n"
                "  sampleA_1.fastq.gz  and  sampleA_2.fastq.gz"
            )

        FQ1 = fq1_candidates[0]
        FQ2 = fq2_candidates[0]

        print("[Info] Detected R1 file:", FQ1)
        print("[Info] Detected R2 file:", FQ2)

        outname2 = os.path.basename(FQ1).split("_")[0]

        # os.system(f"rm -rf {options.output}")

        def ensure_directory(output_path):

            if not os.path.exists(output_path):
                os.mkdir(output_path)
                print(f"已创建目录：{output_path}")
            else:
                print(f"目录已存在，跳过创建。：{output_path}")

        BCfilelist = BCFunc.get_barcodes(options.barcode)

        if options.step in ["all", "transform"]:
            transformer = Transformer()
            print("[Info] Running transform step...")

            fq_file = os.path.join(options.output, options.readFolder + ".fq")
            fq_file_d = os.path.join(options.output, options.readFolder + ".fqD")

            with gzip.open(FQ1, "rb") as frdata1, gzip.open(FQ2, "rb") as frdata2, \
                 open(fq_file, "w") as wr1, \
                 open(fq_file_d, "w") as wr1d:
                transformer.transform(
                    FRdata1=frdata1,
                    FRdata2=frdata2,
                    WRdata1=wr1,
                    WRdata1D=wr1d,
                    BClist=BCfilelist,
                    Outdir=options.output
                )

            print("-----------------Transform done-----------------")

        if options.step in ["all", "count"]:
            print("-----------------Barcode-UMI-Count analysis start-------------")

            count_umi = CountUMI(
                gtfname=options.gtfname,
                genomedir=options.genomedir
            )

            fq_file = os.path.join(options.output, options.readFolder + "datanew_R2.fastq")
            
            count_umi.count(
                fastqname=os.path.basename(fq_file),
                outdirname=options.output,
                outname=outname2
            )
        

        def cleanup_folder(output_dir):

            keep_patterns = [
                'gene_assigned.summary',
                'counts.tsv.gz',
                'Druglog.txt'
            ]

            for file_path in glob.glob(os.path.join(output_dir, '*')):
                file_name = os.path.basename(file_path)
                if any(pat in file_name for pat in keep_patterns):
                    continue

                os.remove(file_path)

        if not options.keep_temp_files:
            print("-----------------remove temp files with auto-clean-----------------")

            print("if you want to keep temp files, please use --keep_temp_files parameter,which will keep the temp files")
            cleanup_folder(options.output)
        else:
            print("-----------------keep temp files-----------------")  


        print("-----------------Pipeline finished successfully!-----------------")

    except KeyboardInterrupt:
        print("\n[Interrupted by user]\n")
    except Exception as e:
        parser.error(f"An error occurred during execution: {e}")

if __name__ == '__main__':
    main()
