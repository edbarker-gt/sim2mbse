# Formal Nastran Parsing Contract

## Purpose

This contract defines the required parsing behavior for any LLM-generated or hand-written parser used in the Nastran → decimated JSON → exchange JSON → SysML pipeline.

It applies specifically to the front-end parsing layer and must be followed before any decimation, normalization, or model generation logic is applied.

---

## 1. Source Language Authority

The parser shall treat the input as a Nastran input deck and shall conform, to the extent required by this pipeline, to the conventions defined by:

- MSC Nastran Quick Reference Guide
- NASA Nastran User Guide
- NX Nastran documentation (secondary reference)

The parser must not invent syntax, reinterpret card semantics, or mix parsing assumptions across incompatible field formats.

---

## 2. Section Structure

The parser shall recognize three major sections in the following order:

1. **Executive Control**
2. **Case Control**
3. **Bulk Data**

### Section delimiters

- `CEND` terminates Executive Control and begins Case Control
- `BEGIN BULK` terminates Case Control and begins Bulk Data
- `ENDDATA` terminates Bulk Data

### Required section state machine

```text
initial -> executive_control
executive_control --CEND--> case_control
case_control --BEGIN BULK--> bulk_data
bulk_data --ENDDATA--> end
```

The parser must maintain section state explicitly.

---

## 3. Comment Rules

- `$` begins a comment
- All text after `$` on a line shall be ignored
- Entire comment lines shall be discarded before semantic parsing

Example:

```text
SOL 101 $ linear static
```

must parse as:

```text
SOL 101
```

---

## 4. Field Format Rules

The parser must support the following field styles:

### 4.1 Free-field format
Detected when a line contains commas.

Example:

```text
MAT1,1,7.0E7,,0.3,0.1
```

Rule:
- Split on commas
- Trim whitespace around each field
- Preserve empty fields if position matters to the target parser logic

### 4.2 Plain whitespace executive/case lines
Detected when the stripped line contains multiple whitespace-separated tokens and is not clearly a fixed-width bulk-data record.

Examples:

```text
SOL 101
SUBCASE 1
```

Rule:
- Split on whitespace
- Use this mode before fixed-width slicing for executive and case control patterns

### 4.3 Fixed-width small-field format
Fallback mode for bulk-style records.

Rule:
- Slice line into 8-character fields
- Trim whitespace from each field
- Discard empty trailing fields

Example:

```text
GRID    1       0       0.0     0.0     0.0
```

parses as fields:

```text
["GRID", "1", "0", "0.0", "0.0", "0.0"]
```

---

## 5. Free-field vs Fixed-field Decision Tree

The parser shall apply the following decision tree **in order**:

### Decision tree

1. Strip comments
2. If line is empty → skip
3. If line contains `,` → parse as **free-field**
4. Else if stripped line matches common executive/case multi-token pattern:
   - more than one whitespace token
   - short line / non-bulk line
   → parse as **whitespace executive/case line**
5. Else → parse as **fixed-width 8-character fields**

### Required examples

#### Example A
Input:

```text
SOL 101
```

Must parse as:

```python
["SOL", "101"]
```

#### Example B
Input:

```text
SUBCASE 1
```

Must parse as:

```python
["SUBCASE", "1"]
```

#### Example C
Input:

```text
MAT1,1,7.0E7,,0.3,0.1
```

Must parse as free-field.

#### Example D
Input:

```text
GRID    1       0       0.0     0.0     0.0
```

Must parse as fixed-width fields if not already matched by earlier rules.

---

## 6. Continuation Resolution Algorithm

The parser must resolve logical records before semantic interpretation.

### Continuation indicators
A line is a continuation line if:

- the first field is `+`
- the first field is `*`
- the line begins with `+`
- the line begins with `*`

### Continuation behavior
- continuation content shall be appended to the previous logical record
- continuation markers themselves shall not become semantic card names
- merged logical record shall be parsed as one record

### Algorithm

1. Initialize `current_record = ""`
2. For each raw line:
   - strip comments
   - skip blank lines
   - if line is continuation:
     - append continuation payload to `current_record`
   - else:
     - if `current_record` is not empty, emit it
     - start new `current_record = line`
3. After final line, emit last `current_record`

### Required invariant
No semantic parsing may occur before continuation resolution is complete.

---

## 7. Executive Control Semantic Rules

### SOL
Example:

```text
SOL 101
```

Required mapping:

```json
{
  "executiveControl": {
    "sol": 101
  }
}
```

Constraint:
- `SOL` must **not** also appear in `otherCards`

### CEND
Example:

```text
CEND
```

Required mapping:

```json
{
  "executiveControl": {
    "cendPresent": true
  }
}
```

### Other executive cards
Non-modeled executive cards may be preserved in:

```json
executiveControl.otherCards
```

but only if they are not already mapped to a dedicated field.

---

## 8. Case Control Semantic Rules

### SUBCASE
Example:

```text
SUBCASE 1
```

Required mapping:

```json
{
  "caseControl": {
    "subcases": [
      { "id": 1 }
    ]
  }
}
```

### Scalar assignments
Examples:

```text
SPC = 2
LOAD = 2
DLOAD = 7
```

Required mapping to current subcase:

- `SPC` → `subcase.spc`
- `LOAD` → `subcase.load`
- `DLOAD` → `subcase.load` or explicitly preserved per chosen contract

### Analysis type
If the contract requires it, `analysisType` may be inferred from `SOL`.

---

## 9. Bulk Data Semantic Rules

### GRID
Rule:
- increment node count only
- do not preserve full node table in baseline contract mode

### Element cards
Examples:

- `CQUAD4`
- `CTRIA3`
- `CBAR`
- `CBEAM`
- `CBUSH`

Rule:
- increment `elementCountsByType[card]`
- do not preserve connectivity in baseline contract mode

### MAT1
Rule:
- preserve `mid`
- preserve `type = MAT1`
- do not infer missing properties unless contract explicitly permits

---

## 10. Prohibited Behaviors

The parser must not:

- treat `SOL 101` as a single card string in `otherCards`
- treat comments as semantic input
- mix free-field and fixed-field parsing arbitrarily
- parse continuation markers as primary cards
- reconstruct mesh in baseline mode
- hallucinate material, property, or load data

---

## 11. Minimal Test Cases

### Test 1
Input:

```text
SOL 101
CEND
BEGIN BULK
ENDDATA
```

Expected:
- `executiveControl.sol == 101`
- `executiveControl.cendPresent == true`
- `SOL` absent from `otherCards`

### Test 2
Input:

```text
SOL 101
CEND
SUBCASE 1
  SPC = 2
  LOAD = 2
BEGIN BULK
GRID    1       0       0.0     0.0     0.0
CQUAD4  1       1       1       2       3       4
ENDDATA
```

Expected:
- one subcase with `id=1`, `spc="2"`, `load="2"`
- `nodeCount == 1`
- `elementCountsByType.CQUAD4 == 1`

---

## 12. Summary

This parsing contract defines the front-end rules that convert a raw Nastran deck into parsed semantic facts suitable for deterministic decimation and downstream exchange-layer construction.

No downstream stage may override these front-end parsing rules.
