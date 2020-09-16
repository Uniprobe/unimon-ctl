from .errors import Error
from .controller import UnimonControl
from .version import __version__
from flask import Flask, request, jsonify
import json
import logging

API_BASE = "/api/v1"

DEFAULT_MECH = ""

def api(debug, port, mechanism, controller):
  logger = logging.getLogger("api")
  logger.setLevel(logging.DEBUG)
  DEFAULT_MECH = mechanism

  app = Flask('unimon-ctl')
  app.config["DEBUG"] = debug

  @app.route(API_BASE, methods=['GET'])
  def help():
    logger.debug("📩  || api request for help")
    commands = {
      "version": "get the version of unimon-ctl",
      "domain_id/list": "get a list of all clickos routers on a domain",
      "domain_id/router_id/state": "get the state of a given clickos router"
    }
    body = jsonify(commands)
    return body, 200

  @app.route(API_BASE+"/version", methods=['GET'])
  def version():
    logger.debug("📩  || api request for get version")
    version = {
      "app": "unimon-ctl",
      "version": __version__
    }
    body = jsonify(version)
    return body, 200

  @app.route(API_BASE+"/<int:domain_id>/list", methods=['GET'])
  def list_routers(domain_id):
    logger.debug("📩  || api request for list routers")
    try:
      mechanism = request.args.get("mechanism", DEFAULT_MECH)
      routers = controller.get_router_list(mechanism, domain_id)
      return jsonify(routers), 200
    except Error as e:
      logger.error(e.get_pretty())
      return e.get_json()

  @app.route(API_BASE+"/<int:domain_id>/<int:router_id>/state", methods=['GET'])
  def router_state(domain_id, router_id):
    logger.debug("📩  || api request for get router state")
    try:
      mechanism = request.args.get("mechanism", DEFAULT_MECH)
      state = controller.get_router_state(mechanism, domain_id, router_id)
      return jsonify({"state": state}), 200
    except Error as e:
      logger.error(e.get_pretty())
      return e.get_json()

  @app.route(API_BASE+"/<int:domain_id>/<int:router_id>/start", methods=['GET'])
  def start_router(domain_id, router_id):
    logger.debug("📩  || api request for start router")
    try:
      mechanism = request.args.get("mechanism", DEFAULT_MECH)
      rid = controller.start_router(mechanism, domain_id, router_id)
      return jsonify({"message": "router {} started".format(rid)}), 200
    except Error as e:
      logger.error(e.get_pretty())
      return e.get_json()

  @app.route(API_BASE+"/<int:domain_id>/<int:router_id>/stop", methods=['GET'])
  def stop_router(domain_id, router_id):
    logger.debug("📩  || api request for stop router")
    try:
      mechanism = request.args.get("mechanism", DEFAULT_MECH)
      rid = controller.stop_router(mechanism, domain_id, router_id)
      return jsonify({"message": "router {} stopped".format(rid)}), 200
    except Error as e:
      logger.error(e.get_pretty())
      return e.get_json()

  @app.route(API_BASE+"/<int:domain_id>/<int:router_id>/remove", methods=['GET'])
  def remove_router(domain_id, router_id):
    logger.debug("📩  || api request for remove router")
    try:
      mechanism = request.args.get("mechanism", DEFAULT_MECH)
      force = request.args.get("force", False)
      if not isinstance(force, bool):
        force = False
      controller.remove_router(mechanism, domain_id, router_id, force=force)
      return jsonify({"message": "router removed"}), 200
    except Error as e:
      logger.error(e.get_pretty())
      return e.get_json()

  @app.route(API_BASE+"/<int:domain_id>/install", methods=['GET'])
  def install_router(domain_id, router_id):
    logger.debug("📩  || api request for install router")
    try:
      mechanism = request.args.get("mechanism", DEFAULT_MECH)
      name = request.args.get("name", DEFAULT_MECH)
      if not isinstance(force, bool):
        force = False
      controller.remove_router(mechanism, domain_id, router_id, force=force)
      return jsonify({"message": "router removed"}), 200
    except Error as e:
      logger.error(e.get_pretty())
      return e.get_json()
    

  logger.debug("💬  || running api")
  app.run(host='0.0.0.0', port=port)