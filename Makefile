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

.PHONY: download
download:
ifeq ($(OS),Windows_NT)
	if not exist target mkdir target
else
	mkdir -p target
endif
	cd target && curl -O -J -L  "https://repo1.maven.org/maven2/org/cicirello/btpe-iterations/1.0.0/btpe-iterations-1.0.0-jar-with-dependencies.jar"

.PHONY: run
run:
	java -cp ${JARFILE} org.cicirello.experiments.btpe.CountIterationsBTPE > ${pathToDataFiles}/raw.txt

.PHONY: analyze
analyze:
	$(py) -m pip install --upgrade --user scipy
	$(py) -B src/main/python/analyze.py ${pathToDataFiles}/raw.txt > ${pathToDataFiles}/tables.tex
	$(py) -B src/main/python/findmax.py ${pathToDataFiles}/raw.txt > ${pathToDataFiles}/max.txt
