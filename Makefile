MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MKFILE_DIR := $(dir $(MKFILE_PATH))
FUNCTIONS := ./functions

all: $(FUNCTIONS)/*
	-@for f in $^ ; do cd "$(MKFILE_DIR)/$${f}" && make && cp output.ext2 ../../output/`basename "$${f}"`.ext2; done

test:
	cd tests/test_rw/ && make && cp output.ext2 ../../output/test_rw.ext2
	cd tests/test_createfaceted/ && make && cp output.ext2 ../../output/test_createfaceted.ext2
	cd tests/test_createfaceted2/ && make && cp output.ext2 ../../output/test_createfaceted2.ext2
	cd tests/test_delete/ && make && cp output.ext2 ../../output/test_delete.ext2
	cd tests/test_gate/ && make && cp output.ext2 ../../output/test_gate.ext2


