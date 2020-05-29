# -*- coding: utf-8 -*-
from .errors import Error
from .controller import UnimonControl
from .api import api

import argparse
import logging
import os

def get_cli_logger():
  """ ⚠️ only needed for development ⚠️ """
  cli_logger = logging.getLogger("cli")
  cli_logger.setLevel(logging.ERROR)
  if os.getenv("UNIMONCTL_DEV", None):
    cli_logger.setLevel(logging.DEBUG)
  return cli_logger

def main():

  cli_logger = get_cli_logger()

  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s || %(message)s')
  controller = UnimonControl()

  def run_api(args):
    cli_logger.debug("runing api")
    try:
      api(is_debug, args.get("port"), controller)
      exit(0)
    except Error as e:
      cli_logger.error(e.get_pretty())
      exit(1)

  def list_routers(args):
    cli_logger.debug("listing routers")
    try:
      routers = controller.get_router_list(args.get("mechanism"), domain_id)
      print("👍  || router list")
      for rtr, state in routers.items():
        print("➕  || router id: \033[1m{}\033[0m || router state: \033[1m{}\033[0m".format(rtr, state))
      exit(0)
    except Error as e:
      cli_logger.error(e.get_pretty())
      exit(1)

  def check_state(args):
    cli_logger.debug("checking state")
    try:
      state = controller.get_router_state(args.get("mechanism"), domain_id, args.get("router_id"))
      print("👍  || router state || \033[1m{}\033[0m".format(state))
      exit(0)
    except Error as e:
      cli_logger.error(e.get_pretty())
      exit(1)

  def check_config(args):
    cli_logger.debug("checking config")

  def install_config(args):
    logging.debug("installing config")
    try:
      name = args.get("config-path") if args.get("name") == None else args.get("name")[0]
      rid = controller.install_from_file(args.get("mechanism"), domain_id, args.get("config-path"), name)
      print("👍  || router has been created || \033[1m{}\033[0m".format(rid))
      if args.get("s"):
        controller.start_router(args.get("mechanism"), domain_id, rid)
        print("👍  || router started || \033[1m{}\033[0m".format(rid))
      exit(0)
    except Error as e:
      cli_logger.error(e.get_pretty())
      exit(1)

  def remove_router(args):
    cli_logger.debug("removing router")
    try:
      controller.remove_router(args.get("mechanism"), domain_id, args.get("router_id"), args.get("f"))
      print("👍  || router has been removed || \033[1m{}\033[0m".format(args.get("router_id")))
      exit(0)
    except Error as e:
      cli_logger.error(e.get_pretty())
      exit(1)

  def start_router(args):
    cli_logger.debug("starting router")
    try:
      rid = controller.start_router(args.get("mechanism"), domain_id, args.get("router_id"))
      print("👍  || router started || \033[1m{}\033[0m".format(rid))
      exit(0)
    except Error as e:
      cli_logger.error(e.get_pretty())
      exit(1)

  def stop_router(args):
    cli_logger.debug("stopping router")
    try:
      rid = controller.stop_router(args.get("mechanism"), domain_id, args.get("router_id"))
      print("👍  || router stopped || \033[1m{}\033[0m".format(rid))
      exit(0)
    except Error as e:
      cli_logger.error(e.get_pretty())
      exit(1)

  def get_handler(args):
    cli_logger.debug("getting handler")
    try:
      data = controller.get_elem_handler(args.get("mechanism"), domain_id, args.get("router_id"), args.get("element"), args.get("handler"))
      print("👍  || data grabbed || \033[1m{}\033[0m".format(data))
      exit(0)
    except Error as e:
      cli_logger.error(e.get_pretty())
      exit(1)

  def print_version():
    cli_logger.debug("printing version")
    print("👀  ||| Unimon Control Version ||| \033[1m{}\033[0m".format(controller.get_version()))

  # Args
  parser = argparse.ArgumentParser(description="Control ClickOS Xen Domains")

  # - Top Level
  parser.add_argument('domain_id', type=int, nargs=1, help="the xen domain id running a clickos image")
  parser.add_argument('--mechanism', type=str, default=controller.DEFAULT_COM_MECH, help="what mechanism to use for inter-domain communication (default: %(default)s)")
  parser.add_argument('--debug', action='store_true', help="enable debug level logging")
  parser.add_argument('--version', action='store_true', help="print the version")
  subparsers = parser.add_subparsers(help='sub-command help')
  api_parser = subparsers.add_parser('api', help="run the unimon-ctl api")
  list_parser = subparsers.add_parser('list', help="get a list of all clickos routers present on a domain")
  state_parser = subparsers.add_parser('state', help="get the state of clickos router")
  check_parser = subparsers.add_parser('config', help="get the current config name on a clickos router")
  install_parser = subparsers.add_parser('install', help="install a click config to a clickos xen domain")
  remove_parser = subparsers.add_parser('remove', help="remove click router from clickos domain")
  start_parser = subparsers.add_parser('start', help="start a clickos router")
  stop_parser = subparsers.add_parser('stop', help="stop a clickos router")
  handler_parser = subparsers.add_parser('handler', help="get an elements handler value")

  # -- API
  api_parser.add_argument('--port', type=int, default=8080, help="the port to tun the api over")
  api_parser.set_defaults(func=run_api)

  # -- List
  list_parser.set_defaults(func=list_routers)

  # -- State
  state_parser.add_argument('router_id', type=int, help="the id of the target clickos router")
  state_parser.set_defaults(func=check_state)

  # -- Config Check
  check_parser.add_argument('router_id', type=int, help="the id of the target clickos router")
  check_parser.set_defaults(func=check_config)

  # -- Install
  install_parser.add_argument('config-path', type=str, help="the path of the .click file to use as the config")
  install_parser.add_argument('--name', type=str, nargs=1, help="add a friendly name for the router config")
  install_parser.add_argument('-s', action='store_true', help="once config installed, start the clickos router")
  install_parser.set_defaults(func=install_config)

  # -- Remove
  remove_parser.add_argument('router_id', type=int, help="the id of the target router")
  remove_parser.add_argument('-f', action='store_true', help="if router is still running, it will be stopped")
  remove_parser.set_defaults(func=remove_router)

  # -- Start
  start_parser.add_argument('router_id', type=int, help="the id of the target clickos router")
  start_parser.set_defaults(func=start_router)

  # -- Stop
  stop_parser.add_argument('router_id', type=int, help="the id of the target clickos router")
  stop_parser.set_defaults(func=stop_router)

  # -- Handler
  handler_parser.add_argument('router_id', type=int, help="the id of the target clickos router")
  handler_parser.add_argument('element', type=str, help="the name of the target element")
  handler_parser.add_argument('handler', type=str, help="the name of the target handler")
  handler_parser.set_defaults(func=get_handler)

  # Parse
  args = parser.parse_args()
  args_dict = vars(parser.parse_args())
  domain_id = args_dict.get("domain_id", -1)[0]
  if domain_id <= 0:
    logging.fatal("domain id must be greater than 0")
    exit(1)
  do_version = args_dict.get("version", False)
  if do_version:
    print_version()
  is_debug = args_dict.get("debug", False)
  if is_debug:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s || %(message)s')
    controller.set_debug()

  args.func(vars(parser.parse_args()))

main()

