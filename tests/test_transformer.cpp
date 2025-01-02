#include <iostream>
#include <fstream>
#include <string>
#include <unordered_set>
#include <vector>
#include <cstdlib>   // For EXIT_SUCCESS, EXIT_FAILURE
#include <algorithm> // For string manipulation functions if needed

// Transformer class in C++.
// The logic is similar to the Python version, but adapted for C++.
class Transformer {
public:
    // Constructor to set the same_seq member variable (default: "CAGTGGTATCAACGCAGA").
    Transformer(const std::string &same_seq_ = "CAGTGGTATCAACGCAGA")
        : same_seq(same_seq_) {}

    // transform() function replicates the Python logic.
    // FRdata1, FRdata2: input file streams for read1 and read2.
    // WRdata1, WRdata1D: output file streams for writing specific barcodes.
    // BClist: a set of valid barcodes.
    // Outdir: output directory path (for writing files like datanew_R1.fastq, etc.).
    void transform(std::istream &FRdata1,
                   std::istream &FRdata2,
                   std::ostream &WRdata1,
                   std::ostream &WRdata1D,
                   const std::unordered_set<std::string> &BClist,
                   const std::string &Outdir)
    {
        // Indices and counters
        size_t index = 0;

        // Open output files in the specified directory
        std::ofstream datanew((Outdir + "/datanew_R1.fastq").c_str());
        std::ofstream datanew2((Outdir + "/datanew_R2.fastq").c_str());
        std::ofstream Obread1((Outdir + "/Obread1.fastq").c_str());
        std::ofstream Obread2((Outdir + "/Obread2.fastq").c_str());

        if (!datanew.is_open() || !datanew2.is_open() ||
            !Obread1.is_open() || !Obread2.is_open()) {
            std::cerr << "Error: Could not open one or more output files." << std::endl;
            return;
        }

        // We read 4 lines at a time from FRdata1 and FRdata2, mirroring the Python version.
        // Each loop iteration processes one "read pair".
        // We'll keep going until FRdata1 runs out of data.
        while (true) {
            // Read the first line from FRdata1
            std::string line1;
            if (!std::getline(FRdata1, line1)) {
                // End of file
                std::cout << index << std::endl; // mimic printing index
                break;
            }

            // Read the next three lines from FRdata1
            std::string line2, line3, line4;
            if (!std::getline(FRdata1, line2) ||
                !std::getline(FRdata1, line3) ||
                !std::getline(FRdata1, line4)) {
                // If we can't read complete 4 lines, we stop
                std::cout << index << std::endl;
                break;
            }

            // Read four lines from FRdata2
            std::string line2_1, line2_2, line2_3, line2_4;
            if (!std::getline(FRdata2, line2_1) ||
                !std::getline(FRdata2, line2_2) ||
                !std::getline(FRdata2, line2_3) ||
                !std::getline(FRdata2, line2_4)) {
                // If we can't read 4 lines from FRdata2, we stop
                std::cout << index << std::endl;
                break;
            }

            // Split line2 by the same_seq
            // We'll store the resulting parts in a vector of strings
            std::vector<std::string> lineUMI_before = splitString(line2, same_seq);

            // If we found more than 1 part, same_seq is found in line2
            if (lineUMI_before.size() > 1) {
                // lineUMI is everything after same_seq
                std::string lineUMI = lineUMI_before[1];
                // The first 12 bp as barcode
                std::string lineUMI2 = lineUMI.substr(0, 12);

                // Check if this 12bp barcode is in our BClist
                if (BClist.find(lineUMI2) != BClist.end()) {
                    // If the length of lineUMI is > 23, we proceed
                    if (lineUMI.size() > 23) {
                        std::string readName1 = parseReadName(line1, lineUMI2, lineUMI.substr(12, 10));
                        std::string readName2 = parseReadName(line2_1, lineUMI2, lineUMI.substr(12, 10));

                        // The portion of line2 after the 22bp that includes the same_seq
                        std::string line2toBC = lineUMI.substr(22); 
                        // The corresponding portion in line4
                        std::string line4toBC = line4.substr(line4.size() - line2toBC.size());

                        // Write to datanew_R1.fastq
                        datanew << readName1 << "\n"
                                << line2toBC << "\n"
                                << line3 << "\n"
                                << line4toBC << "\n";

                        // Write to datanew_R2.fastq
                        datanew2 << readName2 << "\n"
                                 << line2_2 << "\n"
                                 << line2_3 << "\n"
                                 << line2_4 << "\n";

                        index++;
                    } else {
                        // Write these "obread" lines if we can't proceed with the 22-bp requirement
                        Obread1 << line1 << "\n"
                                << line2 << "\n"
                                << line3 << "\n"
                                << line4 << "\n";

                        Obread2 << line2_1 << "\n"
                                << line2_2 << "\n"
                                << line2_3 << "\n"
                                << line2_4 << "\n";

                        // Write the failing UMI to WRdata1
                        WRdata1 << lineUMI2 << "\n";
                    }
                } else {
                    // If the 12-bp UMI is not in BClist, write the entire line2 to WRdata1D
                    WRdata1D << line2 << "\n";
                }
            }

            // Here you could optionally implement a progress counter:
            // e.g., if (index % 10000 == 0) { std::cerr << "Processed " << index << " reads\n"; }
        }

        // Close output files
        datanew.close();
        datanew2.close();
        Obread1.close();
        Obread2.close();
    }

private:
    std::string same_seq;

    // Helper function to split a string by a given delimiter (in this case same_seq)
    std::vector<std::string> splitString(const std::string &str, const std::string &delim)
    {
        std::vector<std::string> result;
        size_t start = 0;
        size_t end = 0;
        while ((end = str.find(delim, start)) != std::string::npos) {
            // substring from [start..end)
            result.push_back(str.substr(start, end - start));
            start = end + delim.size();
        }
        // last segment
        result.push_back(str.substr(start));
        return result;
    }

    // Helper function to parse the read name and insert the UMI
    // For example: if line1 = "@ReadA 1:N:0:CGATC", then line1.split(" ")[0] = "@ReadA",
    // line1.split(" ")[1] = "1:N:0:CGATC", etc.
    // This replicates how you created line1BC in Python.
    std::string parseReadName(const std::string &originalName,
                              const std::string &UMI2,
                              const std::string &next10bp)
    {
        // Split the original name by the first space
        // Then reconstruct the name + "_" + UMI2 + "_" + next10bp + " " + remainder
        // Note: This is a basic approach; adjust if your naming pattern is different.
        size_t spacePos = originalName.find(' ');
        if (spacePos == std::string::npos) {
            // No space found, just append the UMI
            return originalName + "_" + UMI2 + "_" + next10bp;
        } else {
            std::string firstPart = originalName.substr(0, spacePos);
            std::string secondPart = originalName.substr(spacePos + 1);
            return firstPart + "_" + UMI2 + "_" + next10bp + " " + secondPart;
        }
    }
};

////////////////////////////////////////////////////////////////////////////////////
// Example usage (in a main function):
// g++ -std=c++17 -O2 -o transform main.cpp
// ./transform
////////////////////////////////////////////////////////////////////////////////////

int main(int argc, char** argv)
{
    // Example: we expect 7 arguments just to demonstrate usage:
    // 1) FRdata1 filename
    // 2) FRdata2 filename
    // 3) WRdata1 filename
    // 4) WRdata1D filename
    // 5) BClist filename
    // 6) Outdir
    // 7) same_seq (optional)
    if (argc < 6) {
        std::cerr << "Usage: " << argv[0] 
                  << " <FRdata1> <FRdata2> <WRdata1> <WRdata1D> <BClist> <Outdir> [same_seq]" 
                  << std::endl;
        return EXIT_FAILURE;
    }

    // Open input files
    std::ifstream FRdata1(argv[1]);
    std::ifstream FRdata2(argv[2]);
    if (!FRdata1.is_open() || !FRdata2.is_open()) {
        std::cerr << "Could not open FRdata1 or FRdata2." << std::endl;
        return EXIT_FAILURE;
    }

    // Open output files
    std::ofstream WRdata1(argv[3]);
    std::ofstream WRdata1D(argv[4]);
    if (!WRdata1.is_open() || !WRdata1D.is_open()) {
        std::cerr << "Could not open WRdata1 or WRdata1D." << std::endl;
        return EXIT_FAILURE;
    }

    // Load BClist into an unordered_set
    std::ifstream bcfile(argv[5]);
    if (!bcfile.is_open()) {
        std::cerr << "Could not open BClist file." << std::endl;
        return EXIT_FAILURE;
    }
    std::unordered_set<std::string> BClist;
    {
        std::string line;
        while (std::getline(bcfile, line)) {
            // Each line is one barcode
            BClist.insert(line);
        }
    }

    // Output directory
    std::string Outdir(argv[6]);

    // same_seq can be provided or defaults to the one in the constructor
    std::string same_seq = (argc > 7) ? argv[7] : "CAGTGGTATCAACGCAGA";

    // Create Transformer object
    Transformer transformer(same_seq);

    // Invoke transform()
    transformer.transform(FRdata1, FRdata2, WRdata1, WRdata1D, BClist, Outdir);

    return EXIT_SUCCESS;
}