run:
\tuvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
\tdocker build -t face-attendance .

docker-run:
\tdocker run -p 8000:8000 -v $(PWD)/data:/app/data face-attendance

test:
\tpytest -q

fmt:
\tpython - <<'PY'\nprint("No formatter pinned; add ruff/black if needed.")\nPY
