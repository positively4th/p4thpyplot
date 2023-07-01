all = p4thpymisc 

.PHONY: $(all)

all: $(all)

p4thpymisc: 
	(git clone git@github.com:positively4th/p4thpymisc.git || echo) \
	&& ([ -f "p4thpymisc/Makefile" ] && make -C p4thpymisc || echo)

clean: 
	rm -rf $(all)


