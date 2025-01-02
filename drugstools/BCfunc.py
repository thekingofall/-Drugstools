class BCFunc:
    @staticmethod
    def get_barcodes(bcfile):
        namedir = []
        BCname = open(bcfile, "r+")
        for i in BCname:
            if i.rstrip("\n") != '':
                namedir.append(i.rstrip("\n"))
        return namedir