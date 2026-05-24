from flask import Flask, request, jsonify
from flask_cors import CORS
from central_runner import AgentRunner
from validation_layer import TaskValidator

app = Flask(__name__)
CORS(app)

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    task = data.get('task')
    domain = data.get('domain', 'engineering')
    
    # 1. Validate
    validator = TaskValidator()
    validation_status = validator.pre_flight_check(task)
    
    # 2. Execute
    runner = AgentRunner(domain)
    result = runner.execute_task(task)
    
    return jsonify({"status": validation_status, "result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
