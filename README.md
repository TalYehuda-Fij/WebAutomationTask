# WebAutomationTask - Profile Update and Avatar Change Test

## Test Purpose
This test validates the user's ability to update their profile information by:
- Successfully logging into the system
- Navigating through the profile settings
- Updating the username with a random string
- Changing the avatar selection
- Verifying the changes persist in the system
- Confirming access to the lobby and coin display functionality

## Preconditions
- Valid user credentials (email and password)
- Chrome browser with Selenium WebDriver installed
- Python environment with required packages:
  - selenium
  - random
  - logging
- User account with permissions to modify profile settings
- Initial stable state of the application
- User logged out of the system

## Steps to Execute
1. Open application and login:
   - Navigate to application URL
   - Click login button
   - Enter email and password
   - Submit login form
   - Handle subscription popup by clicking "Later"

2. Access profile settings:
   - Click Menu button
   - Navigate to "My Account"
   - Click Edit (pencil) button

3. Modify profile:
   - Generate and enter random username
   - Select random avatar
   - Wait 3 seconds
   - Click Apply button

4. Verify changes:
   - Navigate to My Profile
   - Verify new username is displayed
   - Return to lobby
   - Check coin amounts are visible

## Post-Conditions
- Log out of the system (if required)
- Close browser and WebDriver sessions
- Ensure all system resources are properly released
- Document any changes made to the test account

## Validation Criteria
Test is considered successful if:
1. User successfully logs in and navigates to profile settings
2. New random username is saved and displayed correctly
3. Avatar change is successfully applied
4. User can return to lobby and view coin amounts
5. No error messages or unexpected behaviors occur during test execution
6. All steps complete within specified timeouts (10 seconds per action)
