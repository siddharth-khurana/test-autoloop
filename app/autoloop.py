import os
import httpx
from dotenv import load_dotenv

load_dotenv()


AUTOLOOP_CLIENT_KEY = os.getenv("AUTOLOOP_CLIENT_KEY")
AUTOLOOP_CLIENT_SECRET = os.getenv("AUTOLOOP_CLIENT_SECRET")
AUTOLOOP_RVSF_ID = os.getenv("AUTOLOOP_RVSF_ID")
AUTOLOOP_RVSF_BRANCH_ID = os.getenv("AUTOLOOP_RVSF_BRANCH_ID")


TOKEN_URL = "https://userapi.theautoloop.ai/third-party-client/token"

SEARCH_URL = (
    "https://leadapi.theautoloop.ai/"
    "rvsf/lead/third-party/search"
)

SAVE_URL = (
    "https://leadapi.theautoloop.ai/"
    "rvsf/lead/third-party/save"
)

GET_URL = (
    "https://leadapi.theautoloop.ai/"
    "rvsf/lead/third-party/get"
)


async def get_autoloop_token():
    headers = {
        "rvsf_id": AUTOLOOP_RVSF_ID,
        "Content-Type": "application/json",
    }

    payload = {
        "third_party_client_key": AUTOLOOP_CLIENT_KEY,
        "third_party_client_secret_key": AUTOLOOP_CLIENT_SECRET,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            TOKEN_URL,
            headers=headers,
            json=payload,
        )

    response.raise_for_status()

    result = response.json()

    token = result.get("data", {}).get("access_token")

    if not token:
        raise RuntimeError(
            f"AutoLoop did not return an access token: {result}"
        )

    return token


def autoloop_headers(token: str):
    return {
        "Authorization": f"Bearer {token}",
        "rvsf_id": AUTOLOOP_RVSF_ID,
        "rvsf_branch_id": AUTOLOOP_RVSF_BRANCH_ID,
    }


async def search_leads(
    registration_number=None,
    lead_sequence=None,
    start_date=None,
    end_date=None,
    maker_id=None,
    model_id=None,
    status_id=None,
    stage_id=None,
):
    token = await get_autoloop_token()

    headers = {
        **autoloop_headers(token),
        "Content-Type": "application/json",
    }

    payload = {
        "lead_sequence": lead_sequence,
        "vehicle_registration_number": registration_number,
        "filterStartDate": start_date,
        "filterEndDate": end_date,
        "vehicle_category_id": None,
        "vehicle_maker_id": maker_id,
        "vehicle_model_id": model_id,
        "lead_creator_full_name": None,
        "lead_creator_mobile_number": None,
        "lead_status_id": status_id,
        "lead_stage_id": stage_id,
        "lead_type_id": None,
    }

    params = {
        "pageSize": 10,
        "pageNumber": 1,
        "orderByCol": "created_dt",
        "orderByDir": "desc",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            SEARCH_URL,
            headers=headers,
            params=params,
            json=payload,
        )

    response.raise_for_status()

    return response.json()


async def get_lead(vehicle_lead_id):
    token = await get_autoloop_token()

    headers = autoloop_headers(token)

    params = {
        "vehicle_lead_id": vehicle_lead_id,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            GET_URL,
            headers=headers,
            params=params,
        )

    response.raise_for_status()

    return response.json()


async def create_lead(
    registration_number,
    owner_name,
    mobile,
    email,
):
    token = await get_autoloop_token()

    headers = autoloop_headers(token)

    data = {
        "lead_section_id": "9",
        "is_for_submit": "true",
        "lead_type_id": "1",
        "source_id": "1",
        "lead_creator_full_name": owner_name,
        "lead_creator_mobile_number": mobile,
        "lead_creator_email_id": email,
        "rvsfVehicleDetails[0].vehicle_registration_number": (
            registration_number
        ),
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            SAVE_URL,
            headers=headers,
            data=data,
        )

    response.raise_for_status()

    return response.json()