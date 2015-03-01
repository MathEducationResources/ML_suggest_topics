## help: list all available commands
help: Makefile
	@sed -n 's/##//p' $<

.PHONY: all clean
.DELETE_ON_ERROR:
.SECONDARY:

## all: Adds suggested topic to all json files
all: 
	python suggest_topic.py

## clean: Removes all intermediate files
clean:
	rm vocabulary.csv
	rm topics.csv
	rm X_data.csv
	rm Y_data.csv
	rm classifier.bin

## vocabulary.csv: generates list of (stemmed) vocabulary in all questions
## topics.csv: generates list of all topics in all questions
vocabulary.csv topics.csv: make_vocabulary.py
	python $<

## X_data.csv: generates feature vectors, for each question
## Y_data.csv: generates label vectors, for each question
X_data.csv Y_data.csv: make_X_Y.py vocabulary.csv topics.csv
	python $<

## classifier.bin: generates fitted classifier (pickle file)
classifier.bin: fit_model.py X_data.csv Y_data.csv
	python $<