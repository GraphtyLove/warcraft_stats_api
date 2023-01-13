from typing import Dict, List

from httpx import AsyncClient, Client


async def get_request_async(url: str, client: AsyncClient, headers: Dict[str, str] | None = None) -> List | Dict | None:
	response = await client.get(url=url, headers=headers)
	return response.json()


def get_request_sync(url: str, client: Client | None = None, headers: Dict[str, str] | None = None) -> List | Dict | None:
	if not client:
		client = Client()
	return client.get(url=url, headers=headers).json()
