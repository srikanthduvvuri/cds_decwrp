from behave import given, when, then
from app import app
import json
import requests_mock

@given("applicant provides fraudulent identity")
def step_given_fraud(context):
    context.payload = {"applicant_info": {"applicant_id": "001", "name": "Joe", "national_id": "0000000000"}}
    context.mock_identity = {"verified": False, "reason": "Fraud flagged by agency"}

@given("applicant provides valid identity")

def step_given_valid(context):
    context.payload = {"applicant_info": {"applicant_id": "002", "name": "Jane", "national_id": "1234567890"}}
    context.mock_identity = {"verified": True, "reason": "Identity verified successfully"}
    context.mock_credit = {"status": "approved", "interest_rate": 0.1, "reason": "All good"}

@when("process application is called")
def step_when_call(context):
    context.client = app.test_client()
    with requests_mock.Mocker() as mock:
        mock.post("http://identity-verification:5002/verify-identity", json=context.mock_identity)
        if context.mock_identity["verified"]:
            mock.post("http://credit-decision:5003/decide", json=context.mock_credit)
        context.response = context.client.post("/process-application", json=context.payload)

@then("application should be rejected with identity error")
def step_then_rejected(context):
    assert context.response.status_code == 400
    assert b"Fraud flagged by agency" in context.response.data

@then("application should be approved with interest rate")
def step_then_approved(context):
    assert context.response.status_code == 200
    data = context.response.get_json()
    assert data["status"] == "approved"
    assert data["interest_rate"] == 0.1