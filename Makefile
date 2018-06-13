all:
	python newOthello.py
push:
	git add .
	git commit -m "Hello"
	git push
