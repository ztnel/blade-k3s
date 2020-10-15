.PHONY: all
all : setup flash

.PHONY: setup
setup: ## install packages and init and sync submodules
	./bin/setup

.PHONY: flash
flash: ## flash compute module eMMC with specified OS image
	@if [[ "$(img)" -ne 0 ]]; then exit 1; fi
	./bin/flash_emmc $(img)

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