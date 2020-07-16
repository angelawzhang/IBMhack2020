# ShopBlack
ShopBlack is a Chrome Extension that helps users find black owned alternatives to popular shopping sites.

### How To Use ShopBlack
1. Clone repo
2. Navigate to `chrome://extensions/`
3. Turn on developer mode
4. Select `Load unpacked` and navigate to the directory containing the manifest.json file
5. Viola! You have installed the extension

### How to use API
Currently, the API can be found hosted on IBM Cloud Foundry at [this link](https://ibm-hack-2020.stage1.mybluemix.net/)

"Businesses" as referred to below are objects of this format:

```json
{
    "type": "business", // hard-coded to always be this
    "name": "<business-name>",
    "domain": "mybusiness.com",
    "blackOwned": true, // or false
    "logo": "<url-to-logo>",
    "categories": [
        "clothing",
        "tech"
    ],
    "photos": [
        "<url-to-product-photo1>",
        "<url-to-product-photo2>",
        "<url-to-product-photo3>"
    ]
}
```

#### Routes

##### /business

* GET /business: fetches an array of all businesses in database

* GET /business/\<business-name\>: fetches a single business that matches the provided name

* POST /business: creates a business with the data provided in the request JSON body (must match business model above)
    * must have header `"Content-Type": "application/json"`


* DELETE /business/\<business-name\>: deletes a business matching the provided name

##### /domain:

* GET /domain/<domain-name>: used by the chrome extension: provide the domain name (domain apex, i.e. send `google.com` if you're on the page `maps.google.com/<some-path>`). The result will be a response of the following format:
```json
{
    "blackOwned": false, // or true
    "alternatives": [
        {
            // ... business object 1
        },
        {
            // ... business object 2
        }
        // ... etc.
    ] // if blackOwned == true, then alternatives will be empty, because the extension doesn't need a list of
    // alternatives if the current site is black-owned
}
```