from typing import Dict, List

from httpx import AsyncClient, Client


async def get_request_async(url: str, client: AsyncClient) -> List | Dict | None:
	response = await client.get(url=url)
	return response.json()


def get_request_sync(url: str, client: Client) -> List | Dict | None:
	return client.get(url=url).json()
