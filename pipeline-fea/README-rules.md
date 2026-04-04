How to use it with an LLM

Use a prompt shaped like this:

You are generating code for one pipeline stage.

Follow this machine-readable rule spec exactly:

[PASTE YAML OR JSON SPEC HERE]

Target stage: decimator

Produce:
    1. One Python file
    2. A short README paragraph
    3. A validation checklist showing how the file satisfies the rule spec

Or for the exchange stage:

    Follow this rule spec exactly.
    Target stage: exchange_creator.
    Do not generate any other stage.

