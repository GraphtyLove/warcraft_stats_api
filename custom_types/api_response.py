from typing import Dict, Literal, Any

ErrorResponse = Dict[Literal["error"], str]
SuccessResponse = Dict[Literal["data"], Any]