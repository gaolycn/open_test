# Makefile for thrift interface files
# Now ONLY support generating finance thrift interface
#
# If you want to use this file, you can put *.thrift file in
# this directory and write its make rule. Or you can write a
# general make rule if all *.thrift files already exist.

TARGETS=finance

all: $(TARGETS)

finance: finance.thrift
	-rm -r finance

	thrift --gen py finance.thrift
	cp -r gen-py/finance .
	rm -r gen-py

.PHONY:clean
clean:
	-rm -r $(TARGETS)
