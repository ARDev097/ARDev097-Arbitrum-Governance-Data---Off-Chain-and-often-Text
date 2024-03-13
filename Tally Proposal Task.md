# Arbitrum Governance Data Pipeline - Text of Tally Proposals

## Task Description

The focus of this subtask within the Arbitrum Governance Data Pipeline project is to gather and process data related to the text of tally proposals. The goal is to create a reproducible and generalizable method for obtaining essential governance data from on-chain sources, specifically concentrating on tally proposals.

## Subtask Description

In this subtask, the following dataset has been created, providing a comprehensive view of tally proposal details:

### Datasets Column Explanation

1. **id**: Proposal unique identifier.
2. **title**: Proposal title.
3. **description**: Proposal description.
4. **start_timestamp**: Timestamp when the voting for the proposal starts.
5. **end_timestamp**: Timestamp when the voting for the proposal ends.
6. **for_votes**: Count of 'for' votes on the proposal.
7. **for_vote_weightage**: Total weightage of 'for' votes on the proposal.
8. **for_percentage**: Percentage of 'for' votes from the total voting percentage.
9. **against_votes**: Count of 'against' votes on the proposal.
10. **against_vote_weightage**: Total weightage of 'against' votes on the proposal.
11. **against_percentage**: Percentage of 'against' votes from the total voting percentage.
12. **abstain_votes**: Count of 'abstain' votes on the proposal.
13. **abstain_vote_weightage**: Total weightage of 'abstain' votes on the proposal.
14. **abstain_percentage**: Percentage of 'abstain' votes from the total voting percentage.

## Advantages of Using This Dataset

1. **Comprehensive Proposal Information**: The dataset provides a detailed overview of each tally proposal, including its title, description, and timestamps for voting start and end.
2. **Granular Voting Breakdown**: Analysts can analyze the dataset to understand the distribution of 'for,' 'against,' and 'abstain' votes, along with their corresponding weightages.
3. **Timestamp Analysis**: The inclusion of start and end timestamps allows for temporal analysis, understanding voting patterns over time.
4. **Ease of Proposal Identification**: Analysts can easily retrieve the proposal ID directly from the 'id' column, simplifying the process of identifying specific proposals.

