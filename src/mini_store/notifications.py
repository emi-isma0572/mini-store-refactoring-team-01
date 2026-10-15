"""Customer notification behavior."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    """Content for one channel. Channels that have no title (SMS) ignore it."""

    body: str
    title: str = ""


class NotificationService:
    """Decides what to tell a customer and delivers it on their preferred channel.

    Public methods own the wording of each notification.
    ``_deliver`` owns the routing: which sender and which contact field
    each channel uses. Adding a message type touches only the first part;
    adding a channel touches only ``_deliver`` plus that channel's wording.
    """

    def __init__(self, email_sender, sms_sender, push_sender):
        self.email_sender = email_sender
        self.sms_sender = sms_sender
        self.push_sender = push_sender

    def send_order_confirmation(self, customer, order_id: str) -> None:
        self._deliver(
            customer,
            {
                "email": Message(
                    title=f"Order {order_id} confirmed",
                    body=f"Hello {customer.name}, your order {order_id} was confirmed.",
                ),
                "sms": Message(body=f"Order {order_id} confirmed for {customer.name}."),
                "push": Message(
                    title="Order confirmed",
                    body=f"Order {order_id} is confirmed.",
                ),
            },
        )

    def send_shipping_update(self, customer, order_id: str, tracking_code: str) -> None:
        self._deliver(
            customer,
            {
                "email": Message(
                    title=f"Order {order_id} shipped",
                    body=(
                        f"Hello {customer.name}, your order {order_id} shipped. "
                        f"Tracking: {tracking_code}."
                    ),
                ),
                "sms": Message(body=f"Order {order_id} shipped. Tracking: {tracking_code}."),
                "push": Message(
                    title="Order shipped",
                    body=f"Track order {order_id}: {tracking_code}.",
                ),
            },
        )

    def _deliver(self, customer, messages_by_channel: dict[str, Message]) -> None:
        channel = customer.preferred_channel
        message = messages_by_channel.get(channel)

        if channel == "email":
            self.email_sender.send(customer.email, message.title, message.body)
        elif channel == "sms":
            self.sms_sender.send(customer.phone, message.body)
        elif channel == "push":
            self.push_sender.send(customer.device_id, message.title, message.body)
        else:
            raise ValueError("Unsupported notification channel")
