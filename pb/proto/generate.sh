#python -m grpc_tools.protoc -I . --python_out=../ --pyi_out=../ --grpc_python_out=../ enum.proto
#python -m grpc_tools.protoc -I . --python_out=../ --pyi_out=../ --grpc_python_out=../ object.proto
#python -m grpc_tools.protoc -I . --python_out=../ --pyi_out=../ --grpc_python_out=../ trader.proto
#python -m grpc_tools.protoc -I . --python_out=../ --pyi_out=../ --grpc_python_out=../ api_service.proto
#python -m grpc_tools.protoc -I . --python_out=../ --pyi_out=../ --grpc_python_out=../ strategy_service.proto
#python -m grpc_tools.protoc -I . --python_out=../ --pyi_out=../ --grpc_python_out=../ gateway_service.proto
#python -m grpc_tools.protoc -I . --python_out=../ --pyi_out=../ --grpc_python_out=../ backtest_service.proto
#python -m grpc_tools.protoc -I . --python_out=../ --pyi_out=../ --grpc_python_out=../ control_service.proto
#python -m grpc_tools.protoc -I . --python_out=../ --pyi_out=../ --grpc_python_out=../ quote_service.proto

python -m grpc_tools.protoc -I . --python_out=../ --pyi_out=../ --grpc_python_out=../ object.proto