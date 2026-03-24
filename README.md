# CustomerAPI (Python 3.9) - example

Examples of initial connection and basic communication with the **CustomerAPI**.

> [!IMPORTANT]
> These are **demo examples**; therefore, not all API functions are implemented.

The full API documentation can be found at:  
[https://api.sos.sk/customer/docs](https://api.sos.sk/customer/docs)

## Commands
- **login**: Prompts for username and password. Uses `Basic SosApiKey` for authentication.
- **search**: Performs a GET request to `/products?query={search_string}`. Requires an active Bearer token.
- **item**: Performs a GET request to `/products/{item_number}`. Requires an active Bearer token.
- **status** Check token validity and remaining time.
- **revoke**: Manually invalidates the current access token.
- **quit**: Automatically revokes the token and terminates the application.

## Token Management
The program automatically checks token validity before each command prompt. If the token is near expiration (less than 5 minutes), the user is prompted to manually authorize a refresh.

## Authentication Headers
- **Auth routes**: `Authorization: Basic {SosApiKey}`
- **Other routes**: `Authorization: {token_type} {access_token}`# SosCustomerApiPy