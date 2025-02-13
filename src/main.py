from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from requests import get as requests_get
from enum import Enum


app = FastAPI(
    title="LRS Connector",
    description="LRS Connector is a lightweight FastAPI application designed to act as a proxy for querying Learning Record Stores (LRS) such as Learning Locker or Ralph, from the DataSpace.",
    version="0.0.1",
)


class LRSEnum(str, Enum):
    learninglocker = "learninglocker"
    ralph = "ralph"

XAPI_ENDPOINT = 'X-Experience-API-Endpoint'
XAPI_LRS = 'X-Experience-API-LRS'


# Dépendance pour vérifier la présence et le remplissage des en-têtes requis
def verify_headers(request: Request):
    if not request.headers.get(XAPI_ENDPOINT) or not request.headers.get(XAPI_LRS):
        raise HTTPException(status_code=400, detail="Missing required headers.")


@app.get("/statements", dependencies=[Depends(verify_headers)], tags=["statements"])
async def get_statements(request: Request):
    # Parse headers
    headers = dict(request.headers)
    headers.pop("host", None)

    which_lrs: LRSEnum = headers.pop(XAPI_LRS.lower(), LRSEnum.learninglocker)

    # Change xAPI path depending on the LRS, default to Learning Locker
    if which_lrs == LRSEnum.learninglocker:
        xapi_base_path = "/data/xAPI/statements"
    elif which_lrs == LRSEnum.ralph:
        xapi_base_path = "/xAPI/statements"
    else:
        xapi_base_path = "/data/xAPI/statements"

    # Build the URL dynamically
    try:
        lrs_base_url = headers.get(XAPI_ENDPOINT.lower())
        api_url = f"{lrs_base_url}{xapi_base_path}" + (f"?{str(request.query_params)}" if str(request.query_params) else "")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Couldn't build the URL") from e

    accumulated_statements = []
    # Fetch data from the LRS, paginating if necessary
    while api_url:
        # Fetch data from the LRS
        try:
            response = requests_get(url=api_url, headers=headers)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Couldn't fetch data from the LRS") from e

        # Check if the response is valid
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        # Parse the response
        try:
            fetched_data = response.json()
            accumulated_statements.extend(fetched_data.get("statements", []))
            more = fetched_data.get("more")
            api_url = more if more and more.startswith("http") else f"{lrs_base_url}{more}" if more else None
        except Exception as e:
            raise HTTPException(status_code=500, detail="Couldn't parse the response from the LRS") from e

    return JSONResponse(accumulated_statements)
