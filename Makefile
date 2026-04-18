PYTHON ?= python3
RUFF ?= $(PYTHON) -m ruff
PYRIGHT ?= $(PYTHON) -m pyright
TARGET_ROOT ?= $(CURDIR)

.PHONY: check format lint typecheck validate-repo validate-plugins sync-user sync-workspace configure-global-ignore install-dev install-hooks hook-pre-commit

check: validate-repo validate-plugins lint typecheck

format:
	$(RUFF) format scripts

lint:
	$(RUFF) check scripts
	$(RUFF) format --check scripts

typecheck:
	$(PYRIGHT) scripts

validate-repo:
	$(PYTHON) scripts/validate_repo_files.py

validate-plugins:
	$(PYTHON) scripts/validate_plugin_bundles.py

sync-user:
	$(PYTHON) scripts/sync_copilot_exports.py --scope user

sync-workspace:
	$(PYTHON) scripts/sync_copilot_exports.py --scope workspace --target-root "$(TARGET_ROOT)"

configure-global-ignore:
	$(PYTHON) scripts/configure_global_copilot_gitignore.py --repo "$(TARGET_ROOT)"

install-dev:
	$(PYTHON) -m pip install --user --upgrade ruff pyright

install-hooks:
	git config core.hooksPath .githooks
	chmod +x .githooks/pre-commit

hook-pre-commit:
	$(PYTHON) scripts/run_pre_commit_checks.py
