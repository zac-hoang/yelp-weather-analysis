import json

def clean_unicode_string(val):
    if isinstance(val, str) and val.startswith("u'") and val.endswith("'"):
        return val[2:-1]  # Bỏ u' và '
    elif isinstance(val, str) and val.startswith("'") and val.endswith("'"):
        return val[1:-1]
    return val


def safe_parse_json(val):
    try:
        if isinstance(val, dict):
            return val
        elif isinstance(val, str):
            if val.strip().lower() in ["none", '"none"', "'none'"]:
                return None  # chuyển chuỗi 'None' thành null thật
            if val.startswith("{"):
                val = (
                    val.replace("None", "null")
                    .replace("False", "false")
                    .replace("True", "true")
                    .replace("u'", "'")
                    .replace("'", '"')
                )
                return json.loads(val)
    except Exception:
        return None
    return val

def clean_boolean(val):
    if isinstance(val, str):
        val_lower = val.strip().lower()
        if val_lower in ["true", "'true'", '"true"']:
            return True
        elif val_lower in ["false", "'false'", '"false"']:
            return False
        elif val_lower in ["none", '"none"', "'none'", 'null', '"null"']:
            return None
    elif isinstance(val, bool):
        return val
    elif val is None:
        return None
    return None  # fallback cho các trường hợp khác


