import requests
from datetime import datetime
import json
from dotenv import load_dotenv
import os 
import csv

# Load environment variables from .env file
load_dotenv()

# GraphQL endpoint URL
graphql_url = 'https://api.tally.xyz/query'

# Your GraphQL query
query = """
query GovernanceProposals($sort: ProposalSort, $chainId: ChainID!, $pagination: Pagination, $governanceIds: [AccountID!], $proposerIds: [AccountID!], $voters: [Address!], $votersPagination: Pagination, $includeVotes: Boolean!) {
  proposals(
    sort: $sort
    chainId: $chainId
    pagination: $pagination
    governanceIds: $governanceIds
    proposerIds: $proposerIds
  ) {
    id
    title
    description
    start {
      ... on Block {
        timestamp
      }
    }
    end {
      ... on Block {
        timestamp
      }
    }
    statusChanges {
      type
    }
    block {
      ... on Block {
        timestamp
      }
    }
    voteStats {
      votes
      weight
      support
      percent
    }
    votes(voters: $voters, pagination: $votersPagination) @include(if: $includeVotes) {
      support
      voter {
        picture
        address
        identities {
          twitter
        }
      }
    }
    governance {
      id
      quorum
      name
      timelockId
      organization {
        metadata {
          icon
        }
      }
      tokens {
        decimals
      }
    }
    tallyProposal {
      id
      createdAt
      status
    }
  }
}
"""

# Headers for the request
headers = {
    "Api-key": os.getenv("API_KEY")  # Retrieve API key from environment variable
}

def fetch_and_save_data():
    print("Fetching and processing data at", datetime.now())

    # Variables for the GraphQL query
    variables = {
        "sort": {
            "field": "START_BLOCK",
            "order": "DESC"
        },
        "chainId": "eip155:42161",
        "governanceIds": ["eip155:42161:0xf07DeD9dC292157749B6Fd268E37DF6EA38395B9", "eip155:42161:0x789fC99093B09aD01C34DC7251D0C89ce743e5a4"],
        "votersPagination": {
            "limit": 1,
            "offset": 0
        },
        "includeVotes": False
    }

    # Sending the GraphQL request with pagination
    total_records = 27
    limit_per_request = 20

    extracted_data = []

    for offset in range(0, total_records, limit_per_request):
        variables["pagination"] = {"limit": limit_per_request, "offset": offset}

        response = requests.post(graphql_url, json={'query': query, 'variables': variables}, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            data = response.json()

            # Extracting relevant information from the response
            proposals = data['data']['proposals']

            # Extracting specific fields from each proposal
            for proposal in proposals:
                start_timestamp = proposal["start"]["timestamp"]
                end_timestamp = proposal["end"]["timestamp"]

                # Check if timestamps are in string format
                if isinstance(start_timestamp, str):
                    start_timestamp = datetime.strptime(start_timestamp, '%Y-%m-%dT%H:%M:%SZ').timestamp()

                if isinstance(end_timestamp, str):
                    end_timestamp = datetime.strptime(end_timestamp, '%Y-%m-%dT%H:%M:%SZ').timestamp()

                # Extracting voteStats
                for_stats = next((stats for stats in proposal["voteStats"] if stats["support"] == "FOR"), {})
                against_stats = next((stats for stats in proposal["voteStats"] if stats["support"] == "AGAINST"), {})
                abstain_stats = next((stats for stats in proposal["voteStats"] if stats["support"] == "ABSTAIN"), {})

                extracted_data.append({
                    "id": proposal["id"],
                    "title": proposal["title"],
                    "description": proposal["description"],
                    "start_timestamp": datetime.utcfromtimestamp(int(start_timestamp)).strftime('%Y-%m-%d %H:%M:%S'),
                    "end_timestamp": datetime.utcfromtimestamp(int(end_timestamp)).strftime('%Y-%m-%d %H:%M:%S'),
                    "for_votes": for_stats.get("votes", 0),
                    "for_vote_weightage": for_stats.get("weight", 0),
                    "for_percentage": for_stats.get("percent", 0),
                    "against_votes": against_stats.get("votes", 0),
                    "against_vote_weightage": against_stats.get("weight", 0),
                    "against_percentage": against_stats.get("percent", 0),
                    "abstain_votes": abstain_stats.get("votes", 0),
                    "abstain_vote_weightage": abstain_stats.get("weight", 0),
                    "abstain_percentage": abstain_stats.get("percent", 0),
                    "tallyproposal_status": proposal["tallyProposal"]["status"],
                })

        else:
            print(f'Error: {response.status_code}, {response.text}')

    # Saving data to a JSON file with utf-8 encoding
    json_file_path = 'tally_proposals_text_data.json'
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(extracted_data, json_file, ensure_ascii=False, indent=2)

    # Saving data to a CSV file
    csv_file_path = 'tally_proposals_text_data.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=extracted_data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(extracted_data)

    print(f'Data has been successfully saved to {json_file_path} and {csv_file_path}')

# Execute the data-fetching logic
fetch_and_save_data()
