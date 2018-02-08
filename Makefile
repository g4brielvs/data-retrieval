
create: $(SOURCE)
	python create_tags.py -s $(SOURCE)

check: $(SOURCE) $(DESTINATION)
	python check.py -s $(SOURCE)lau2_hours-select/ -d $(DESTINATION)lau2_hours-select/
	python check.py -s $(SOURCE)lau2_hours-avg-select/ -d $(DESTINATION)lau2_hours-avg-select/
	python check.py -s $(SOURCE)lau2_days-select/ -d $(DESTINATION)lau2_days-select/
	python check.py -s $(SOURCE)lau2_days-avg-select/ -d $(DESTINATION)lau2_days-avg-select/
