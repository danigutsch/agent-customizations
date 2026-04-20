PYTHON ?= python3
PIPX ?= pipx
RUFF ?= ruff
PYRIGHT ?= pyright
TARGET_ROOT ?= $(CURDIR)
MANIFEST ?=
RUNTIME_AUTHORITY ?= user

.PHONY: check format lint lint-markdown typecheck validate-repo validate-plugins smoke-exports inspect-tool-files sync-user sync-workspace configure-global-ignore setup-mcp install-dev install-hooks hook-pre-commit

check: validate-repo validate-plugins smoke-exports lint typecheck

format:
	$(RUFF) format scripts

lint:
	$(RUFF) check scripts
	$(RUFF) format --check scripts

lint-markdown:
	npm run --silent lint:markdown

typecheck:
	$(PYRIGHT) scripts

validate-repo:
	$(PYTHON) scripts/validate_repo_files.py

validate-plugins:
	$(PYTHON) scripts/validate_plugin_bundles.py

smoke-exports:
	$(PYTHON) scripts/run_export_smoke_tests.py

inspect-tool-files:
	$(PYTHON) scripts/check_tool_file_versions.py --repo "$(TARGET_ROOT)"

sync-user:
	$(PYTHON) scripts/sync_copilot_exports.py --scope user

sync-workspace:
	$(PYTHON) scripts/sync_copilot_exports.py --scope workspace --runtime-authority "$(RUNTIME_AUTHORITY)" --target-root "$(TARGET_ROOT)"

configure-global-ignore:
	$(PYTHON) scripts/configure_global_copilot_gitignore.py --repo "$(TARGET_ROOT)"

setup-mcp:
	@if [ -n "$(MANIFEST)" ]; then \
		$(PYTHON) scripts/setup_copilot_mcp.py --manifest "$(MANIFEST)"; \
	else \
		$(PYTHON) scripts/setup_copilot_mcp.py; \
	fi

install-dev:
	@command -v $(PIPX) >/dev/null 2>&1 || { \
		echo "pipx is required for install-dev."; \
		echo "Install it first (for example: sudo apt-get install -y pipx) and ensure ~/.local/bin is on PATH."; \
		exit 1; \
	}
	@command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1 || { \
		echo "Node.js 20 or newer and npm are required for install-dev."; \
		echo "Install a current Node.js LTS release and ensure both 'node' and 'npm' are on PATH."; \
		exit 1; \
	}
	@node_major=$$(node -p 'Number(process.versions.node.split(".")[0])' 2>/dev/null) || { \
		echo "Unable to determine the installed Node.js version. Node.js 20 or newer is required for install-dev."; \
		exit 1; \
	}; \
	if [ "$$node_major" -lt 20 ]; then \
		echo "Node.js 20 or newer is required for install-dev (found $$(node -v))."; \
		echo "Please install a supported Node.js release before running 'make install-dev'."; \
		exit 1; \
	fi
	@if $(PIPX) list --short 2>/dev/null | grep -q '^ruff '; then \
		$(PIPX) upgrade ruff; \
	else \
		$(PIPX) install ruff; \
	fi
	@if $(PIPX) list --short 2>/dev/null | grep -q '^pyright '; then \
		$(PIPX) upgrade pyright; \
	else \
		$(PIPX) install pyright; \
	fi
	npm ci

install-hooks:
	git config core.hooksPath .githooks
	chmod +x .githooks/pre-commit

hook-pre-commit:
	$(PYTHON) scripts/run_pre_commit_checks.py
