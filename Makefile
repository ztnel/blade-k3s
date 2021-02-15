include .env
export $(shell sed 's/=.*//' .env)

.PHONY: all
all : setup flash

.PHONY: setup
setup: ## install packages, init and sync submodules, fetch and extract latest hypriotOS img
	./bin/setup

.PHONY: flash
flash: ## flash compute module eMMC with latest hypriotOS img
	./bin/flash_emmc

.PHONY: clean
clean: ## clean build artifacts
	@rm -rv build

.PHONY: help	
help:
	@echo Usage:
	@echo "  make [target]"
	@echo
	@echo Targets:
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "  %-30s %s\n", $$1, $$NF \
		 }' $(MAKEFILE_LIST)
