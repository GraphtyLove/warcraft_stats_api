from typing import Dict, Any
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
import os
import httpx as requests

def get_Oauth_jwt(client_id: str, client_secret: str, api_url: str) -> str:
    """
    Function that get the JWT from warcraft logs.
    :return: JWT in string
    """
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(api_url, data=data,
                             auth=(client_id, client_secret))
    response_json = response.json()
    jwt = response_json["access_token"]
    return jwt


def gql_query(query, params: Dict[str, Any]) -> Dict[str, Any]:
    print("params: ", params)
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(
        url=os.environ["WL_API_GQL_URL"],
        headers={"Authorization": "Bearer " + os.environ["WL_JWT"]},
    )
    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)
    try:
        # Execute the query on the transport
        print("Sending GQL query")
        result = client.execute(query, variable_values=params)
        print("GQL query success")
        return result
    except Exception as ex:
        print(f"ERROR WHILE SENDING GQL QUERY: {ex}")
        return {"error": ex}