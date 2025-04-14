from flask import Flask, request, jsonify
import requests
import grpc
import credit_decision_pb2
import credit_decision_pb2_grpc
import random

app = Flask(__name__)

IDENTITY_VERIFICATION_URL = "http://identity-verification:5002/verify-identity"
# IDENTITY_VERIFICATION_URL = "http://localhost:5002/verify-identity"

@app.route('/process-application', methods=['POST'])
def process_application():
    data = request.json
    applicant_info = data.get('applicant_info')
    identity_data = "iddata"

    # Step A: Identity Verification
    print(f">> Performing identity verification for : {applicant_info}")
    identity_response = requests.post(IDENTITY_VERIFICATION_URL, json={"applicant_info": applicant_info})
    print(f">> Identity verification response: {identity_response.status_code}, {identity_response.text}")
    identity_data = identity_response.json()

    if not identity_data.get('verified'):
        return jsonify({
            'status': 'rejected',
            'reason': f"Identity verification failed: {identity_data.get('reason')}"
        }), 400

    # Step B: Credit Decision
    enrich_applicant_info(applicant_info)
    print(f">> Performing Credit decision for : {applicant_info}, {identity_data}")
    with grpc.insecure_channel('credit-decision:5005') as channel:
#    with grpc.insecure_channel('localhost:5005') as channel:
        stub = credit_decision_pb2_grpc.CreditDecisionServiceStub(channel)
        print(">> Created gRPC channel")
        request_msg = credit_decision_pb2.CreditDecisionRequest(
            applicant_id = applicant_info["applicant_id"], 
            income = applicant_info["income"],
            loan_amount= applicant_info["loan_amount"],
            credit_history= applicant_info["credit_history"],
            delinquencies= applicant_info["delinquencies"] 
        )
        print(f">> Sending Credit decision request: {request_msg}")
        credit_decision_response = stub.EvaluateApplication(request_msg)
        print(f">> Credit decision response: {credit_decision_response.status}, {credit_decision_response.reason}")
        return jsonify({
            "status": credit_decision_response.status,
            "interest_rate": credit_decision_response.interest_rate,
            "reason": credit_decision_response.reason
        })    

def enrich_applicant_info(applicant_info):
    applicant_info["loan_amount"] = random.randint(5000, 30000)
    applicant_info["delinquencies"] = random.randint(0, 5)
    applicant_info["credit_history"] = generate_credit_history()
    return applicant_info

def generate_credit_history():
    cr_history = random.choice(["excellent", "good", "fair", "poor"])
    credit_score = 0
    if (cr_history == "excellent"):
        credit_score = 5
    elif (cr_history == "good"):
        credit_score = 3
    elif (cr_history == "fair"):
        credit_score = 2
    elif (cr_history == "poor"):
        credit_score = 1
    
    return credit_score

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)