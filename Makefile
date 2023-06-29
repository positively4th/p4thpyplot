.PHONY: requirements contrib

all: requirements contrib
	
requirements: 
	(python -m venv .venv && .venv/bin/python -m pip install --upgrade pip) \
	&& (source .venv/bin/activate && pip install -r requirements.txt)


contrib: 
	make -C contrib all

clean: 
	make -C contrib clean
	rm -rf .venv

