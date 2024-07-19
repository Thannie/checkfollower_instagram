# Instagram Follower Analyzer

This Python script analyzes the followers and following lists of an Instagram account to identify:

1. Users who follow the account but are not followed back ("fans")
2. Users the account follows but who don't follow back ("fanning")

## Features

- Supports login via username/password or saved session
- Configurable delay between API requests to avoid rate limiting
- Saves results to text files in an `insta_data` directory

## Prerequisites

- Python 3.x

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/Thannie/checkfollower_instagram.git
   cd checkfollower_instagram
   ```
2. Install the required packages using the requirements.txt file:

   ```
   pip install -r requirements.txt
   ```

   This will install all necessary dependencies, including the instagrapi library.

   ---

## Usage

Run the script with the following command:

```
python check_followers.py <username> <password> [<target_username>] [<delay_range>]
```

- `<username>`: Your Instagram username
- `<password>`: Your Instagram password
- `<target_username>` (optional): The username to analyze. If not provided, it will analyze your own account.
- `<delay_range>` (optional): Delay range in seconds (0-10) in the form lower-upper (default: 2-5)

Example:

```
python check_followers.py myusername mypassword targetuser 1-3
```

## Output

The script will create two files in the `insta_data` directory:

- `<target_username>_fans.txt`: List of users who follow the target but are not followed back
- `<target_username>_fanning.txt`: List of users the target follows but who don't follow back

## Disclaimer and Legal Notice

This software is provided "as is", without warranty of any kind, express or implied. By using this software, you agree to the following terms:

1. Educational Purpose: This script is intended for educational purposes only. It is designed to demonstrate programming concepts and API interactions.
2. Use at Your Own Risk: The use of this software is at your own risk. The author will not be liable for any damages, including but not limited to, direct, indirect, special, incidental or consequential damages or losses that occur due to your use of this software.
3. Compliance with Terms of Service: It is your responsibility to ensure that your use of this software complies with Instagram's Terms of Service and API usage guidelines. The author does not guarantee that the use of this software is permitted under Instagram's policies.
4. No Warranty: The author does not warrant that the software will meet your requirements or that the operation of the software will be uninterrupted or error-free.
5. Data Privacy: This software may collect and process personal data. It is your responsibility to ensure that your use of this software complies with relevant data protection laws and regulations.
6. Updates and Support: The author is under no obligation to provide support, updates, or bug fixes for this software.
7. Modifications: If you modify this software, you do so at your own risk. The author is not responsible for any issues arising from modifications made by users.

By using this software, you acknowledge that you have read this disclaimer, understand it, and agree to be bound by its terms.

## License

[MIT License](LICENSE)
