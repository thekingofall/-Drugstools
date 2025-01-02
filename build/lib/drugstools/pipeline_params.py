#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# English comments explaining the script:
# This script defines a function `get_parser()` which returns an OptionParser object.
# The parser includes bilingual (Chinese & English) help messages, with each language
# in its own paragraph for clarity.

from optparse import OptionParser

def get_parser():
    """
    中英双语参数说明

    中文：
    -f, --readFolder
      RNA-seq读段所在文件夹，需包含gz格式的FASTQ文件，
      文件名应包含 *_1*.gz 与 *_2*.gz。

    -b, --barcode
      条形码文件路径，文件中每行包含一个barcode序列。

    -o, --output
      输出目录路径，若已存在同名目录会被覆盖。

    -g, --gtfname
      基因注释文件(GTF)路径，例如 /path/to/genes.gtf。

    -d, --genomedir
      STAR 基因组索引文件夹路径，例如 /path/to/star_genomeIndex/。

    --keep-temp-files
      默认删除中间产物，若指定此参数则保留这些文件。

    --check-installation
      检查并尝试自动安装所需的外部依赖（STAR、samtools、featureCounts、umi_tools）。

    --step
      选择运行流程的步骤：可选 'all'（默认），'transform'，'count'。

    英文：
    -f, --readFolder
      Directory containing gzipped FASTQ files. Filenames should include '*_1*.gz'
      and '*_2*.gz'.

    -b, --barcode
      Path to a text file listing barcodes (one barcode per line).

    -o, --output
      Path to the output directory. Overwrites existing directory.

    -g, --gtfname
      Path to the GTF annotation file, e.g. /path/to/genes.gtf.

    -d, --genomedir
      Directory containing STAR genome indices, e.g. /path/to/star_genomeIndex/.

    --keep-temp-files
      By default, intermediate files are deleted. Use this option to keep them.

    --check-installation
      Check and attempt to auto-install required dependencies (STAR, samtools, 
      featureCounts, umi_tools).

    --step
      Choose which pipeline step(s) to run: 'all' (default), 'transform', or 'count'.

    示例 (Example):
        python pipeline_main.py \\
            -f /path/to/readFolder \\
            -b /path/to/barcodes.txt \\
            -o /path/to/outputDir \\
            -g /path/to/genes.gtf \\
            -d /path/to/star_genomeIndex \\
            --step all
    """

    parser = OptionParser(
        usage="usage: %prog -f <readFolder> -b <barcodeFile> -o <outputDir> -g <gtfFile> -d <genomeDir> [options]",
        version="%prog 1.0",
        description=(
            "Pipeline script for RNA-seq data with barcodes and UMIs.\n\n"
            "中文：此脚本包含中英双语说明，帮助解析命令行参数。\n"
            "English: This script provides bilingual instructions and parses command-line options."
        )
    )

    parser.add_option(
        "-f", "--readFolder",
        action="store",
        dest="readFolder",
        help=(
            "中文：RNA-seq读段所在文件夹 (包含 *_1*.gz, *_2*.gz)\n\n"
            "English: Path to the folder containing gzipped FASTQ files."
        )
    )

    parser.add_option(
        "-b", "--barcode",
        action="store",
        dest="barcode",
        help=(
            "中文：条形码文件路径 (每行一个barcode)\n\n"
            "English: Path to the barcode file (one barcode per line)."
        )
    )

    parser.add_option(
        "-o", "--output",
        action="store",
        dest="output",
        help=(
            "中文：输出结果文件夹，若已存在同名目录会被覆盖\n\n"
            "English: Path to the output directory. Overwrites existing directory."
        )
    )

    parser.add_option(
        "-g", "--gtfname",
        action="store",
        dest="gtfname",
        help=(
            "中文：基因注释文件GTF路径，例如 /path/to/genes.gtf\n\n"
            "English: Path to the GTF annotation file, e.g. /path/to/genes.gtf."
        )
    )

    parser.add_option(
        "-d", "--genomedir",
        action="store",
        dest="genomedir",
        help=(
            "中文：STAR基因组索引文件夹路径，例如 /path/to/star_genomeIndex/\n\n"
            "English: Directory containing STAR genome indices, e.g. /path/to/star_genomeIndex/."
        )
    )

    parser.add_option(
        "--keep-temp-files",
        action="store_true",
        dest="keep_temp_files",
        default=False,
        help=(
            "中文：默认删除中间产物，若指定此参数则保留这些文件\n\n"
            "English: By default, intermediate files are deleted. Use this option to keep them."
        )
    )

    parser.add_option(
        "--check-installation",
        action="store_true",
        dest="check_installation",
        default=False,
        help=(
            "中文：检查并尝试自动安装所需外部依赖（STAR、samtools、featureCounts、umi_tools）\n\n"
            "English: Check and attempt to auto-install required dependencies (STAR, samtools, "
            "featureCounts, umi_tools)."
        )
    )

    parser.add_option(
        "--step",
        action="store",
        dest="step",
        default="all",
        help=(
            "中文：选择运行流程的步骤 (all/transform/count)，默认 'all'\n\n"
            "English: Choose which pipeline step(s) to run (all/transform/count). Default 'all'."
        )
    )

    return parser
