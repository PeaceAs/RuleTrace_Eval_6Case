# RuleTrace-Eval — Original Compositional Grid Reasoning (Six Cases)

Six original code-generated visual puzzles based on the broad task format of abstract grid transformation, **not copied from ARC-AGI-2**. They are independent prototypes, not yet validated GPT-6 failures. Prior observed GPT-6 failure on ARC-AGI-2 dbff022c motivates the research direction but is **not included** as a submission case.

## Set up on Windows (PowerShell)

Open the **inner RuleTrace_Eval_6Case** folder in VS Code, then:

```powershell
python -m unittest discover -s tests -v
Copy-Item results/model_responses_template.json results/model_responses.json
$p = Get-Content data/prompts.json -Raw | ConvertFrom-Json
($p | Where-Object { $_.id -eq 'RT-01' }).prompt | Set-Clipboard
```

Attach **images/RT-01.png** to a *fresh GPT-6 Medium* chat and paste the copied prompt. Save the model reply verbatim in `results/model_responses.json` for RT-01. Each response is a JSON-escaped string containing the raw JSON object. Test RT-02 through RT-06 with their corresponding PNGs and unchanged prompts.

Score (only after responses are saved):

```powershell
python score.py --responses results/model_responses.json --output results/scores.json
```

**Scoring:** 100 for an exact 2-D integer grid match, otherwise 0. Per-cell accuracy is separately reported for diagnostic use. Test-case reference outputs are in `data/reference_answers.json`; do not expose them in the GPT-6 testing conversation.

**Methodology:** Every puzzle has 3 training input/output pairs and 1 test input. The answer is obtained from deterministic generation. Testing must be documented, verified, and transparently labelled. One observed failure, if any, must be reproduced before claiming a stable weakness. These novel cases are intentionally designed to probe compositional transforms, not guaranteed to cause failure.

**Originality and competition disclosure:** The general input-output grid format is associated with ARC-AGI, which should be cited as inspiration. All grids, transformations, images, answer keys, and scoring code here were newly created. Check official competition requirements about using prior benchmark formats.
