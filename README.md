# biopartsDB

HTML platform with a hand-picked selection of publications on biocircuit part libraries. Created by Felipe Xavier Buson at the [Wang Lab](https://wanglab.net/) at the University of Edinburgh. Will be active until this platform can be set up online.

Currently showed to work on:
Firefox
Google Chrome (with a few unaligned pixels)
Microsoft Edge (with a few unaligned pixels)

Only tested on Windows 10.
Necessary programs/packages:
* a web browser
* python 3
  * pandas
  * matplotlib
  * regex
  * dnaplotlib
  * bs4 (BeautifulSoup)
## Browsing

To browse through the html, you need only to download the repository contents into a folder and click on the "Home.html" file in database/browsing.

The "database" folder contains the pages, table data, and javascript code to make a browser-readable product.

The "edits" folder contains a python script that creates new content for the database, based on an input csv table.

Editing existing parts automatically is currently not implemented.

## Adding new parts

The addition of new parts is a process to be carried out by a dedicated curator. The size and scope of the database were chosen precisely for this purpose. Thus, users will not be required to know how to add parts, but this tutorial is here for suggestions to be made on the design of the project, and to make things as easy as possible for the curator.

To simulate this process, fill the columns on "new_parts.csv" to the desired data according to the column legends and run the python program (made and tested with python 3.7) "new_parts.py". Alternatively look at the "all_parts.csv" file for reference of how the tables should be filled

Currently you will still need to empty the "new_parts.csv" file after running the program, leaving only the column names.

*Do not add semicolons (;) in any cell of the table.*

### Updating parts

If the lines put into "new_parts.csv" have a code that is already used in the database, the python script will overwrite the data for that part, and keep the current part description. Everything else that is manual (extra references/links) is still reset every time a part page is updated.

**Column legends**:

* **Name**:

Complex Identification for the part. Does not have to be unique.

Example: L-arabinose inducible promoter

* **Code**:

Simple identification for database referencing. This is what defines file names, so codes have to be unique (redundancy is checked on part creation).

Still, it would be good for it to have some meaning.

Do not use characters that couldn't be in file names. (<>:"/\|?*)

Example: PBAD

* **Type**:

Part type (see the "BrowsebyType.html" page) based on its molecular role in gene expression. Currently using plurals, but this may change to "Type:" in singular for consistency.

Current sets: Constitutive Promoters, Regulated Promoters, RBS, Terminators, Insulators, Riboregulators, CRISPR, Origins of Replication, Degradation Tags, Post-Translational (fusion and cleavage), Recombinases.

* **DR**:

Dynamic range achieved in part characterization. Adimensional.
(For dynamic behaviour. Fill with - if not applicable)

* **n**:

Hill number achieved in part characterization. Adimensional.
(For dynamic behaviour. Fill with - if not applicable)

* **High**:

Maximal expression achieved by part device. Can also represent the absolute value for parts with non-dynamic behaviour (e.g. Terminator and RBS strength, Plasmid copy number, Intein splicing efficiency)
(Fill with - if not applicable, as is the case with insulators)

* **Low**:

Minimal expression achieved by part device.
(Fill with - if not applicable)

* **Unit**:

Unit used for measurement of High/Low values.
(Fill with - if not applicable)

* **Km**:

Amount of input (regulator, be it a protein, RNA or others) necessary for half-maximal expression.
(For dynamic behaviour. Fill with - if not applicable)

* **Km Unit**:

Unit used for Km value. Will be specific for which kind of input is necessary for dynamic behaviour.
(Fill with - if not applicable)

* **Construct**:

Sequence of parts that compose the circuit where the part was characterized.

Must follow the structure: "<part 1 type>:<part 1 name>,<part 2 type>:<part 2 name>".

Each part should be represented with its type (as in dnaplotlib) and name (any), separated by a colon.

Different plasmids should be separated by //.

There is currently no implementation of inverted parts or regulatory signs.

Example: Promoter:Plux,RBS:B0034,CDS:sfGFP,Terminator:B0015//Promoter:J23101,RBS:B0030,CDS:LuxR,Terminator:B0010

Relevant dnaplotlib part types: Promoter, CDS, RBS, Terminator, Ribozyme, Ribonuclease, ProteinStability, Protease, Scar, Empty_Space, Spacer, Origin, Operator, Insulator

* **Function**:

Part function (see the "BrowsebyFunction.html" page) based on the role it serves in a genetic circuit. May change to "Function:" in the future.

Current functions: Hardwire, Input, Buffer, NOT, AND, Insulation, Vector, QS (communication), Memory, Output.

* **Regulator**:

Regulator molecule name (if applicable). This is only for added information and won't mess up code.

Example: AraC

* **Reg Type**:

Which type of regulation the dynamics of a part is based on. This is only for added information and won't mess up code.

Examples: Activation, Repression, Dual

* **Lab**:

Usually the name of the publication's PI.

* **Publication**:

Reference for the publication where the part is characterized. Requires a certain structure with the publication year after the abbreviated author names, followed by a dot.

Example: Wang, B., Barahona, M. and Buck, M., 2013. A modular cell-based biosensor using engineered genetic logic circuits to detect and integrate multiple environmental signals. Biosensors and Bioelectronics, 40(1), pp.368-376.

* **doi**:

Link for the publication where the part is characterized.

* **Strain**:

Chassis in which the part was characterized. E. coli is assumed, as all parts in the database are for E. coli.

Examples: MG1655, TOP10, DH10B

* **Plasmid**:

Vector(s) on which the part was characterized.

Examples: pSB1C3, pGEM, custom names

* **ori**:

Origin(s) of replication of the characterization vector(s).

Examples: pSC101, p15A, ColE1

* **Resistance**:

Antibiotic(s) utilized in the characterization. Presently abbreviations are used.

Examples: Kan, Spec, Amp, Clo, Tet

* **Keywords**:

List of keywords to be read by the search engine. No format is enforced.

* **Sequences**:

Every column after keywords (column 23 onwards) is reserved for sequences. They must follow a defined structure, with the sequence name followed by a colon and the part's seuquence.

Example: B0032:tcacacaggaaag

### 'To do' pages

- Help File

### 'To do' content

- Parts descriptions
- Sequence Annotation
- BLAST functionality
