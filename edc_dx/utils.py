from __future__ import annotations

from typing import Any

from django.conf import settings


class DiagnosisLabelError(Exception):
    pass


try:
    getattr(settings, "EDC_DX_LABELS")
except AttributeError as e:
    raise AttributeError(
        f"{e}. Expected something like `EDC_DX_LABELS=dict"
        "(hiv=HIV,dm=Diabetes,htn=Hypertension,chol=High Cholesterol)`"
    )


# def calculate_dx_date_if_estimated(
#     dx_date: date | None,
#     dx_ago: str | None,
#     report_datetime: datetime | None,
# ) -> Tuple[date, date]:
#     if dx_ago and not dx_date:
#         dx_estimated_date = duration_to_date(dx_ago, report_datetime)
#         dx_date_is_estimated = YES
#     else:
#         dx_estimated_date = None
#         dx_date_is_estimated = NO
#     return dx_estimated_date, dx_date_is_estimated


def get_diagnosis_labels() -> dict:
    try:
        diagnosis_labels = getattr(settings, "EDC_DX_LABELS")
    except AttributeError as e:
        raise AttributeError(
            f"{e}. Expected something like `EDC_DX_LABELS=dict"
            "(hiv=HIV,dm=Diabetes,htn=Hypertension,chol=High Cholesterol)`"
        )

    return {k.lower(): v for k, v in diagnosis_labels.items()}


def get_diagnosis_labels_prefixes() -> list[str]:
    return [k for k in get_diagnosis_labels()]


def raise_on_unknown_diagnosis_labels(obj: Any, fld_suffix: str, fld_value: Any) -> None:
    """Raises an exception if a diagnosis field has a response
    but is not an expected condition.

    See also EDC_DX_LABELS.
    """
    labels = [
        fld.name.split(fld_suffix)[0]
        for fld in obj._meta.get_fields()
        if fld.name.endswith(fld_suffix)
        and fld.name.split(fld_suffix)[0] not in get_diagnosis_labels_prefixes()
        and getattr(obj, fld.name) == fld_value
    ]
    if labels:
        raise DiagnosisLabelError(
            "Diagnosis prefix not expected. See settings.EDC_DX_LABELS. "
            f"Expected one of {get_diagnosis_labels_prefixes()}. Got {labels}."
        )
