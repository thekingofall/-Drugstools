# DrugSeqTools: Drug Discovery RNA Sequencing Data Processing Pipeline with Barcode and Unique Molecular Identifier Support

## Introduction

**DrugSeqTools** is a bioinformatics pipeline designed to process RNA sequencing (Drugseq) data that includes barcodes and Unique Molecular Identifiers (UMIs). This pipeline automates data transformation and counting steps, producing gene expression counts for downstream analysis.

Whether you're a researcher or a student interested in bioinformatics, this guide will help you understand and use DrugSeqTools effectively.

## Features

- **Data Transformation**: Processes raw sequencing reads to correctly associate barcodes and UMIs with each read.
- **UMI Counting**: Counts unique UMIs associated with each gene for accurate expression levels.
- **Automated Installation**: Checks and attempts to install required external dependencies automatically.
- **Flexible Execution**: Allows running the entire pipeline or specific steps as needed.
- **Customized Output**: Generates outputs suitable for downstream analysis, with the option to keep or remove intermediate files.

## Prerequisites

- **Conda**: A package and environment management system for installing dependencies.
- **Python 3.8**: The pipeline is written in Python and requires version 3.8.
- **Sequencing Data**: Paired-end RNA-seq FASTQ files with specific naming conventions (`*_1*.gz` and `*_2*.gz`).
- **Barcode File**: A text file containing barcodes, one per line.
- **GTF Annotation File**: A gene annotation file in GTF format.
- **Genome Index Directory**: A directory containing genome indices for alignment tools like STAR.

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/DrugSeqTools.git
cd DrugSeqTools
```

### Step 2: Check and Install Dependencies

Run the following command to check and install required dependencies:

```bash
drugstools --check-installation
```

This command will attempt to create a conda environment named **Drugseqtoolsenv** and install tools like **STAR**, **samtools**, **featureCounts**, and **umi_tools**.

### Step 3: Activate the Environment

Before running the pipeline, activate the conda environment:

```bash
conda activate Drugseqtoolsenv
```

## Usage

### Basic Command Structure

```bash
drugstools -f <readFolder> -b <barcodeFile> -o <outputDir> -g <gtfFile> -d <genomeDir> [options]
```

### Required Arguments

- `-f <readFolder>`: Path to the folder containing gzipped FASTQ files (`*_1*.gz` and `*_2*.gz`).
- `-b <barcodeFile>`: Path to the barcode file (one barcode per line).
- `-o <outputDir>`: Path to the output directory. Existing directories will be overwritten.
- `-g <gtfFile>`: Path to the GTF annotation file.
- `-d <genomeDir>`: Directory containing genome indices for alignment.

### Optional Arguments

- `--keep-temp-files`: Retain intermediate files generated during the pipeline execution.
- `--check-installation`: Check and attempt to auto-install required external dependencies.
- `--step=<step>`: Choose which pipeline step(s) to run (`all`, `transform`, or `count`). The default is `all`.

### Example Usage

```bash
drugstools -f ./data/reads -b ./barcodes.txt -o ./output -g ./genes.gtf -d ./genomeIndex
```

This command runs the entire pipeline on the sequencing data located in `./data/reads`, using the barcodes from `./barcodes.txt`, outputs results to `./output`, and uses the gene annotation and genome indices specified.

## Workflow Overview

1. **Data Transformation**:
   - Reads from FASTQ files are processed to associate barcodes and UMIs with the correct reads.
   - Generates transformed FASTQ files ready for counting.

2. **UMI Counting**:
   - Transformed reads are aligned to the genome using alignment tools like STAR.
   - UMIs are counted to produce accurate gene expression levels.

3. **Output Generation**:
   - Produces a counts table (`counts.tsv.gz`) suitable for downstream analysis.
   - Provides a summary file (`gene_assigned.summary`).

## Cleaning Up

By default, the pipeline removes intermediate files to save disk space. If you wish to keep these files for further inspection or debugging, use the `--keep-temp-files` option when running the command.

## Troubleshooting

- **Conda Not Found**: Ensure that Conda is installed and accessible from your terminal.
- **Dependencies Not Installed**: If the pipeline reports missing tools, rerun with the `--check-installation` option.
- **Incorrect File Naming**: The pipeline expects FASTQ files matching `*_1*.gz` and `*_2*.gz`. Ensure your files are named accordingly.
- **Permission Issues**: Make sure you have read and write permissions for all specified directories and files.

## Contributing

Contributions are welcome! If you encounter issues or have suggestions, please open an issue on the GitHub repository.

## License

This project is licensed under the Academic and Commercial Use Separation License.

---

## 中文版本

# DrugSeqTools
## 介绍

**DrugSeqTools** 是一个生物信息学流水线工具，旨在处理包含条形码（Barcodes）和唯一分子标识符（UMIs）的RNA测序（Drugseq）数据。该工具自动完成数据转换和计数步骤，生成用于下游分析的基因表达计数结果。

无论您是研究人员还是对生物信息学感兴趣的学生，本指南都将帮助您理解并有效使用DrugSeqTools。

## 功能特点

- **数据转换**：处理原始测序读段，将条形码和UMI正确关联到每个读段。
- **UMI计数**：统计与每个基因相关的独特UMI数量，提供准确的表达水平。
- **自动安装**：检查并尝试自动安装所需的外部依赖项。
- **灵活执行**：允许根据需要运行整个流水线或特定步骤。
- **自定义输出**：生成适合下游分析的输出文件，并可选择保留或删除中间文件。

## 前提条件

- **Conda**：用于安装依赖项的包和环境管理系统。
- **Python 3.8**：该流水线使用Python编写，需要版本3.8。
- **测序数据**：命名格式为`*_1*.gz` 和 `*_2*.gz`的成对RNA-seq FASTQ文件。
- **条形码文件**：包含条形码的文本文件，每行一个条形码。
- **GTF注释文件**：GTF格式的基因注释文件。
- **基因组索引目录**：包含用于比对工具的基因组索引的目录，例如用于STAR。

## 安装

### 第一步：克隆仓库

```bash
git clone https://github.com/yourusername/DrugSeqTools.git
cd DrugSeqTools
```

### 第二步：检查并安装依赖

运行以下命令检查并安装所需的依赖项：

```bash
drugstools --check-installation
```

此命令将尝试创建名为 **Drugseqtoolsenv** 的conda环境，并安装 **STAR**、**samtools**、**featureCounts** 和 **umi_tools** 等工具。

### 第三步：激活环境

在运行流水线之前，激活conda环境：

```bash
conda activate Drugseqtoolsenv
```

## 使用方法

### 基本命令结构

```bash
drugstools -f <readFolder> -b <barcodeFile> -o <outputDir> -g <gtfFile> -d <genomeDir> [options]
```

### 必需参数

- `-f <readFolder>`：包含压缩FASTQ文件（`*_1*.gz` 和 `*_2*.gz`）的文件夹。
- `-b <barcodeFile>`：条形码文件的路径（每行一个条形码）。
- `-o <outputDir>`：输出目录；如果存在同名目录，将被覆盖。
- `-g <gtfFile>`：GTF注释文件的路径。
- `-d <genomeDir>`：包含基因组索引的目录。

### 可选参数

- `--keep-temp-files`：保留执行过程中生成的中间文件。
- `--check-installation`：检查并尝试自动安装所需的外部依赖项。
- `--step=<step>`：选择要运行的流水线步骤（`all`、`transform` 或 `count`）。默认值为 `all`。

### 示例用法

```bash
drugstools -f ./data -b ./barcodes.txt -o ./output -g ./genes.gtf -d ./genomeIndex
```

该命令使用位于`./data`的测序数据，使用`./barcodes.txt`中的条形码，将结果输出到`./output`，并使用指定的基因注释和基因组索引运行整个流水线。

## 流程概述

1. **数据转换**：
   - 处理FASTQ文件中的读段，将条形码和UMI正确关联。
   - 生成转换后的FASTQ文件，供计数步骤使用。

2. **UMI计数**：
   - 使用STAR等比对工具将转换后的读段比对到基因组上。
   - 统计UMI数量，生成准确的基因表达水平。

3. **生成输出**：
   - 生成适合下游分析的计数表（`counts.tsv.gz`）。
   - 提供总结文件（`gene_assigned.summary`）。

## 清理

默认情况下，流水线会删除中间文件以节省磁盘空间。如果您希望保留这些文件以进行进一步检查，请在运行命令时使用 `--keep-temp-files` 选项。

## 常见问题解答

- **未找到Conda**：确保已安装Conda并可在终端中访问。
- **依赖项未安装**：如果流水线提示缺少工具，请使用 `--check-installation` 选项重新运行。
- **文件命名不正确**：流水线期望FASTQ文件匹配`*_1*.gz` 和 `*_2*.gz`模式。请确保您的文件命名正确。
- **权限问题**：确保您对所有指定的目录和文件具有读写权限。

## 贡献

欢迎您的贡献！如果您发现问题或有建议，请在GitHub仓库中提交issue。

## 许可证

本项目采用学术和商业使用分离许可证。

---

