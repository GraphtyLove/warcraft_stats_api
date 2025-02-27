import os

from httpx import Client
from scrapper.exceptions import CharacterNotFound
from scrapper.http_request import get_request_sync


def get_character_spec(region: str, realm_slug: str, character_name: str, client: Client) -> dict:
	region = region.lower()
	character_name = character_name.lower()
	api_endpoint = f"https://{region}.api.blizzard.com/profile/wow/character/{realm_slug}/" \
	               f"{character_name.replace(' ', '')}/specializations?locale=en_US"
	request_headers = {
		'Authorization': f"Bearer {os.environ['BN_JWT']}",
		'Battlenet-Namespace': f'profile-{region}'
	}

	try:
		response_json = get_request_sync(url=api_endpoint, client=client, headers=request_headers)
		if not response_json:
			print(f"Skipping SPEC for: {character_name}  {region}-{realm_slug}. 404")
			raise CharacterNotFound()
		return {"spec": response_json["active_specialization"]["name"]}
	except BaseException as ex:
		print("SPEC FAIL: ", ex)


