#!/usr/bin/env python3

import getpass
import logging
import argparse
import keyring
from keyring.errors import PasswordDeleteError
import sys


def create_argument_parser():
    logger.debug("Parsing Arguments")
    p = argparse.ArgumentParser(description="Simple keyring handler")
    p.add_argument('--add', '-a', help="Add credentials to keyring", action="store_true")
    p.add_argument('--remove', '-r', help="Remove credentials from keyring", action="store_true")
    p.add_argument('--service', '-s', help="Service name to add or remove")
    p.add_argument('--username', '-u', help="Username to add or remove")
    p.set_defaults(add=False, remove=False)

    return p


def initialize_logger():
    _logger = logging.getLogger(__file__)
    _logger.setLevel(logging.INFO)
    # formatter = logging.Formatter("%(levelname)s: %(message)s")
    formatter = logging.Formatter("%(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt=formatter)
    _logger.addHandler(stream_handler)
    return _logger


def add_credentials(service, username, password):
    keyring.set_password(service, username, password)
    logger.info("Credentials for [%s] stored", service)


def remove_credentials(service, username):
    try:
        keyring.delete_password(service, username)
        logger.info("Credentials of user [%s] for service [%s] removed", username, service)
    except PasswordDeleteError as e:
        logger.error("Failed to remove credentials: %s", e)
        sys.exit(1)


def add_credentials_handler():
    username = arguments.username
    service = arguments.service
    passwords_match = False
    while not passwords_match:
        password = getpass.getpass()
        logger.info("Please confirm the password")
        password_confirmation = getpass.getpass()
        if password == password_confirmation:
            passwords_match = True
            add_credentials(service, username, password)
        else:
            logger.warn("Passwords do not match, please retry")


def remove_credentials_handler():
    username = arguments.username
    service = arguments.service
    response = ""
    while response not in ["y", "n"]:
        response = input("Are you sure you want to remove saved credentials for [%s] [y/n]: " % service)
    if response == "y":
        remove_credentials(service, username)

if __name__ == "__main__":
    logger = initialize_logger()
    argument_parser = create_argument_parser()
    arguments = argument_parser.parse_args()
    if arguments.add:
        if not arguments.service or not arguments.username:
            argument_parser.print_help()
        else:
            add_credentials_handler()
    elif arguments.remove:
        if not arguments.service or not arguments.username:
            argument_parser.print_help()
        else:
            remove_credentials_handler()
    else:
        argument_parser.print_help()
