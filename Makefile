.PHONY: server

server:
	.venv/bin/python -m app

.PHONY: styles

styles:
	./tailwindcss -i src/app/static/input.css -o src/app/static/tailwind.css --watch

.PHONY: dev

dev:
	${MAKE} -j2 styles server

stop:
	pkill -f ".venv/bin/python -m app" || true
	pkill -f "./tailwindcss -i src/app/static/input.css -o src/app/static/tailwind.css --watch" || true
