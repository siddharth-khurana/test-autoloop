from datetime import datetime
from zoneinfo import ZoneInfo

from langchain_core.tools import tool

from app.autoloop import (
    search_leads,
    get_lead,
    create_lead,
)


@tool
def get_current_date():
    """
    Get today's date in India.
    Returns the date in YYYY-MM-DD format.
    """

    return datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).date().isoformat()


@tool
async def search_vehicle_leads(
    registration_number: str | None = None,
    lead_sequence: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    maker_id: int | None = None,
    model_id: int | None = None,
    status_id: int | None = None,
    stage_id: int | None = None,
):
    """
    Search vehicle leads in AutoLoop.

    Search can be performed using:
    - vehicle registration number
    - lead sequence
    - date range
    - maker ID
    - model ID
    - status ID
    - stage ID
    """

    return await search_leads(
        registration_number=registration_number,
        lead_sequence=lead_sequence,
        start_date=start_date,
        end_date=end_date,
        maker_id=maker_id,
        model_id=model_id,
        status_id=status_id,
        stage_id=stage_id,
    )


@tool
async def get_vehicle_lead(vehicle_lead_id: int):
    """
    Get complete details of a vehicle lead from AutoLoop
    using its vehicle lead ID.
    """

    return await get_lead(vehicle_lead_id)


@tool
async def create_vehicle_lead(
    registration_number: str,
    owner_name: str,
    mobile: str,
    email: str,
):
    """
    Create a new vehicle lead in AutoLoop.
    """

    return await create_lead(
        registration_number=registration_number,
        owner_name=owner_name,
        mobile=mobile,
        email=email,
    )