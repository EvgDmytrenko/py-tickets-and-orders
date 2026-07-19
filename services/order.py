from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import Ticket, User, Order


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None) -> Order:

    user = User.objects.get_or_create(username=username)
    if date is not None:
        order = Order(user=user)
        order.created_at = parse_datetime(date)
        order.save()
    else:
        order = Order.objects.create(user=user)

    tickets_to_base = [
        Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )
        for ticket in tickets
    ]
    Ticket.objects.bulk_create(tickets_to_base)

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
