from .models import Event, IdempotencyKey
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

class ConcurrencyError(Exception):
    pass

def append_event(aggregate_id, aggregate_type, event_type, data, expected_version=None, metadata=None, idempotency_key=None):
    if metadata is None:
        metadata = {}
    # Idempotency: if key exists, return stored response
    if idempotency_key:
        ik, created = IdempotencyKey.objects.get_or_create(key=idempotency_key)
        if not created:
            return ik.response

    with transaction.atomic():
        last = Event.objects.filter(aggregate_id=aggregate_id).order_by("-version").first()
        current_version = last.version if last else 0
        if expected_version is not None and expected_version != current_version:
            raise ConcurrencyError(f"Expected {expected_version} but found {current_version}")
        next_version = current_version + 1
        ev = Event.objects.create(
            aggregate_id=aggregate_id,
            aggregate_type=aggregate_type,
            version=next_version,
            type=event_type,
            data=data,
            metadata=metadata or {}
        )
        if idempotency_key:
            ik.response = {"event_id": str(ev.id)}
            ik.save()
    return ev
