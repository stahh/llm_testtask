from fastapi.security import APIKeyHeader

token_header = APIKeyHeader(name="Authorization", auto_error=True)
