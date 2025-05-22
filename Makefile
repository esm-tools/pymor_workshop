fake-data:
	python ./scripts/create-fake-data.py \
		-y ./synthetic-data/aux-files-data-skeletons.yaml \
		-o ./synthetic-data/aux-files/
	python ./scripts/create-fake-data.py \
		-y ./synthetic-data/combining-variables-data-skeletons.yaml \
		-o ./synthetic-data/combining-variables/
