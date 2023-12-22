from fastapi import FastAPI, Request, Response
from .auth import validate_session, validate_token
from .records import (
    create_record,
    get_all_records,
    find_record,
    update_record,
)

controllers_to_skip_validation = []


async def data_api(req: Request, res: Response):
    method = req.get("method")

    print("In this function", res.headers)

    # Check if the method should skip validation
    if method not in controllers_to_skip_validation:
        # If the method is not in the skip list, apply the validateToken middleware first
        await validate_token(req, res)
        
        # After token validation, apply the validateSession middleware
        await validate_session(req, res)

    # Once validated, call the appropriate controller method
    if method == "createRecord":
        return await create_record(req)
    # elif method == "getRecordById":
    #     return await get_record_by_id(req)
    elif method == "getAllRecords":
        return await get_all_records(req)
    elif method == "findRecord":
        return await find_record(req)
    # elif method == "executeScript":
    #     return await execute_script(req)
    elif method == "updateRecord":
        return await update_record(req)
    # elif method == "test":
    #     return await test(req)
    # elif method == "syncCollection":
    #     return await sync_collection(req)
    else:
        return {"error": "Invalid method"}
