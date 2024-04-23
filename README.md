# Summary check heuristic

This is a set of functions written in order to check the accuracy of the summary generated by Claude. 
A heuristic like this would be useful to automatically detect summaries in which amounts and decimals are wrong.
The functions extract and compare the values found in asset_changes and summary in order to assess if the summary is faulty or not.

This heuristic is still flawed and requires more testing and suggestions.

### Objective:
- Figuring out a way to automatically detect a flawed summary in order to automatically up the model and re-run Claude
  
### Assumptions:
* - asset_changes json object returned by Tenderly contains the accurate amounts of all asset changes
        * - After the fixes from dev branch, this should hold true
* - These values are all expected to be present in an accurate summary
 
### Flow:
* 1. Extract amount values from asset_changes and the summary
* 2. Check if all the values from asset_changes are present in the summary values
* 3. If not, up the model and restart
* 4. If yes, check if there are values in summary that do NOT appear in asset_changes values
* 5. If there are none, the summary is fine
* 6. If there are any, compare them to the values in asset_changes
        * Remove any extra characters (',','.', etc.) and left trim '0' both values
        * The idea is that if values cleaned like this match, it implies right digits but wrong decimals         
* 7. If there are any matches, up the model and restart

### Issues:
* 1. Claude generates amounts in irregular ways
        * Sometimes, it rounds up the numbers, which can cause the heuristic to mistakenly conclude that there is a value from asset_changes missing
* 2. Claude sometimes uses numerical bullet lists
        * This is potentially a problem because when extracting numbers from the summary string it is difficult to filter out these bullet list numbers without filtering out other potentially useful numbers
        * The presence of bullet list numbers in the summary and, consequently, the list of summary values can cause problems during comparison
        * For example, when there is an amount of 0.1 ETH and the bullet list number 1., after removing extra characters and left trimming the '0' characters, the heuristic can conclude that there is a value with wrong decimals in the summary
