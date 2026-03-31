from typing import Dict


STATE_TO_FUEL_PRICE_REGION: Dict[str, str] = {
    "CT": "New England",
    "ME": "New England",
    "MA": "New England",
    "NH": "New England",
    "RI": "New England",
    "VT": "New England",
    "NJ": "Middle Atlantic",
    "NY": "Middle Atlantic",
    "PA": "Middle Atlantic",
    "IL": "East North Central",
    "IN": "East North Central",
    "MI": "East North Central",
    "OH": "East North Central",
    "WI": "East North Central",
    "IA": "West North Central",
    "KS": "West North Central",
    "MN": "West North Central",
    "MO": "West North Central",
    "NE": "West North Central",
    "ND": "West North Central",
    "SD": "West North Central",
    "DE": "South Atlantic",
    "DC": "South Atlantic",
    "FL": "South Atlantic",
    "GA": "South Atlantic",
    "MD": "South Atlantic",
    "NC": "South Atlantic",
    "SC": "South Atlantic",
    "VA": "South Atlantic",
    "WV": "South Atlantic",
    "AL": "East South Central",
    "KY": "East South Central",
    "MS": "East South Central",
    "TN": "East South Central",
    "AR": "West South Central",
    "LA": "West South Central",
    "OK": "West South Central",
    "TX": "West South Central",
    "AZ": "Mountain",
    "CO": "Mountain",
    "ID": "Mountain",
    "MT": "Mountain",
    "NM": "Mountain",
    "NV": "Mountain",
    "UT": "Mountain",
    "WY": "Mountain",
    "AK": "Pacific",
    "CA": "Pacific",
    "HI": "Pacific",
    "OR": "Pacific",
    "WA": "Pacific",
}


def resolve_fuel_price_region_from_zipcode(zipcode: str) -> str:
    """
    Resolves a 5-digit US zipcode to the configured fuel price region.
    """
    zipcode_details = lookup_zipcode(zipcode)
    state_code = zipcode_details.get("state")
    if not state_code:
        raise ValueError(f"Zipcode '{zipcode}' could not be resolved to a US state")

    try:
        return STATE_TO_FUEL_PRICE_REGION[state_code]
    except KeyError as exc:
        raise ValueError(
            f"Zipcode '{zipcode}' resolved to unsupported state '{state_code}'"
        ) from exc


def lookup_zipcode(zipcode: str) -> dict:
    """
    Uses the external zipcode dataset to resolve a US zipcode record.
    """
    try:
        import zipcodes
    except ImportError as exc:
        raise ImportError(
            "The 'zipcodes' package is required for zipcode-based fuel price overrides. "
            "Install T3CO with its default dependencies to enable this feature."
        ) from exc

    matches = zipcodes.filter_by(zipcodes.list_all(), zip_code=zipcode)
    if not matches:
        raise ValueError(f"Zipcode '{zipcode}' was not found in the zipcode dataset")

    return matches[0]
