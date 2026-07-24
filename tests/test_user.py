import responses
from pygenezys.client import GenezysClient

USER_URL = "https://app.genezys.xyz/api-prod-user-service/users/connected"

FAKE_USER_RESPONSE = {
    "message": "user found",
    "data": {
        "pseudo": "TestPlayer",
        "preferredLanguage": "FR",
        "email": "test@example.com",
        "id": "test-user-id-123",
        "ownReferral": "FAKECODE01",
        "contactInfo": {
            "address1": "",
            "address2": "",
            "city": "",
            "contactEmail": "test@example.com",
            "firstName": "",
            "lastName": "",
            "phone": "",
            "zipCode": ""
        },
        "usedReferral": {
            "firstDistributionState": "done",
            "id": "00000000-0000-0000-0000-000000000000",
            "code": "FAKECODE02",
            "type": "points-program"
        },
        "points": {
            "nbGems": 100,
            "tokensToClaim": {
                "canBeRefreshAfter": "2026-01-01T00:00:00.000Z",
                "latestClaimedTokenPeriodId": "00000000-0000-0000-0000-000000000001",
                "latestCountedTokenPeriodId": "00000000-0000-0000-0000-000000000002",
                "nbActivityPointsOnGoingPeriod": 10,
                "nbActivityPointsWaitingClaim": 5,
                "nbTokens": 3
            },
            "activityPoints": 1000.0,
            "nbPoints": 2000.0,
            "referralCode": "FAKECODE01",
            "nbTokens": 500.0,
            "id": "test-user-id-123"
        },
        "tutorial": {
            "forceTutorial": False,
            "scenarios": [
                {
                    "scenarioId": "getting-started",
                    "completed": True,
                    "completedAt": "2026-01-01T00:00:00.000Z",
                    "rewarded": True
                }
            ]
        },
        "userDetails": {
            "sportsFollowed": ["football"],
            "ageRange": "18-24",
            "rewarded": True,
            "userId": "test-user-id-123",
            "region": "test-region",
            "completedAt": "2026-01-01T00:00:00.000Z",
            "sex": "unspecified",
            "sportsPracticed": ["football"]
        }
    }
}


@responses.activate
def test_get_username(client):
    responses.add(responses.GET, USER_URL, json=FAKE_USER_RESPONSE, status=200)
    assert client.user.get_username() == "TestPlayer"


@responses.activate
def test_get_user_id(client):
    responses.add(responses.GET, USER_URL, json=FAKE_USER_RESPONSE, status=200)
    assert client.user.get_user_id() == "test-user-id-123"


@responses.activate
def test_get_gnz(client):
    responses.add(responses.GET, USER_URL, json=FAKE_USER_RESPONSE, status=200)
    assert client.user.get_gnz() == 500


@responses.activate
def test_get_all_info(client):
    responses.add(responses.GET, USER_URL, json=FAKE_USER_RESPONSE, status=200)
    assert client.user.get_all_info() == FAKE_USER_RESPONSE
