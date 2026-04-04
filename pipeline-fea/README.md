# 🚀 Nastran → SysML v2 Pipeline (Baseline Contract Version)

This is a deterministic, architecture-driven pipeline for:

```text
simple-example.bdf
    ↓
simple-example_decimated.json
    ↓
simple-example_exchange.json
    ↓
simple-example_model.sysml           (non-flattened)
    ↓
simple-example_presentation.sysml    (flattened / diagram-friendly)
```

It is intentionally constrained to the two baseline contracts:

- Nastran Extraction Schema
- Nastran Simulation Schema

---

## Files

- `nastran_decimator.py`
- `nastran_exchange_create.py`
- `nastran_exchange_to_sysml_nonflattened.py`
- `nastran_exchange_to_sysml_flattened.py`
- `README.md`

---

## What each script does

### 1) `nastran_decimator.py`

Reads a Nastran `.bdf` or `.dat` file and emits a compact decimated JSON with:

- `executiveControl`
- `caseControl`
- `bulkDataSummary`
- `fileSummary`

This script intentionally drops:

- full GRID table contents  
- element connectivity  
- repeated coordinate/orientation numerics  
- continuation-heavy raw property formatting  
- raw bulk-data deck text  

Additional behavior:
- captures original input filename and propagates it through the pipeline

Default output file:

```text
<source_bdf_stem>_decimated.json
```

Example:

```bash
python nastran_decimator.py simple-example.bdf
```

Produces:

```text
simple-example_decimated.json
```

---

### 2) `nastran_exchange_create.py`

Reads the decimated JSON and creates a normalized exchange / simulation JSON with:

- `simulationIdentity`
- `solver`
- `files`
- `executiveControl`
- `caseControl`
- `bulkData`
- `results`
- `provenance`

This script implements the **Normalized Exchange Layer**, which:

- converts extraction output into a canonical system-of-record representation  
- preserves source filename and provenance  
- decouples parsing logic from SysML generation  

Default output file:

```text
<source_bdf_stem>_exchange.json
```

Example:

```bash
python nastran_exchange_create.py simple-example_decimated.json
```

Produces:

```text
simple-example_exchange.json
```

---

### 3) `nastran_exchange_to_sysml_nonflattened.py`

Reads the exchange JSON and produces a deterministic **SysML v2 structured model**.

Characteristics:

- includes `part def` (types)
- includes typed `part : Type` usages
- preserves formal MBSE structure
- separates definitions from instances

This version is best for:

- MBSE tools
- formal system modeling
- architecture correctness

Default output file:

```text
<source_bdf_stem>_model.sysml
```

Example:

```bash
python nastran_exchange_to_sysml_nonflattened.py simple-example_exchange.json
```

---

### 4) `nastran_exchange_to_sysml_flattened.py`

Reads the exchange JSON and produces a **flattened, presentation-oriented SysML model**.

Characteristics:

- removes visible `part def` separation
- emits one visible block per object
- assigns values directly on the block
- uses original filename stem as the **top-level part name**
- improves readability in SysIDE (VS Code)

Formatting fixes included:

- `sourceFiles = test.bdf` (not JSON array)
- `elementCountsByType = CQUAD4=10` (not escaped JSON)

This version is best for:

- diagrams
- presentations
- AIAA figures

Default output file:

```text
<source_bdf_stem>_presentation.sysml
```

Example:

```bash
python nastran_exchange_to_sysml_flattened.py simple-example_exchange.json
```

---

## Full pipeline example

```bash
python nastran_decimator.py                         test.bdf
python nastran_exchange_create.py                   test_decimated.json
python nastran_exchange_to_sysml_nonflattened.py    test_exchange.json
python nastran_exchange_to_sysml_flattened.py       test_exchange.json

python nastran_decimator.py                         simple-example.bdf
python nastran_exchange_create.py                   simple-example_decimated.json
python nastran_exchange_to_sysml_nonflattened.py    simple-example_exchange.json
python nastran_exchange_to_sysml_flattened.py       simple-example_exchange.json
```

---

## Naming convention

The pipeline always uses the **original BDF filename stem**:

- `simple-example.bdf`
- `simple-example_decimated.json`
- `simple-example_exchange.json`
- `simple-example_model.sysml`
- `simple-example_presentation.sysml`

The flattened model also uses the filename stem as the **top-level SysML part name**.

---

## System Architecture Perspective

This pipeline implements a three-stage architecture:

1. Extraction / Decimation  
2. Exchange-Layer Normalization  
3. Deterministic Model Synthesis  

The key architectural contribution is the **Normalized Exchange Layer**, which:

- acts as a stable intermediate representation (IR)  
- enables deterministic transformation  
- preserves traceability from source file to SysML  
- supports extension to additional simulation domains  

---

## Design principles

- deterministic  
- schema-disciplined  
- MBSE abstraction level  
- traceable (filename + provenance propagation)  
- no mesh reconstruction  
- no LLM dependency  

---

## Important limitation

This is a **baseline-contract implementation**.

It intentionally does not include:

- detailed property summaries  
- explicit load/constraint expansion  
- results extraction  
- mesh reconstruction  

This ensures the pipeline remains:

- deterministic  
- auditable  
- architecture-focused  

---

## Future extension ideas

- property summaries (PBAR, PSHELL, etc.)  
- load and constraint expansion  
- results ingestion (.f06, .op2)  
- multi-domain support (CFD, thermal, EM)  
- SysML semantic enrichment  

---

## License

MIT (or your preferred license)
