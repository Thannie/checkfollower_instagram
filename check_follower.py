from instagrapi import Client
from instagrapi.exceptions import LoginRequired, UserNotFound
from instagrapi.types import UserShort

import argparse, re

import time

import os
import sys

def get_input() -> tuple[argparse.Namespace]:
    """
    Parses the command line arguments and returns the username, password, target user, and delay range.
    """
    
    def delay_range_type(value):
        """Custom argparse type for delay range in the form lower-upper."""
        try:
            lower, upper = map(int, value.split('-'))
        except ValueError:
            raise argparse.ArgumentTypeError(f"Delay must be in the form lower-upper, given: {value}")
        
        if lower == 0 and upper == 0:
            print("Using no delay is not advised.")
        
        if lower < 0 or upper < 0 or lower > 10 or upper > 10 or lower > upper:
            raise argparse.ArgumentTypeError(f"Delay range must be between 0 and 10 seconds, and lower must be <= upper. Given: {value}")
        
        return lower, upper

    def is_delay(value):
        """Check if the value matches the delay format."""
        return re.match(r'^\d+-\d+$', value) is not None

    # Create the parser
    parser = argparse.ArgumentParser(description='Process some inputs.')

    # Add the required arguments
    parser.add_argument('username', type=str, help='Your username')
    parser.add_argument('password', type=str, help='Your password')

    # Add the optional target argument
    parser.add_argument('target', type=str, nargs='?', help='The target (optional)')

    # Add the optional delay argument
    parser.add_argument('delay', type=delay_range_type, nargs='?', default=(2, 5), help='Optional delay range in seconds (0-10) in the form lower-upper (default: 2-5)')

    # Parse the known arguments
    args = parser.parse_known_args()[0]


    if args.target and is_delay(args.target):
        args.delay = delay_range_type(args.target)
        args.target = None
    else:
        if len(parser.parse_known_args()[1]) > 0:
            args.delay = delay_range_type(parser.parse_known_args()[1][0])

    if args.target == None:
        print("No target specified, checking for the logged-in account.")
        args.target = args.username

    return args.username, args.password, args.target, args.delay

def login_user() -> None:
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """
    USERNAME = sys.argv[1]
    PASSWORD = sys.argv[2]

    global client 

    client = Client()
    client.delay_range = DELAY_RANGE

    try:
        session = client.load_settings("session.json")
    except Exception as e:
        print("Couldn't load session: %s" % e)
        print("Attempting to login without session information")
        session = None

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            client.set_settings(session)
            client.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                client.get_timeline_feed()
            except LoginRequired:
                print("Session is invalid, need to login via username and password")

                old_session = client.get_settings()

                # use the same device uuids across logins
                client.set_settings({})
                client.set_uuids(old_session["uuids"])

                client.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            print("Couldn't login user using session information: {}".format(e))

    if not login_via_session:
        try:
            print("Attempting to login via username and password. username: %s" % USERNAME)
            if client.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            print("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")
    
    client.dump_settings("session.json")
    return None

def get_user_id(username) -> str:
    return client.user_id_from_username(username)

def get_followers(user_id) -> dict[str, UserShort]:
    return client.user_followers(user_id) 

def get_following(user_id) -> dict[str, UserShort]:
    return client.user_following(user_id)

def get_solely_followers_following(followers, following) -> tuple[list[str], list[str]]:
    """
    Returns a tuple of two lists: the first list contains the followers that are not following back,
    and the second list contains the people you are following but they are not following you back.
    """
    followers = {followers[follower].username for follower in followers}
    following = {following[follower].username for follower in following}

    followers_set = set(followers)
    following_set = set(following)

    common = followers_set.intersection(following_set)

    fans = [fan for fan in followers if fan not in common]
    fanning = [fan for fan in following if fan not in common]

    return fans, fanning

def save_results(fans, fanning) -> bool:
    """
    Saves the results to a file in the insta_data directory.
    Returns True if the results were saved successfully, False otherwise.
    """

    global directory
    directory = "insta_data"

    if not os.path.exists(directory):
        os.mkdir(directory)

    try:
        filepath = os.path.join(directory, f"{SPECIFIED_USER}_fanning.txt")

        with open(filepath, "w") as f:
            for fan in fanning:
                f.write(fan + "\n")
    except Exception as e:
        print(f"Error saving {filepath}: {e}")

        return False

    try:
        filepath = os.path.join(directory, f"{SPECIFIED_USER}_fans.txt")

        with open(filepath, "w") as f:
            for fan in fans:
                f.write(fan + "\n")
    except Exception as e:
        print(f"Error saving {filepath}: {e}")

        return False


    return True

def to_stdout(fans, fanning) -> None:
    """
    Prints the results to stdout, in case saving the results failed.
    """
    print("You follow this user but they are not following you!")

    for fan in fanning:
        print(fan)

    print("\n\n")
    print("They are following you but you are not following them!")

    for fan in fans:
        print(fan)

    print("\n\n")

    return None

def main():
    t1 = time.time()

    global USERNAME, PASSWORD, SPECIFIED_USER, DELAY_RANGE    

    USERNAME, PASSWORD, SPECIFIED_USER, DELAY_RANGE = get_input()
    
    login_user()

    try:
        user_id = get_user_id(SPECIFIED_USER)
    except UserNotFound:
        print("Target user not found.")
        sys.exit(1)

    followers = get_followers(user_id)
    following = get_following(user_id)

    fans, fanning = get_solely_followers_following(followers, following)
    
    successfully_saved = save_results(fans, fanning)

    if not successfully_saved:
        to_stdout(fans, fanning)
    else:
        print("Results saved successfully to {}.".format(directory))

    print("Done! Elapsed: {} seconds".format(round((time.time() - t1), 2)))
    print("Checked for: {}".format(SPECIFIED_USER))
    print("Total fans: {}".format(len(fans)))
    print("Total fanning: {}".format(len(fanning)))
    

if __name__ == "__main__":
    main()
