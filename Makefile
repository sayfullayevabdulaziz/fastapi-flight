#!/usr/bin/make

include .env
export PYTHONPATH=:$(PWD)
export PYTHONPATH=:$(PWD)/app

run:
	cd app && /bin/bash -c "uvicorn main:app --reload"