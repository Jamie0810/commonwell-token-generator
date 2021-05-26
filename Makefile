clean:
	rm -vrf .eggs .pytest_cache ./*/__pycache__ ./build ./dist *.pyc *.tgz *.egg-info

install:
	pip3 install setuptools pytest
	python3 setup.py install

example:
	python3 examples/main.py

test:
	python3 setup.py test