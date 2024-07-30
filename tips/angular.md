- Search 'Cannot enable prod mode after platform setup'and save function name (example Hd)
- match and replace in response body: 


  - Select the Proxy tab in Burp Suite 
  - Select the Proxy -> Options sub-tab 
  - Scroll down to the “Match/Replace” section and remove any existing rules 
  - Click “Add” to add a new rule 
  - Select “Response Body” as the type 
  - Match the string <code>function Hd(){ </code>
  - Add in a replacement string that adds <code> function Hd(){ ngDevMode=1; return </code>
