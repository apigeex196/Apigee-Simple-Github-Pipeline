You have access to my workspace. Please fix a regression in the **new proxy discovery tool** by comparing it against the **old apigee discovery tool** and then make the code changes directly.

## Problem

The **new tool** returns only **1 empty proxy** from source `esp`, while the **old tool** returns **4997 proxies** for the same environment.

Observed behavior:

* Old tool returns all proxies correctly
* New tool inventory/security summary shows 1 proxy with empty fields like `proxyName` and `sysgen`

## Root cause already identified

The bug is in:

`proxy-discovery/tool/extractors/esp_client.py`

The new tool is not parsing the real ESP response shape correctly.

### Actual ESP response shape

The ESP API returns a wrapper object like:

```json
{
  "mediatedResource": [
    {
      "proxyName": "...",
      "sysgen": "...",
      ...
    }
  ]
}
```

### Current wrong behavior in new tool

The new tool checks for keys like:

* `items`
* `proxies`

and otherwise treats the whole response object as a single proxy:

```python
items = [data]
```

So instead of extracting `data["mediatedResource"]`, it passes the wrapper object downstream, which causes:

* only 1 item
* empty proxy fields
* broken inventory/security summary

## What I want you to do

### 1. Compare old and new ESP clients

Please inspect both files:

* `tools/apigee-discovery/extractors/esp_client.py`
* `proxy-discovery/tool/extractors/esp_client.py`

Understand how the old tool handles ESP responses and port the missing logic into the new tool.

### 2. Fix parsing in new ESP client

Update `proxy-discovery/tool/extractors/esp_client.py` so that `fetch_proxies()` supports these response shapes in this priority:

1. if response is a list → use it directly
2. if response is a dict with `mediatedResource` and it is a list → use `data["mediatedResource"]`
3. else if dict with `items` list → use `data["items"]`
4. else if dict with `proxies` list → use `data["proxies"]`
5. else if dict looks like a single proxy object (contains one of `resourceName`, `mediatedResourceId`, `name`, `proxyName`) → wrap in list
6. otherwise return empty list or raise a clear error, but do **not** treat the wrapper as a proxy

### 3. Restore environment-specific URL behavior from old tool

The old tool has special handling for `test1`. Port that behavior into the new tool.

Expected logic:

* if environment == `test1`, use base URL:
  `https://api-test1.test.intranet`
  and do not send `environment` as query param
* for other environments, use normal base URL and send `environment=<env>` as query param

### 4. Keep backward compatibility

Do not break existing support for:

* `items`
* `proxies`
* single-proxy dict payloads

### 5. Add lightweight debug logging

Add safe debug prints/logging around:

* response top-level keys
* detected response shape
* final extracted proxy count

But keep it minimal and not noisy.

### 6. Validate the fix

After code change, tell me:

* what exact file(s) changed
* what logic was added/removed
* what command I should run to retest

## Expected result

When I run the new tool with source `esp`, it should return the full proxy inventory instead of one empty proxy.

Example command I use:

```bash
python -X utf8 tool/discover.py inventory --env prod --out output --security-summary --source esp --insecure
```

## Important

* Make the actual code changes in the workspace
* Do not just explain
* Reuse the old tool’s proven logic where appropriate
* Keep the patch minimal and production-safe
* After editing, show me a short summary and the diff for the changed file
