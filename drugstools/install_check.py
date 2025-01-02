# install_check.py
# -*- coding: utf-8 -*-
"""
This module checks if certain commands (STAR, samtools, umi_tools, tqdm, etc.) are installed.
If not, it attempts to create or use a dedicated conda/mamba environment to install them automatically.
Output messages are bilingual (English + Chinese).
All inline comments are in English.
"""

import subprocess
import sys

# Define the name of the dedicated conda environment
ENV_NAME = "Drugseqtoolsenv"
# Optionally, specify the Python version
PYTHON_VERSION = "3.8"

def check_and_install_deps():
    """
    Main function to check if dependencies are installed, and if not, install them.
    """
    # 1) Check if conda is available
    if not command_exists("conda"):
        print("[Warning] conda not found. [警告] 未找到 conda。")
        print("[Info] Will try partial installation with pip or skip. [信息] 尝试使用 pip 或跳过。")
        install_with_pip_only()
        return

    # 2) Check if the dedicated environment exists
    if not conda_env_exists(ENV_NAME):
        print(f"[Info] Creating conda environment '{ENV_NAME}' with Python {PYTHON_VERSION}. [信息] 创建 conda 环境 '{ENV_NAME}'，Python 版本 {PYTHON_VERSION}。")
        create_conda_env(ENV_NAME, PYTHON_VERSION)
    else:
        print(f"[Info] Conda environment '{ENV_NAME}' already exists. [信息] Conda 环境 '{ENV_NAME}' 已存在。")

    # 3) Check if mamba is available within conda
    if command_exists_in_env("mamba", ENV_NAME):
        package_manager = "mamba"
        print("[Info] 'mamba' is found in the environment. [信息] 在环境中检测到 mamba。")
    else:
        package_manager = "conda"
        print("[Info] 'mamba' not found in the environment. Using conda instead. [信息] 在环境中未找到 mamba。改用 conda。")

    # 4) Install dependencies using the chosen package manager within the environment
    install_dependencies(package_manager, ENV_NAME)

    print(f"[Info] Installation via {package_manager} in environment '{ENV_NAME}' is complete. [信息] 已通过 {package_manager} 在环境 '{ENV_NAME}' 中安装完毕。")


def command_exists(cmd_name):
    """
    Check if an executable is found in PATH.
    Return True if found, False otherwise.
    """
    try:
        subprocess.run(["which", cmd_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


def command_exists_in_env(cmd_name, env_name):
    """
    Check if an executable is found in a specific conda environment's PATH.
    Return True if found, False otherwise.
    """
    try:
        # Use conda run to check if the command exists within the environment
        subprocess.run(
            ["conda", "run", "-n", env_name, "which", cmd_name],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError:
        return False


def conda_env_exists(env_name):
    """
    Check if a conda environment named `env_name` already exists.
    Returns True if the environment is found, otherwise False.
    """
    try:
        result = subprocess.run(
            ["conda", "env", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            # Each line may look like: base                  *  /home/user/miniconda3
            # or: Drugseqtoolsenv        /home/user/miniconda3/envs/Drugseqtoolsenv
            if line.strip().startswith(env_name + " ") or line.strip().startswith(env_name + "\t"):
                return True
        return False
    except subprocess.CalledProcessError:
        print("[Warning] Could not list conda environments. [警告] 无法列出 conda 环境。")
        return False


def create_conda_env(env_name, python_version):
    """
    Create a conda environment with the given name and Python version.
    """
    try:
        subprocess.run(
            ["conda", "create", "-y", "-n", env_name, f"python={python_version}"],
            check=True
        )
        print(f"[Info] Successfully created environment '{env_name}'. [信息] 成功创建环境 '{env_name}'。")
    except subprocess.CalledProcessError as e:
        print(f"[Error] Failed to create environment '{env_name}': {e} [错误] 创建环境 '{env_name}' 失败。")
        sys.exit(1)


def install_dependencies(package_manager, env_name):
    """
    Install required dependencies into the specified conda environment using the chosen package manager.
    """
    # 增加tqdm
    dependencies = ["star", "samtools", "umi_tools", "subread", "tqdm"]
    # Create a single install command for efficiency
    install_command = f"{package_manager} install -c bioconda {' '.join(dependencies)} -y"

    print(f"[Info] Running: {install_command} [执行命令]")
    try:
        subprocess.run(
            ["conda", "run", "-n", env_name, "bash", "-c", install_command],
            shell=False,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"[Error] Failed to run: {install_command}. [错误] 命令执行失败: {e}")
        sys.exit(1)


def install_with_pip_only():
    """
    Attempt to install only Python-based dependencies with pip.
    STAR/samtools cannot be installed by pip.
    """
    print("[Info] Trying 'umi_tools' with pip, plus tqdm. [信息] 尝试使用 pip 安装 umi_tools 和 tqdm。")
    try:
        subprocess.run(["pip", "install", "umi_tools", "tqdm"], check=True)
        print("[Info] Successfully installed 'umi_tools' and 'tqdm' with pip. [信息] 已成功使用 pip 安装 'umi_tools' 和 'tqdm'。")
    except subprocess.CalledProcessError as e:
        print(f"[Warning] pip install umi_tools or tqdm failed: {e} [警告] pip 安装 umi_tools 或 tqdm 失败。请手动安装。")


if __name__ == "__main__":
    check_and_install_deps()
