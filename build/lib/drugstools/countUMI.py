import os
import datetime

class CountUMI:
    def __init__(self, gtfname, genomedir, featurecountthread="4", starthread="8"):
        self.gtfname = gtfname
        self.genomedir = genomedir
        self.featurecountthread = featurecountthread
        self.starthread = starthread

    def count(self, fastqname, outdirname, outname):
        now = datetime.datetime.now().strftime("%Y%m%d%H%M")
        log_filename = now + "Druglog.txt"
        
        infile = os.path.join(outdirname, "datanew_R2.fastq")
        outfile = os.path.join(outdirname, outname)
        outbam = os.path.join(outdirname, outname + "_Aligned.sortedByCoord.out.bam")
        
        star_cmd = (
            f"STAR --runThreadN {self.starthread} "
            f"--genomeDir {self.genomedir} "
            f"--readFilesIn {infile} "
            f"--outFileNamePrefix {outdirname}/{outname}_ "
            f"--outFilterMultimapNmax 1 --outSAMtype BAM SortedByCoordinate "
            f">> {log_filename} 2>&1"
        )
        featurecounts_cmd = (
            f"featureCounts -a {self.gtfname} -o gene_assigned "
            f"-R BAM {outbam} -T {self.featurecountthread} "
            f">> {log_filename} 2>&1"
        )
        mv1_cmd = f"mv gene_assigned* {outdirname} >> {log_filename} 2>&1"
        mv2_cmd = f"mv *featureCounts* {outdirname} >> {log_filename} 2>&1"
        samtools_sort_cmd = (
            f"samtools sort {outbam}.featureCounts.bam "
            f"-o {outfile}_assigned_sorted.bam "
            f">> {log_filename} 2>&1"
        )
        samtools_index_cmd = (
            f"samtools index {outfile}_assigned_sorted.bam "
            f">> {log_filename} 2>&1"
        )
        umi_tools_cmd = (
            f"umi_tools count --per-gene --gene-tag=XT --assigned-status-tag=XS "
            f"--per-cell --wide-format-cell-counts "
            f"-I {outfile}_assigned_sorted.bam "
            f"-S {outfile}_counts.tsv.gz "
            f">> {log_filename} 2>&1"
        )
        
        os.system(star_cmd)
        print(outbam)
        os.system(featurecounts_cmd)
        os.system(mv1_cmd)
        os.system(mv2_cmd)
        os.system(samtools_sort_cmd)
        os.system(samtools_index_cmd)
        os.system(umi_tools_cmd)
