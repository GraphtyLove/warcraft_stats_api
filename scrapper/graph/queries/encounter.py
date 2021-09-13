"""File containing the GQL query for one encounter."""

from gql import gql

# Query top 100 players for an encounter
ENCOUNTER_QUERY = gql(
    """
    query worldData ($encounter_id: Int!, $class_name: String!, $spec_name: String!, $difficulty: Int!, $metric: CharacterRankingMetricType, $covenantID: Int) {
    worldData{
        encounter (id: $encounter_id){
        name
        characterRankings (className: $class_name, difficulty: $difficulty, metric: $metric, page: 1, specName: $spec_name, covenantID: $covenantID) 
    }
    }
}
    """
)
