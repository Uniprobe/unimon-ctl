from .errors import Error
from .controller import UnimonControl
from .version import __version__
from flask import Flask, request, jsonify
import json
import logging

API_BASE = "/api/v1"

def api(debug, port, controller):
  logger = logging.getLogger("api")
  logger.setLevel(logging.DEBUG)

  app = Flask('unimon-ctl')
  app.config["DEBUG"] = debug

  @app.route(API_BASE+"/version", methods=['GET'])
  def help():
    logger.debug("📩  || api request for help")
    commands = {
      "version": "get the version of unimon-ctl",
      "domain_id/list": "get a list of all clickos routers on a domain",
      "domain_id/router_id/state": "get the state of a given clickos router"
    }
    body = jsonify(version)
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
      mechanism = request.args.get("mechanism", controller.DEFAULT_COM_MECH)
      routers = controller.get_router_list(mechanism, domain_id)
      return jsonify(routers), 200
    except Error as e:
      logger.error(e.get_pretty())
      return e.get_json()
    

  logger.debug("💬  || running api")
  app.run(host='0.0.0.0', port=port)