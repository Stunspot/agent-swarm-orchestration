PARTIAL — DEPENDENCY UNAVAILABLE

**Missing Source:** `customer-import-format` definition or the target repository containing its implementation (parser).  
**Exact Method to Identify/Read It:** Inspect the codebase of the unavailable target repository for files matching patterns like `*.py`, `*.ts`, `*.java`, etc., that handle CSV, JSON, XML, or custom delimited formats; search for class names/functions named `CustomerImporter`, `ImportParser`, `FormatHandler`; review configuration schemas (e.g., OpenAPI specs) referencing the import endpoint.  
**Downstream Slice Held Pending:** Design exact tests for the customer-import parser. This includes generating unit test cases covering valid inputs, edge cases (malformed rows, missing fields), and invalid inputs; defining expected outputs or error responses based on schema validation rules found in the unavailable repository.  

---

### Independent Authority Conclusion
The mission cannot proceed to design exact tests without access to the target repository that defines the customer-import format parser. The absence of this source prevents:  
- Identifying input/output schemas, field constraints, and parsing logic;  
- Determining edge cases specific to the implementation (e.g., date formats, encoding rules);  
- Validating test coverage against actual behavior rather than hypothetical assumptions.  

No generic tests or substitute packets are drafted here because they would lack fidelity to the real parser’s requirements. The downstream slice remains entirely held pending until the missing source is supplied or an alternative authoritative definition becomes available.
