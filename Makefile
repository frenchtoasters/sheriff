CONDA_INSTALLER=Miniconda3-latest-Linux-x86_64.sh
CONDA_PREFIX?=$(HOME)/miniconda3
ENV_NAME=sheriff-bot

.PHONY: all install_conda create_env activate_env unit-test bdd test

all: install_conda create_env

install_conda:
	@if [ ! -d "$(CONDA_PREFIX)" ]; then \
		echo "🔧 Installing Miniconda..."; \
		curl -LO https://repo.anaconda.com/miniconda/$(CONDA_INSTALLER); \
		bash $(CONDA_INSTALLER) -b -p $(CONDA_PREFIX); \
		rm $(CONDA_INSTALLER); \
	else \
		echo "✅ Miniconda already installed at $(CONDA_PREFIX)"; \
	fi

create_env:
	@echo "📦 Creating conda environment '$(ENV_NAME)'..."
	$(CONDA_PREFIX)/bin/conda env create -f environment.yml || echo "✅ Environment already exists."

activate_env:
	@echo "🔬 To activate the environment, run:"
	@echo "source $(CONDA_PREFIX)/bin/activate $(ENV_NAME)"

# Run unit tests with pytest
unit-test:
	@echo "Running pytest unit tests..."
	pytest -v

# Run BDD tests with behave
bdd:
	@echo "Running behave BDD tests..."
	behave tests/features

# Run both pytest and behave tests
test: unit-test bdd
	@echo "All tests completed successfully."

.PHONY: boostrap-cluster
bootstrap-cluster:
	@echo "🔧 Bootstrapping kubernetes cluster..."
	./hack/boostrap_cluster.sh
