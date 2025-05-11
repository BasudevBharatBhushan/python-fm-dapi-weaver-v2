from fastapi import FastAPI, Request, Response
from .auth import validate_session, validate_token,signin,signout
from .records import (
    create_record,
    get_all_records,
    find_record,
    update_record,
    delete_record,
    upload_container
)

# List of method names that do not require token/session validation.
controllers_to_skip_validation = ["signin"]


# Mapping of method names to their corresponding handler functions
METHOD_HANDLERS = {
    "createRecord": create_record,
    "getAllRecords": get_all_records,
    "findRecord": find_record,
    "updateRecord": update_record,
    "deleteRecord": delete_record,
    "signin": signin,
    "signout" : signout,
    "uploadContainer":upload_container
    
}


async def data_api(req: Request, res: Response):
    method = req.state.body.get("method")
    if method not in METHOD_HANDLERS:
        return {"error": f"Invalid method ${method}"}
    if method not in controllers_to_skip_validation:
        # If the method is not in the skip list, apply the validateToken  first
        await validate_token(req)        
        # After token validation, apply the validateSession middleware
        await validate_session(req)
               
    handler = METHOD_HANDLERS[method]
    return await handler(req)

