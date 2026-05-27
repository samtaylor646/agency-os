from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from central_runner import DAGOrchestrator
from validation_layer import TaskValidator
from server.services.kill_switch import kill_switch

app = Flask(__name__)
CORS(app)

@app.route('/kill-switch/activate', methods=['POST'])
def activate_kill_switch():
    data = request.get_json() or {}
    tenant_id = data.get('tenant_id', 'GLOBAL')
    success = kill_switch.activate(tenant_id)
    return jsonify({"status": "activated" if success else "failed", "tenant_id": tenant_id})

@app.route('/kill-switch/deactivate', methods=['POST'])
def deactivate_kill_switch():
    data = request.get_json() or {}
    tenant_id = data.get('tenant_id', 'GLOBAL')
    success = kill_switch.deactivate(tenant_id)
    return jsonify({"status": "deactivated" if success else "failed", "tenant_id": tenant_id})

@app.route('/kill-switch/status', methods=['GET'])
def kill_switch_status():
    tenant_id = request.args.get('tenant_id', 'GLOBAL')
    is_active = kill_switch.is_active(tenant_id)
    return jsonify({"status": "active" if is_active else "inactive", "tenant_id": tenant_id})

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    task = data.get('task')
    domain = data.get('domain', 'engineering')
    
    # 1. Validate
    validator = TaskValidator()
    validation_status = validator.pre_flight_check(task)
    
    # 2. Execute
    runner = DAGOrchestrator('test_workflow')
    runner.add_node('1', 'TestAgent', task)
    import asyncio
    result = asyncio.run(runner.execute_workflow('1'))
    
    
    return jsonify({"status": validation_status, "result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
