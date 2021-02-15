#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
SafeLoad YAML Parser
--------------------
Modified: 2020-10

Syntax inspired by: https://www.elastic.co/guide/en/beats/winlogbeat/current/using-environ-vars.html

Usage:
test.yaml:
    ...
    hostname: ${HOSTNAME:black-pearl}
                    ^         ^
                 env var    default
    ...
If the environment variable cannot be found a default value can be specified as a fallback.
"""

import logging
import yaml
import re
import os
import sys


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def path_constructor(loader:yaml.loader.SafeLoader, node:yaml.nodes.ScalarNode) -> str:
    """
    Extract the matched value, expand env variable, and replace the match
    
    :raises IndexError: if environment variable was not found and no default was specified
    :returns: string replacement
    """
    value = node.value
    match = path_matcher.match(value)
    env_var = match.group()[2:-1].split(':')
    try:
        var = os.environ[env_var[0]] + value[match.end():]
    except KeyError:
        # here we expect the default to be defined otherwise we raise IndexError
        var = env_var[1] + value[match.end():]
    return var

path_matcher = re.compile(r'\$\{([^}^{]+)\}')
yaml.add_implicit_resolver('!path', path_matcher, None, yaml.loader.SafeLoader)
yaml.add_constructor('!path', path_constructor, yaml.loader.SafeLoader)

logging.info("Loading yaml from: %s", sys.argv[1])
# LOAD path to yaml from arg
with open(sys.argv[1], 'r') as stream:
    try:
        user_cfg = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logging.exception("Error parsing yaml: %s", exc)
    except IndexError as exc:
        logging.exception("Environment variable required but was not specified: %s", exc)
    else:
        logging.info('Saving to build directory')
        with open(os.environ['BUILD']+'/user-data', 'w') as outstream:
            yaml.dump(user_cfg, outstream, default_flow_style=False)
    logging.info('Yaml parse complete')
    