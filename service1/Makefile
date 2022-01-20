help: ## show this help
	@echo 'usage: make [target] ...'
	@echo ''
	@echo 'targets:'
	@egrep '^(.+)\:\ .*##\ (.+)' ${MAKEFILE_LIST} | sed 's/:.*##/#/' | column -t -c 2 -s '#'

install:  ## install requirements
	pip install -r requirements.txt
	pip install grpcio-tools mypy-protobuf

dev: ## start in dev mode
	PYTHONASYNCIODEBUG=1 DEBUG=1 PORT=8080 watchmedo auto-restart -d app -p '*.py' -- python -m app.main

proto: ## prepare grpc files
	python -m grpc_tools.protoc --proto_path=../protos/service1 --python_out=. --grpc_python_out=. --mypy_out=. ../protos/service1/app/grpc/service1.proto

lint:  ## run linters
	flake8 app
	mypy --ignore-missing-imports --follow-imports=silent app
