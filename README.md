# Data Processing Tool

This tool automates lead validation using Python and Pandas.

### Logic Overview:
- **Modular Filtering:** Separates rules for `NWC`, `Title`, and `Prooflink`.
- **String Normalization:** Ensures case-insensitive matching for titles and requirements.
- **Domain Verification:** Checks if prooflinks correspond to corporate email domains.

### Scalability Note:
For datasets larger than 50k rows, the logic can be optimized using **vectorized operations** in Pandas to maintain high performance.
