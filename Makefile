.PHONY: clean
clean:
	rm -rf dist \
		   ssdpy/__pycache__ \
		   ssdpy/*.pyc \
		   ssdpy.egg-info \
		   tests/*.pyc \
		   build


.PHONY: release
release: clean
	python setup.py sdist bdist_wheel
	twine upload dist/*
