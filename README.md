# Summary check heuristic

This is a set of functions written in order to check the accuracy of the summary. 
A heuristic like this is useful to automatically detect summaries in which amounts and decimals are wrong.

### Objective:
- To know when to upgrade the model and re-run the explanation
        - When some of the values from json are missing in summary -> upgrade and re-run
            - The reason for a value missing in summary can be either complete absence, or wrong decimals
            - In any case, if the check doesn't find any of the json values in the summary, it will re-run
            - It is also possible for the check to fail finding a value because claude rounded it up (!)
                - Needs a failsafe mechanism that will prevent infinite restarting, in case Claude decides to continue rounding up
        - When there are values in the summary that have the same digits as the ones from json, 
          but wrong decimals (excluding numbers for bullet lists etc.) -> upgrade and re-run
            - It implies misapplied decimals
            - Has to be separated because it is possible that all values from json will be in the summary,
              but it doesn't exclude the possibility that there might also be values with misapplied decimals
  
### Assumptions:
- asset_changes json object returned by Tenderly contains the accurate amounts of all asset changes
    - After the fixes from dev branch, this should be solved
- These values are expected to be present in an accurate summary
- 
### Flow:
Extract amount values from asset_changes and the summary
            |
Check if all the values from asset_changes are present in the summary values
    |                                              |
    |                                           If not, up the model and restart
If yes, check if there are values in summary
that do not appear in asset_changes values
    |
If there are any, compare them to
