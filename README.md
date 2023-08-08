# btpe-iterations

Copyright &copy; 2023 Vincent A. Cicirello

This repository contains code to reproduce the experiments, and analysis of 
experimental data, from the following paper:

> Vincent A. Cicirello. 2023. An Analysis of an Open Source Binomial Random Variate Generation Algorithm, *Engineering Proceedings*, Accepted pending publication.

| __Related Publication__ |  |
| :--- | :--- |
| __License__ | [![GitHub](https://img.shields.io/github/license/cicirello/cycle-mutation-experiments)](LICENSE) |
| __Packages and Releases__ |  |

## Dependencies

The experiments depend upon the following libraries, and in some cases this research has 
also contributed to these libraries:
* [&rho;&mu;](https://rho-mu.cicirello.org)
* [org.cicirello.core](https://core.cicirello.org)

## Requirements to Build and Run the Experiments

To build and run the experiments on your own machine, you will need the following:
* __JDK 17__: I used OpenJDK 17, but other distributions should be fine. 
* __Apache Maven__: In the root of the repository, there is a `pom.xml` 
  for building the Java programs for the experiments. Using this `pom.xml`, 
  Maven will take care of downloading the exact version of 
  [&rho;&mu;](https://rho-mu.cicirello.org) (release 3.1.1) and its dependency 
  that were used in the experiments. 
* __Python 3__: The repository contains Python programs that were used to 
  process the raw data for the paper. If you want to run the Python programs, 
  you will need Python 3. 
* __Make__: The repository contains a Makefile to simplify running the build, 
  running the experiment's Java program, and running the Python program to 
  analyze the data. If you are familiar with using the Maven build tool, 
  and running Python programs, then you can just run these directly, although 
  the Makefile may be useful to see the specific commands needed.

## Building the Java Programs (Option 1)

The source code of the Java programs implementing the experiments
is in the [src/main/java](src/main/java) directory.  You can build the experiment 
programs in one of the following ways.

__Using Maven__: Execute the following from the root of the
repository.

```shell
mvn clean package
```

__Using Make__: Or, you can execute the following from the root
of the repository.

```shell
make build
```

## Running the Experiments

If you just want to inspect the data from my runs, then you can find that output
in the [/data](data) directory. If you instead want to run the experiments yourself,
you must first either follow the build instructions or download a prebuilt jar (see above
sections). Once the jar of the experiments is either built or downloaded, you can then run 
the experiments with the following executed at the root of the repository:

```shell
make run
```

If you don't want to overwrite my original data files, then first change the variable
`pathToDataFiles` in the `Makefile` before running the above command.

## Analyzing the Experimental Data

To run the Python program that I used to process the raw data,  
and generate the tables of the paper (as well as additional tables
not used in the paper), you need Python 3 installed. The source 
code of the Python programs is found in the [src/main/python](src/main/python) 
directory.  To run the analysis, execute the following at the root of the 
repository:

```shell
make analyze
```

If you don't want to overwrite my original data files, and tables, then change the 
variable `pathToDataFiles` in the `Makefile` before running the above command.

This will analyze the data from the [/data](data) directory. It will also 
generate the tables, etc in that directory. This make command will also take
care of installing any required Python packages if you don't already have them
installed.

## Other Files in the Repository

There are a few other files, potentially of interest, in the repository,
which include:
* `system-stats.txt`: This file contains details of the system I 
  used to run the experiments, such as operating system, processor 
  specs, Java JDK and VM. It is in the [/data](data) directory.

## License

The code to replicate the experiments from the paper, as well as the
&rho;&mu; library is licensed under the [GNU General Public License 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
