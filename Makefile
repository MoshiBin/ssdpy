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
	python3 -m build .
	twine upload dist/*
