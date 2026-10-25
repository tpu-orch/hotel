from datetime import datetime, timezone

from app.core.rules import occupies_room, periods_overlap


def dt(day: int, hour: int = 12) -> datetime:
    return datetime(2026, 10, day, hour, tzinfo=timezone.utc)


def test_overlapping_periods():
    assert periods_overlap(dt(15), dt(18), dt(17), dt(20))


def test_new_period_inside_existing():
    assert periods_overlap(dt(15), dt(20), dt(16), dt(18))


def test_checkout_equals_next_checkin_is_not_overlap():
    # прежний гость выезжает в тот же момент, когда заезжает новый
    assert not periods_overlap(dt(12, 14), dt(15, 14), dt(15, 14), dt(18, 12))


def test_periods_far_apart():
    assert not periods_overlap(dt(1), dt(3), dt(10), dt(12))


def test_overlap_is_symmetric():
    assert periods_overlap(dt(15), dt(18), dt(17), dt(20)) == periods_overlap(
        dt(17), dt(20), dt(15), dt(18)
    )


def test_active_statuses_occupy_room():
    for status in ("RESERVATION_PENDING", "RESERVED", "CANCELLATION_PENDING"):
        assert occupies_room(status)


def test_inactive_statuses_do_not_occupy_room():
    for status in ("AVAILABLE", "CANCELLED"):
        assert not occupies_room(status)