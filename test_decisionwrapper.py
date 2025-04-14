import json
from app import app
import requests_mock

def test_identity_verification_failure():
    with app.test_client() as client, requests_mock.Mocker() as mock:
        mock.post("http://identity-verification:5002/verify-identity", json={
            "verified": False,
            "reason": "Fraud flagged by agency"
        })
        payload = {"applicant_info": {"applicant_id": "001", "name": "Joe", "national_id": "0000000000"}}
        res = client.post("/process-application", json=payload)
        assert res.status_code == 400
        assert b"Fraud flagged by agency" in res.data

def test_full_credit_flow():
    with app.test_client() as client, requests_mock.Mocker() as mock:
        mock.post("http://identity-verification:5002/verify-identity", json={
            "verified": True,
            "reason": "Identity verified successfully"
        })
        mock.post("http://credit-decision:5003/decide", json={
            "status": "approved",
            "interest_rate": 0.1,
            "reason": "All good"
        })
        payload = {"applicant_info": {"applicant_id": "002", "name": "Jane", "national_id": "1234567890"}}
        res = client.post("/process-application", json=payload)
        assert res.status_code == 200
        data = res.get_json()
        assert data["status"] == "approved"
        assert data["interest_rate"] == 0.1