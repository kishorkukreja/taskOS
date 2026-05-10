# Primary Run Prompt

You are the primary implementation agent for `mission.md` in this folder.

Goal:
Build `artifacts/primary-output/mission_artifact_auditor.py`.

The script should:

1. Accept a mission folder path as the first argument, defaulting to `.`.
2. Accept `--json <path>` to write a machine-readable report.
3. Check for these required files:
   - `mission.md`
   - `README.md`
   - `docs/idea.md`
   - `artifacts/codex-goal-feature-check.md`
   - `artifacts/primary-run-prompt.md`
   - `artifacts/primary-run-log.md`
   - `artifacts/goal-buddy-review.md`
   - `artifacts/findings.md`
   - `artifacts/checkpoint-notes/checkpoint-001.md`
4. Check that `mission.md` contains sections for objective, definition of done, non-goals, constraints, verification commands, reward/evaluation criteria, and current next step.
5. Emit a concise console summary and a JSON object with `passed`, `missing_files`, `missing_mission_sections`, and `score` fields.
6. Exit 0 only if all required files and sections are present.

Do not edit files outside this experiment folder.
Record assumptions and limitations in `artifacts/primary-run-log.md`.
