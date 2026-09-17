# NVIDIA DataDesigner — Synthetic Data Generation

This project demonstrates how to use **NVIDIA DataDesigner** to generate synthetic datasets using Large Language Models (LLMs).

The current example generates **10 short horror stories** using NVIDIA's **Nemotron 3.5 Lightning** model through the NVIDIA API and exports the generated dataset as a CSV file.

---

## Overview

The project uses the following workflow:

```text
Python Configuration
        ↓
NVIDIA DataDesigner
        ↓
NVIDIA API
        ↓
Nemotron 3.5 Lightning
        ↓
Generated Synthetic Data
        ↓
Dataset Profiling
        ↓
CSV Export
```

DataDesigner is responsible for building and executing the dataset-generation pipeline, while NVIDIA provides the hosted LLM used to generate the text.

---

## Technologies Used

* Python 3.14+
* uv
* NVIDIA DataDesigner
* NVIDIA API
* NVIDIA Nemotron 3.5 Lightning
* Jinja templating
* CSV

---

## Project Setup

### 1. Clone the Repository

Clone the project repository:

```powershell
git clone <YOUR_REPOSITORY_URL>
cd DataDesigner
```

If the repository is already available locally, simply navigate into the project directory:

```powershell
cd C:\Users\kaush\DataDesigner
```

---

## 2. Install Dependencies

This project uses **uv** for Python environment and dependency management.

Make sure `uv` is installed:

```powershell
uv --version
```

Then install all project dependencies:

```powershell
uv sync --all-packages
```

This creates/uses the project's virtual environment and installs the required dependencies.

Activate the environment if required:

```powershell
.venv\Scripts\Activate.ps1
```

You should see a prompt similar to:

```text
(data-designer-workspace) PS C:\Users\...\DataDesigner>
```

---

# NVIDIA API Setup

DataDesigner needs access to an LLM provider in order to generate text.

In this project, **NVIDIA is the provider** and the **NVIDIA API is the interface used to communicate with the hosted model**.

The project uses:

```text
Provider:
NVIDIA

API endpoint:
https://integrate.api.nvidia.com/v1

Model:
nvidia/nemotron-3.5-lightning-30b-a3b
```

The API uses an API key for authentication.

---

## 3. Get an NVIDIA API Key

Create an NVIDIA API key through NVIDIA's API Catalog / Build platform.

Do **not** put the API key directly inside the Python source code.

Do not commit the key to Git.

---

## 4. Configure the API Key

DataDesigner expects the environment variable:

```text
NVIDIA_API_KEY
```

For PowerShell, configure it for the current terminal session:

```powershell
$env:NVIDIA_API_KEY = "YOUR_NVIDIA_API_KEY"
```

You can verify that the variable exists without printing the actual secret:

```powershell
if ($env:NVIDIA_API_KEY) {
    Write-Host "NVIDIA_API_KEY is configured"
} else {
    Write-Host "NVIDIA_API_KEY is NOT configured"
}
```

Expected output:

```text
NVIDIA_API_KEY is configured
```

### Security

Never do this:

```powershell
Write-Host $env:NVIDIA_API_KEY
```

Never commit the API key to GitHub.

Never put the API key directly into:

```python
api_key = "..."
```

Use the environment variable instead.

---

# DataDesigner Provider Configuration

DataDesigner uses a provider configuration similar to:

```yaml
providers:
  - name: nvidia
    endpoint: https://integrate.api.nvidia.com/v1
    provider_type: openai
    api_key: NVIDIA_API_KEY
```

### Why is `provider_type` set to `openai`?

NVIDIA provides an **OpenAI-compatible API interface**.

This does **not** mean that the model is provided by OpenAI.

The configuration means that DataDesigner can communicate with NVIDIA's endpoint using the OpenAI-compatible API format.

The relationship is:

```text
Provider
    ↓
NVIDIA

API endpoint
    ↓
https://integrate.api.nvidia.com/v1

API key
    ↓
NVIDIA_API_KEY

Model
    ↓
nvidia/nemotron-3.5-lightning-30b-a3b
```

---

# Verify the DataDesigner Configuration

You can inspect the configured providers with:

```powershell
uv run data-designer config providers
```

The NVIDIA provider should be present.

---

# Test Configuration

The project uses a Python configuration file:

```text
test_config.py
```

The configuration exposes a function called:

```python
load_config_builder()
```

This allows the DataDesigner CLI to load the configuration.

---

# Horror Story Dataset

The current configuration generates a single column:

```text
story
```

The column is generated using an LLM.

Example configuration:

```python
import data_designer.config as dd


def load_config_builder() -> dd.DataDesignerConfigBuilder:
    config_builder = dd.DataDesignerConfigBuilder()

    config_builder.add_column(
        dd.LLMTextColumnConfig(
            name="story",
            model_alias="nvidia-text",
            prompt=(
                "Generate one original short horror story. "
                "The story must be between 100 and 150 words. "
                "Build suspense and end with an unsettling twist. "
                "Output ONLY the story itself. "
                "Do NOT explain your reasoning. "
                "Do NOT analyze the request. "
                "Do NOT include a plan, outline, word count, commentary, "
                "or phrases such as 'Let's think step by step'. "
                "Do NOT include a title. "
                "Start directly with the first sentence of the story "
                "and end with the final sentence of the story."
            ),
        )
    )

    return config_builder
```

---

# Understanding the Configuration

## `DataDesignerConfigBuilder`

```python
config_builder = dd.DataDesignerConfigBuilder()
```

This creates the configuration builder used to define the dataset.

Columns are then added to this builder.

---

## `LLMTextColumnConfig`

```python
dd.LLMTextColumnConfig(...)
```

This tells DataDesigner that the column should be generated using an LLM.

In this example:

```python
name="story"
```

creates the dataset column:

```text
story
```

---

## Model Alias

The configuration uses:

```python
model_alias="nvidia-text"
```

The alias points to the configured NVIDIA model.

Conceptually:

```text
nvidia-text
      ↓
NVIDIA provider
      ↓
Nemotron 3.5 Lightning
```

Using an alias makes it possible to reference the configured model without repeatedly specifying the complete model configuration.

---

# Validate the Configuration

Before generating data, validate the configuration:

```powershell
uv run data-designer validate test_config.py
```

Expected result:

```text
✅ Validation passed
```

Validation checks that the DataDesigner configuration is valid before the generation pipeline is executed.

---

# Check Model Connectivity

You can also verify that the configured model and provider are reachable:

```powershell
uv run data-designer check-models test_config.py
```

A successful result looks similar to:

```text
🩺 Running health checks for models...

Checking 'nvidia/nemotron-3.5-lightning-30b-a3b'
in provider named 'nvidia'

✅ Passed!

✅ All models and tools responded successfully
```

This confirms that:

* the provider configuration is available
* the API key is being recognized
* the model can be reached
* the model can successfully respond to a generation request

---

# Generate the Dataset

Generate 10 horror stories with:

```powershell
uv run data-designer create test_config.py `
    --num-records 10 `
    --dataset-name horror_stories `
    --output-format csv
```

Or as a single line:

```powershell
uv run data-designer create test_config.py --num-records 10 --dataset-name horror_stories --output-format csv
```

---

# Generated Dataset

DataDesigner creates the dataset under:

```text
artifacts/
└── horror_stories/
    └── horror_stories.csv
```

The CSV contains:

```text
story
```

with 10 generated records.

---

# What Happens During Generation?

When the `create` command is executed, DataDesigner performs several stages.

### 1. Load Configuration

```text
test_config.py
        ↓
load_config_builder()
```

### 2. Validate Configuration

```text
Configuration
      ↓
Validation
```

### 3. Resolve Model

```text
nvidia-text
      ↓
NVIDIA provider
      ↓
Nemotron model
```

### 4. Check Model Health

DataDesigner sends a small request to verify that the model responds successfully.

### 5. Generate Records

For 10 records:

```text
Record 1 → LLM
Record 2 → LLM
Record 3 → LLM
...
Record 10 → LLM
```

### 6. Profile Dataset

DataDesigner calculates dataset statistics such as:

* number of records
* number of columns
* unique values
* token statistics
* completion statistics

### 7. Export Dataset

The generated data is finally written to:

```text
horror_stories.csv
```

---

# API Request Flow

The complete communication can be understood as:

```text
Your Python configuration
          ↓
     DataDesigner
          ↓
     NVIDIA API
          ↓
    Nemotron Model
          ↓
   Generated response
          ↓
     DataDesigner
          ↓
       CSV file
```

The API key is used for authentication.

The model performs the actual text generation.

DataDesigner manages the dataset-generation workflow.

---

# Provider vs API

These terms are easy to confuse.

### Provider

The provider is the service that gives access to the model.

In this project:

```text
Provider = NVIDIA
```

### API

The API is the interface through which the application communicates with that provider.

In this project:

```text
API = NVIDIA's OpenAI-compatible API
```

### Model

The model is the actual AI system generating the text.

```text
Model = Nemotron 3.5 Lightning
```

So:

```text
NVIDIA
  ↓
Provider

NVIDIA API
  ↓
Communication interface

Nemotron
  ↓
LLM generating the text
```

---

# Using This Project on Another Machine

Someone else who wants to use this project should:

### 1. Clone the repository

```powershell
git clone <YOUR_REPOSITORY_URL>
cd DataDesigner
```

### 2. Install uv

Verify:

```powershell
uv --version
```

### 3. Install project dependencies

```powershell
uv sync --all-packages
```

### 4. Obtain their own NVIDIA API key

Each user should use their **own API key**.

The project owner should never distribute their private API key.

### 5. Configure the environment variable

```powershell
$env:NVIDIA_API_KEY = "THEIR_NVIDIA_API_KEY"
```

### 6. Verify the key exists

```powershell
if ($env:NVIDIA_API_KEY) {
    Write-Host "NVIDIA_API_KEY is configured"
} else {
    Write-Host "NVIDIA_API_KEY is NOT configured"
}
```

### 7. Validate the configuration

```powershell
uv run data-designer validate test_config.py
```

### 8. Check model connectivity

```powershell
uv run data-designer check-models test_config.py
```

### 9. Generate the dataset

```powershell
uv run data-designer create test_config.py --num-records 10 --dataset-name horror_stories --output-format csv
```

The generated CSV will appear under:

```text
artifacts/horror_stories/horror_stories.csv
```

---

# Changing the Number of Stories

The number of records is controlled from the command line.

For 100 stories:

```powershell
uv run data-designer create test_config.py --num-records 100 --dataset-name horror_stories --output-format csv
```

For 1,000 stories:

```powershell
uv run data-designer create test_config.py --num-records 1000 --dataset-name horror_stories --output-format csv
```

The configuration does not need to be changed just to change the number of records.

---

# Changing the Output Format

DataDesigner supports different output formats.

### CSV

```powershell
--output-format csv
```

### JSONL

```powershell
--output-format jsonl
```

### Parquet

```powershell
--output-format parquet
```

For example:

```powershell
uv run data-designer create test_config.py --num-records 100 --dataset-name horror_stories --output-format parquet
```

---

# Customizing the Stories

The prompt in `test_config.py` controls the type of content generated.

For example, the prompt can be changed to request:

```text
Psychological horror
Supernatural horror
Ghost stories
Cosmic horror
Horror mystery
Horror set in an abandoned hospital
Horror set in a forest
Horror involving an AI system
```

For example:

```python
prompt=(
    "Generate one original short psychological horror story. "
    "Keep it between 100 and 150 words. "
    "Build suspense and end with an unsettling twist. "
    "Output only the story."
)
```

The configuration can therefore be reused to create many different synthetic text datasets.

---

# Important Considerations

## API Costs / Usage

Generating data through a hosted LLM API consumes model/API usage.

Larger datasets require more model requests and tokens.

For example:

```text
10 stories
    ↓
10 generation requests

1,000 stories
    ↓
approximately 1,000 generation tasks
```

Actual usage depends on the model configuration and generated content.

---

## Generated Data Should Be Reviewed

LLM-generated synthetic data can contain:

* repetitive patterns
* unexpected formatting
* irrelevant content
* factual errors
* malformed responses
* outputs that don't follow the prompt exactly

Therefore, generated datasets should be inspected and validated before being used in production or downstream ML pipelines.

---

## Never Commit API Keys

Make sure secrets are excluded from version control.

For example, `.env` files containing credentials should not be committed.

A project should contain configuration such as:

```text
NVIDIA_API_KEY
```

but never the actual secret value.

---

# Future Improvements

This project can be extended to generate richer synthetic datasets.

For example:

```text
story_id
title
genre
setting
character
story
ending_type
```

A more advanced pipeline could look like:

```text
genre
  ↓
setting
  ↓
character
  ↓
story
  ↓
ending
```

DataDesigner can use relationships between generated columns, allowing later columns to reference values generated earlier in the dataset.

This makes it possible to construct more structured and realistic synthetic datasets instead of generating isolated pieces of text.

---

# Summary

This project demonstrates a basic **LLM-powered synthetic data generation workflow using NVIDIA DataDesigner**.

The main components are:

```text
uv
 ↓
Python
 ↓
DataDesigner
 ↓
NVIDIA API
 ↓
Nemotron
 ↓
Synthetic Dataset
 ↓
CSV
```

The current example generates:

```text
10 short horror stories
```

using an NVIDIA-hosted Nemotron model.

The project can be reused by other developers by cloning the repository, installing dependencies with `uv`, configuring their own `NVIDIA_API_KEY`, validating the DataDesigner configuration, checking model connectivity, and running the dataset-generation command.
