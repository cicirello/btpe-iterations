ifeq ($(OS),Windows_NT)
	py = "python"
else
	py = "python3"
endif

JARFILE = "target/btpe-iterations-1.0.0-jar-with-dependencies.jar"
pathToDataFiles = "data"

.PHONY: build
build:
	mvn clean package

.PHONY: run
run:
	java -cp ${JARFILE} org.cicirello.experiments.btpe.CountIterationsBTPE > ${pathToDataFiles}/raw.txt

.PHONY: analyze
analyze:
	$(py) -m pip install --upgrade --user scipy
	$(py) -B src/main/python/analyze.py ${pathToDataFiles}/raw.txt > ${pathToDataFiles}/tables.tex
