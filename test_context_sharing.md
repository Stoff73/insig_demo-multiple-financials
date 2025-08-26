# Testing Company/Ticker Context Sharing

## Test Steps

### Test 1: Analysis Tab → Ratios Tab
1. Open the application at http://localhost:5173
2. Navigate to the **Analysis** tab
3. Enter company name: "Test Company"
4. Enter ticker: "TEST"
5. Navigate to the **Ratios Configuration** tab
6. **Expected**: The dialog should NOT appear, and "Test Company (TEST)" should be shown at the top

### Test 2: Ratios Tab → Analysis Tab
1. Clear browser localStorage (Developer Tools → Application → Storage → Local Storage → Clear)
2. Refresh the page
3. Navigate to the **Ratios Configuration** tab
4. Enter company name: "XP Power"
5. Enter ticker: "XPP"
6. Click "Configure Ratios"
7. Navigate to the **Analysis** tab
8. **Expected**: Company and Ticker fields should be pre-filled with "XP Power" and "XPP"

### Test 3: Change Company in Ratios Tab
1. In the **Ratios Configuration** tab with existing company
2. Click "Change Company" button
3. Enter new company: "Another Company"
4. Enter new ticker: "ANC"
5. Click "Configure Ratios"
6. Navigate to **Analysis** tab
7. **Expected**: Fields should update to "Another Company" and "ANC"

### Test 4: Persistence Across Page Reload
1. Set company and ticker in either tab
2. Refresh the browser page (F5)
3. **Expected**: Company and ticker should persist across page reload

### Test 5: No Folder Creation on Typing
1. Clear any test folders from data/ directory
2. Navigate to **Ratios Configuration** tab
3. Type slowly: "A", then "AB", then "ABC" in ticker field
4. Check data/ directory
5. **Expected**: No folders should be created until "Configure Ratios" is clicked

## Implementation Details

- **Context Provider**: `CompanyContext` provides shared state
- **localStorage**: Persists data across page reloads and tabs
- **Folder Creation**: Only happens on save action in RatioConfigManager
- **Bidirectional Sync**: Both tabs read and write to shared context