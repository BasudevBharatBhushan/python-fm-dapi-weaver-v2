<h1 align="center">python-fm-dapi-weaver</h1><br>

A developer-friendly Python library for interacting with FileMaker Server via the FileMaker Data API. Connect your apps to FileMaker databases for streamlined data management, automation, and integration

## Table of Contents

- [Features](#features)
- [How to Install](#how-to-install)
- [How to Use](#how-to-use)
- [API Structure](#api-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Authentication**: Use **Basic Auth** for secure sign-in/sign-out and automatic session managements
- **CRUD Operations**: Perform **Create**, **Read**, **Update**, and **Delete** on FileMaker records.
- **File Uploads**: Upload files to FileMaker container fields using **multipart/form-data**.
- **Error Handling**: Includes robust error handling for API requests and responses.

## How to Install

You can install the package via pip:

```
pip install python-fm-dapi-weaver


```

## How to Use

After installing the package, you can start the server by following these steps:

### Start the FastAPI Server

To start the server, import the `start_server` function and call it as shown below:

```python
from python_fm_dapi_weaver.main import start_server

start_server()


```

### Custom Configuration

You can also start the server with custom host, port, and reload settings.

```
from python_fm_dapi_weaver.main import start_server

start_server(host="0.0.0.0", port=8080, reload=True)

```

### Parameters:

- **host** – IP address to bind the server (default is `127.0.0.1`)
- **port** – Port number to listen on (default is `8000`)
- **reload** – Enable auto-reloading of server on code changes (default is `False`)

## API Structure

### Endpoint

- `<serverURL>api/dataApi` 
  Example: `http://localhost:8000/api/dataApi`

### HTTP Method

- `POST`

### Authentication

> Must send **Basic Authentication credentials** in the headers for each request.  The `Authorization` header must contain the FileMaker Database **username** and **password** encoded in **Base64**.

### Body Structure

```
{
    "fmServer": "<IpAddress>",
    "method": "<methodName>",
    "methodBody": {<method specific body>},
    "session": {
        "token": "<sessionToken>",
        "required": <true/false>
    }
}

```

## Method Examples

### 1. **Signin** 

Used for signing into the FileMaker database.

```
{
    "fmServer": "<IpAddress>",
    "method": "signin",
    "methodBody": {
       
        "database": "<Filemaker_Filename>"
    },
    "session": {
        "token": "",
        "required": ""
    }
}

```

### 2. **Signout** 

Used for signing out from the FileMaker server.

> The `session.token` should be the token received from the **Signin** method.

```
{
    "fmServer": "<IpAddress>",
    "method": "signout",
    "methodBody": {
        "database": "<Filemaker_Filename>"
    },
    "session": {
        "token": "<sessionToken>",  // Token received from the Signin method
        "required": <true/false>
    }
}
```

### 3. **Get All Records** 

Fetches all records from the specified layout, with pagination.

> The `session.token` should be the token received from the **Signin** method.

##### **Pagination Options (Optional):**

- **`offset`**: The starting point of records to fetch. If `offset` is provided (e.g., `1`), it will start fetching from the second record (indexing starts from 0). 
  Default: `0` (starts from the first record).
- **`limit`**: The maximum number of records to fetch. If `limit` is provided (e.g., `10`), it will fetch up to 10 records per request. 
  Default: No limit (all records will be fetched).

These fields are optional and can be omitted if you want to fetch all records without pagination.

Example:

- If `offset` is `1` and `limit` is `10`, it will fetch records from index 1 to 10 (inclusive).
- If neither `offset` nor `limit` is specified, it will fetch all available records.

```
{
    "fmServer": "<IpAddress>",
    "method": "getAllRecords",
    "methodBody": {
        "database": "<Filemaker_Filename>",
        "layout": "<Layout_Name>",
        "offset": "1",  // Optional - Starting from the second record
        "limit": 10     // Optional - Fetch up to 10 records
    },
    "session": {
        "token": "<sessionToken>",  // Token received from the Signin method
        "required": <true/false>
    }
}

```

### 4. **Create Record** 

Used for creating a new product record in a specified FileMaker layout.

> The `session.token` should be the token received from the **Signin** method.

##### **Product Record Fields:**

The fields in the `record` object should match the product-related field names in the FileMaker layout. Example fields might include `ProductName`, `ProductCode`, `Price`, `Quantity`, etc.

Example:

```
{
    "fmServer": "<IpAddress>",
    "method": "createRecord",
    "methodBody": {
        "database": "<Filemaker_Filename>",
        "layout": "<Layout_Name>",  // The layout that holds the product records
        "record": {
            "ProductName": "Laptop",     // Example product name
            "ProductCode": "LP123",      // Example product code
            "Price": "1200",             // Example product price
            "Quantity": "50"             // Example quantity in stock
        }
    },
    "session": {
        "token": "<sessionToken>",  // Token received from the Signin method
        "required": <true/false>
    }
}

```

### 5. **Delete Record** 

Used for deleting a record from a specified FileMaker layout.

> The `session.token` should be the token received from the **Signin** method.

##### **Record Deletion:**

You need to specify the **recordId** of the record you want to delete. The `recordId` refers to the unique identifier for the record in the FileMaker layout.

Example:

```
{
    "fmServer": "<IpAddress>",
    "method": "deleteRecord",
    "methodBody": {
        "database": "<Filemaker_Filename>",
        "layout": "<Layout_Name>",  // The layout from which the record will be deleted
        "recordId": "<Record_ID>"   // The unique ID of the record to delete
    },
    "session": {
        "token": "<sessionToken>",  // Token received from the Signin method
        "required": <true/false>
    }
}

```

### 6. **Update Record** 

Used for updating an existing record in a specified FileMaker layout.

> The `session.token` should be the token received from the **Signin** method.

##### **Record Update:**

You need to specify the **recordId** of the record you want to update. The fields in the `record` object should match the field names in the FileMaker layout, and they should be updated with the new values.

Example:

```
{
    "fmServer": "<IpAddress>",
    "method": "updateRecord",
    "methodBody": {
        "database": "<Filemaker_Filename>",
        "layout": "<Layout_Name>",  // The layout in which the record will be updated
        "recordId": "<Record_ID>",  // The unique ID of the record to update
        "record": {
            "ProductName": "Updated Laptop",   // Updated product name
            "ProductCode": "LP1234",           // Updated product code
            "Price": "1300",                   // Updated price
            "Quantity": "40"                   // Updated quantity
        }
    },
    "session": {
        "token": "<sessionToken>",  // Token received from the Signin method
        "required": <true/false>
    }
}

```

### 7. **Find Record** 

Used for finding specific records in a specified FileMaker layout.

> The `session.token` should be the token received from the **Signin** method.

##### **Search Criteria:**

You can specify search criteria in the `query` field. Each query defines the fields you want to search for and the values to match. You can also apply sorting and specify scripts to run.

##### **Query Options:**

- **`query`**: Define search criteria. Each object inside the query array represents a field-value pair that you want to search for.
- **`sort`**: (Optional) Specify sorting order based on a field, e.g., `CreationTimestamp`.
- **`scripts`**: (Optional) Specify FileMaker scripts to be executed during the search.
- **`limit`**: (Optional) Limit the number of records returned.
- **`offset`**: (Optional) Define the starting point for pagination.

Example:

```
{
    "fmServer": "<IpAddress>",
    "method": "findRecord",
    "methodBody": {
        "database": "<Filemaker_Filename>",
        "layout": "<Layout_Name>", 
        "offset": "1",              // Optional
        "limit": "10",              // Optional
        "query": [
            {"ProductName": "=Laptop"},   // Search for records where ProductName equals "Laptop"
            {"Price": ">1000"}            // Search for records where Price is greater than 1000
        ],
        "sort": [
            {"fieldName": "CreationTimestamp", "sortOrder": "ascend"} 
        ],
        "scripts": {
            "script": "<FM_Script_Name>",              
            "script.param": "<Script_Param>"           
        }
    },
    "session": {
        "token": "<sessionToken>",  // Token received from the Signin method
        "required": <true/false>
    }
}

```

### 8. **Upload Container**

Used for uploading a container field (e.g., an image or file) to a specified record in a FileMaker layout.

> The `session.token` should be the token received from the **Signin** method.

##### **Required Parameters for Upload:**

- **`database`**: The name of the FileMaker database where the container field resides.
- **`layout`**: The layout that contains the record with the container field.
- **`recordId`**: The unique ID of the record that will hold the uploaded file.
- **`fieldName`**: The name of the container field in which the file will be stored.
- **`file`**: The actual file to upload (this is typically included as a part of the request body, but the example provided does not show the file).

##### **Example for Uploading a File Using `multipart/form-data` with Generic Data:**

```
curl --location 'http://<Api Server>/api/dataApi' \
--header 'Authorization: Basic <Base64(username:password)>' \
--form 'method="uploadContainer"' \
--form 'data={
    "fmServer": "<IpAddress>",
    "database": "DatabaseName",
    "layout": "LayoutName",
    "recordId": "1",
    "fieldName": "ContainerFieldName",
    "sessionToken": "Session-token"
}' \
--form 'file=@"/path/to/your/file.jpg"'  # path to the file you want to upload



```

## Contributing

We appreciate and encourage community involvement!  
If you're interested in contributing to the `python-fm-dapi-weaver`,for detailed instructions on how to set up the development environment and contribute to the project, please refer to our [CONTRIBUTING.md](CONTRIBUTING.md).

## License

&copy; Mindfire Digital LLP. All rights reserved.

This project is licensed under the [MIT License](LICENSE).
