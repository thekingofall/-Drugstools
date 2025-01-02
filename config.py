from setuptools import setup, find_packages

setup(
    name="drugstools",
    version="1.0.0",
    description="A pipeline for processing RNA-seq data with barcode and UMI analysis.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/thekingofall/Drugstools.git",  # 
    packages=find_packages(),
    install_requires=[
        # 在此列出您的依赖包，例如：
        # "numpy>=1.18.5",
        # "pandas>=1.0.0",
    ],
    entry_points={
        'console_scripts': [
            'drugstools=drugstools.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
