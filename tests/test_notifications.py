from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from mini_store.notifications import NotificationService


def make_customer(channel: str):
    return SimpleNamespace(
        name="Ana",
        preferred_channel=channel,
        email="ana@example.com",
        phone="+521234567890",
        device_id="device-1",
    )


def test_email_order_confirmation_is_sent():
    email = Mock()
    service = NotificationService(email, Mock(), Mock())

    service.send_order_confirmation(make_customer("email"), "A-100")

    email.send.assert_called_once_with(
        "ana@example.com",
        "Order A-100 confirmed",
        "Hello Ana, your order A-100 was confirmed.",
    )


def test_sms_shipping_update_is_sent():
    sms = Mock()
    service = NotificationService(Mock(), sms, Mock())

    service.send_shipping_update(make_customer("sms"), "A-100", "TRACK-9")

    sms.send.assert_called_once_with(
        "+521234567890",
        "Order A-100 shipped. Tracking: TRACK-9.",
    )


def test_email_order_confirmation():
    email = Mock()
    service = NotificationService(email, Mock(), Mock())

    service.send_order_confirmation(make_customer("email"), "B-200")

    email.send.assert_called_once()

def test_sms_shipping_update():
    sms = Mock()
    service = NotificationService(Mock(), sms, Mock())

    service.send_shipping_update(make_customer("sms"), "B-200", "TRACK-25")

    sms.send.assert_called_once()

def test_email_is_not_sent_for_sms_customer():
    email = Mock()
    service = NotificationService(email, Mock(), Mock())

    service.send_shipping_update(make_customer("sms"), "A-100", "TRACK-9")

    email.send.assert_not_called()

# --- AI-assisted pass: lock down every channel x message combination ---

def make_service():
    email, sms, push = Mock(), Mock(), Mock()
    return NotificationService(email, sms, push), email, sms, push


def test_sms_order_confirmation_is_sent():
    service, email, sms, push = make_service()

    service.send_order_confirmation(make_customer("sms"), "A-100")

    sms.send.assert_called_once_with("+521234567890", "Order A-100 confirmed for Ana.")
    email.send.assert_not_called()
    push.send.assert_not_called()


def test_push_order_confirmation_is_sent():
    service, email, sms, push = make_service()

    service.send_order_confirmation(make_customer("push"), "A-100")

    push.send.assert_called_once_with("device-1", "Order confirmed", "Order A-100 is confirmed.")
    email.send.assert_not_called()
    sms.send.assert_not_called()


def test_email_shipping_update_is_sent():
    service, email, sms, push = make_service()

    service.send_shipping_update(make_customer("email"), "A-100", "TRACK-9")

    email.send.assert_called_once_with(
        "ana@example.com",
        "Order A-100 shipped",
        "Hello Ana, your order A-100 shipped. Tracking: TRACK-9.",
    )
    sms.send.assert_not_called()
    push.send.assert_not_called()


def test_push_shipping_update_is_sent():
    service, email, sms, push = make_service()

    service.send_shipping_update(make_customer("push"), "A-100", "TRACK-9")

    push.send.assert_called_once_with("device-1", "Order shipped", "Track order A-100: TRACK-9.")
    email.send.assert_not_called()
    sms.send.assert_not_called()


@pytest.mark.parametrize(
    "send",
    [
        lambda service, customer: service.send_order_confirmation(customer, "A-100"),
        lambda service, customer: service.send_shipping_update(customer, "A-100", "TRACK-9"),
    ],
    ids=["order_confirmation", "shipping_update"],
)
def test_unsupported_channel_raises_and_sends_nothing(send):
    service, email, sms, push = make_service()

    with pytest.raises(ValueError, match="Unsupported notification channel"):
        send(service, make_customer("fax"))

    email.send.assert_not_called()
    sms.send.assert_not_called()
    push.send.assert_not_called()
