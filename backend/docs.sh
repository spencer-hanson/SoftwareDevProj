#!/bin/bash

mkdir -p docs
pydoc -w `find apis -name '*.py'`
mv *.html docs
