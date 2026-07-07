AUDIT_CONTRACT_PROMPT = """ 
Step 1: Read the entire source codes from input text.
Step 2: Determine the entry function for auditing.
Step 3: Analyze the entry function for potential security vulnerabilities.
Step 4: Make a detailed plan on how to attack the contract, code is required.
Step 5: Generate a report summarizing the findings and recommendations for improving security.
{code}
"""