import subprocess

def install_dependencies():
    commands = [
        "conda install -c bioconda star",
        "conda install -c bioconda samtools",
        "conda install -c bioconda umi_tools",
        "pip install gzip"
    ]
    
    for cmd in commands:
        subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    install_dependencies()