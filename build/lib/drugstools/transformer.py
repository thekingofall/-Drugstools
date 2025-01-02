
### transformer.py
import gzip
import os

from tqdm import tqdm 

class Transformer:
    def __init__(self, same_seq="CAGTGGTATCAACGCAGA"):
        self.same_seq = same_seq

    def transform(self, FRdata1, FRdata2, WRdata1, WRdata1D, BClist, Outdir):
        index = 0
        datanew = open(os.path.join(Outdir, "datanew_R1.fastq"), "w+")
        datanew2 = open(os.path.join(Outdir, "datanew_R2.fastq"), "w+")
        Obread1 = open(os.path.join(Outdir, "Obread1.fastq"), "w+")
        Obread2 = open(os.path.join(Outdir, "Obread2.fastq"), "w+")
        with tqdm(desc="Processing reads", unit=" read") as pbar:
            while True:
                line1 = FRdata1.readline().rstrip().decode('utf-8')
                if not line1:
                    print(index)
                    break

                line2 = FRdata1.readline().rstrip().decode('utf-8')
                lineUMI_before = line2.split(self.same_seq)
                line3 = FRdata1.readline().rstrip().decode('utf-8')
                line4 = FRdata1.readline().rstrip().decode('utf-8')

                line2_1 = FRdata2.readline().rstrip().decode('utf-8')
                line2_2 = FRdata2.readline().rstrip().decode('utf-8')
                line2_3 = FRdata2.readline().rstrip().decode('utf-8')
                line2_4 = FRdata2.readline().rstrip().decode('utf-8')

                if len(lineUMI_before) > 1:
                    lineUMI = lineUMI_before[1]
                    lineUMI2 = str(lineUMI)[0:12]  # the first 12 bp as barcode
                    if lineUMI2 in BClist:
                        if len(lineUMI) > 23:
                            line1BC = (
                                line1.split(" ")[0] + "_" + lineUMI2 + "_" + lineUMI[12:22]
                                + " " + line1.split(" ")[1]
                            )
                            line2_1BC = (
                                line2_1.split(" ")[0] + "_" + lineUMI2 + "_" + lineUMI[12:22]
                                + " " + line2_1.split(" ")[1]
                            )
                            line2toBC = line2.split(self.same_seq)[1][22:]
                            line4toBC = line4[len(line4) - len(line2toBC):]
                            datanew.write(
                                line1BC + "\n"
                                + line2toBC + "\n"
                                + line3 + "\n"
                                + line4toBC + "\n"
                            )
                            datanew2.write(
                                line2_1BC + "\n"
                                + line2_2 + "\n"
                                + line2_3 + "\n"
                                + line2_4 + "\n"
                            )
                            index += 1
                        else:
                            Obread1.write(
                                line1 + "\n"
                                + line2 + "\n"
                                + line3 + "\n"
                                + line4 + "\n"
                            )
                            Obread2.write(
                                line2_1 + "\n"
                                + line2_2 + "\n"
                                + line2_3 + "\n"
                                + line2_4 + "\n"
                            )
                            WRdata1.write(lineUMI2 + "\n")
                    else:
                        WRdata1D.write(line2 + "\n")
                pbar.update(1)

        datanew.close()
        datanew2.close()
        Obread1.close()
        Obread2.close()
