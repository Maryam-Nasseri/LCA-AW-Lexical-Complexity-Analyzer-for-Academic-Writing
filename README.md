# LCA-AW-Lexical-Complexity-Analyzer-for-Academic-Writing

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2537862.svg)](https://doi.org/10.5281/zenodo.2537862)

LCA-AW (Lexical Complexity Analyzer for Academic Writing); version 2.1. 

This code is a modified version of the LCA (lexical complexity analyzer, described in Lu, 2012). The modified version integrated the BAWE (British Academic Written English) corpus' word list, the bawe_list.txt, that is a list of most frequently-used academic writing words in linguistics-related disciplines and language studies. The BNC-British National Corpus (or an option to use ANC- American National Corpus,) and the BAWE word lists act as filters for calculating lexical sophistication indices (see Lu, 2012). LCA-AW, will be suitable for analysing lexical complexity of academic writing in linguistics-related disciplines.

This code works for Python 2 users only. To use the code with Python 3 versions, download the latest release version 2.2 from the 'releases' section ![GitHub release (latest by date)](https://img.shields.io/github/v/release/Maryam-Nasseri/LCA-AW-Lexical-Complexity-Analyzer-for-Academic-Writing) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4147000.svg)](https://doi.org/10.5281/zenodo.4147000)


**1- Copyright and Citation information:**

Copyright © 2019 Maryam Nasseri (University of Birmingham) and Xiaofei Lu (The Pennsylvania State University) 


**In-text citation:**
If you use LCA-AW in your research, please refer to it as "Lexical Complexity Analyzer for Academic Writing (LCA-AW, v 2.1, Nasseri & Lu, 2019), 
a modified version of the LCA (Lexical Complexity Analyzer, Lu, 2012)" in your text.

**Citing in references:**
Nasseri, M., & Lu, X. (2019).Lexical Complexity Analyzer for Academic Writing (LCA-AW,version 2.1). DOI: 10.5281/zenodo.2537862


The original LCA:
The original LCA Version 1.1 Released on February 12, 2013; Copyright (C) 2013 Xiaofei Lu
download the original LCA at http://www.personal.psu.edu/xxl13/download.html

Lu, Xiaofei (2012). The relationship of lexical richnes to the quality 
of ESL speakers' oral narratives. The Modern Language Journal, 96(2), 190-208. 


**2- GNU and free software:**
 
This program is free software; you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation; either version 2 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT 
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
details.

You should have received a copy of the GNU General Public License along with 
this program; if not, write to the Free Software Foundation, Inc., 59 Temple 
Place, Suite 330, Boston, MA  02111-1307  USA

        


**3- About LCA-AW:**

This tool computes the lexical complexity of English texts using 25 different 
lexical measures that are reported in the literature to be indicative and/or 
predictive of linguistic proficieny and/or development. 
Information on the measures can be found in Lu (2012, 2014). 
This tool uses frequency lists derived from the British National Corpus (BNC)
(with an option to change to the American National Corpus, ANC) as well as the BAWE word list
for Linguistics and Language Studies. These word lists act as filters to calculate lexical sophistication 
indices. As such, lexical sophistication will be calculated as the ones that do not appear 
in the top 2000 most frequently-used words in the BNC 
(or ANC) nor in the 100 most frequently-used academic words in the BAWE word list.


**4- Running the tool**

**4.1 Input files:** All input files must be POS-tagged and lemmatized first and 
must be in the following format (see files in the samples folder for 
examples). The file should contain a minumum of 50 words. 

lemma_pos lemma_pos lemma_pos ...

or 

lemma_pos
lemma_pos
lemma_pos

You can use any POS tagger and lemmatizer, as long as the Penn Treebank POS 
tagset is adopted and the input file is appropriately formatted. In Lu 
(2012), the following POS tagger and lemmaitzer were used:

The Stanford POS tagger: 
http://nlp.stanford.edu/software/tagger.shtml

MORPHA: 
http://www.informatics.susx.ac.uk/research/groups/nlp/carroll/morph.html

full information on how to install and use Stanford POS Tagger and Morpha and analyse your texts with LCA can be found in:
Lu (2014), Computational Methods for Corpus Annotation and Analysis, Springer Netherlands.

Notice: Although Tree Tagger can perform the tokenisation, tagging, and lemmatisation of all files with one command and at the same time, it can produce different token counts than the above-mentioned programmes, depending on the type of texts. If the Tree Tagger out put (.tt files) are formatted as

token	POStag	lemma

per line, you may need to tranform the file (to lemma_tag format) so that the LCA-AW takes every line as one token not one sentence. To transform the .tt file via the command line in Linux use:

awk '{print $3"_"$2}' TreeTaggerFile.txt > TreeTaggerFile_Reformatted.txt



**4.2 Analyzing a single file:** To get the lexical complexity of a single file, 
run the following from this directory. Replace input_file with the actual 
name of your input file and output_file with the desired name of your output 
file.

python lc.py input_file > output_file

e.g.,

python lc.py samples/1.lem > 1.lex

To use the American National Corpus (ANC) wordlist instead of the BNC wordlist
for lexical sophistication analysis, use the lc-anc.py script, e.g.,

python lc-anc.py samples/1.lem > 1-anc.lex

--to give the full path of the input and output files use the below command, which takes the input file 'sample.lem' and gives an output file of 'sample.lex':

python lc-anc.py ~/corpus/programmes/LCA-AW/sample.lem > ~/corpus/programmes/LCA-AW/sample.lex

**4.3 Analyzing multiple files:** To get the lexical complexity of two or more 
files within a single folder, run the following from this directory. Replace 
path_to_folder with the actual path to the folder that contains your files 
and output_file with the desired name of your output file. The folder should 
only contain the files you want to analyze. The name of the folder of input files should end with a slash /

python folder-lc.py path_to_folder > output_file

e.g.,

python folder-lc.py samples/ > samples.lex

To use the American National Corpus (ANC) wordlist instead of the BNC wordlist
for lexical sophistication analysis, use the folder-lc-anc.py script, e.g.,

python folder-lc-anc.py samples/ > samples-anc.lex

--to give the full path of the input and output files use the below command, which takes the input file 'samples' and gives an output file of 'outputsamples.lex' (you can check your results with the samples folder which contains two .lem files, and the output folder 'outputsamples.lex' inside the LCA-AW folder):

python folder-lc-anc.py ~/corpus/programmes/LCA-AW/samples/ > ~/corpus/programmes/LCA-AW/outputsamples.lex


**4.4 Using the output:** The output file is comma-delimited and can be loaded to 
excel and spss, or R directly for analysis.

**5- Report a problem**

If you run into any problems while using the analyzer you can contact me https://www.researchgate.net/profile/Maryam_Nasseri
