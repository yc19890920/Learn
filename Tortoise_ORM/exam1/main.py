import asyncio
import uvloop
from tortoise import Tortoise, run_async
from app.models import Tournament, Team, Event

import settings


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(config=settings.TORTOISE_ORM)
    # Generate the schema
    await Tortoise.generate_schemas()


async def main1():
    # run_async is a helper function to run simple async Tortoise scripts.
    # run_async(init())
    await init()
    # await Tortoise.generate_schemas()
    await Tortoise.close_connections()
    print("===============")
    await init()

    tournament = Tournament(name='New Tournament 1')
    await tournament.save()

    # Or by .create()
    await Tournament.create(name='Another Tournament 1')

    # Now search for a record
    tour = await Tournament.filter(name__contains='Another').first()
    print(tour.name)

    # Or by .create()
    await Event.create(name='Without participants', tournament=tournament)
    event = await Event.create(name='Test', tournament=tournament)
    participants = []
    for i in range(2):
        team = await Team.create(name='Team {}'.format(i + 1))
        participants.append(team)

    # M2M Relationship management is quite straightforward
    # (look for methods .remove(...) and .clear())
    await event.participants.add(*participants)

    # You can query related entity just with async for
    async for team in event.participants:
        print(team)

    # After making related query you can iterate with regular for,
    # which can be extremely convenient for using with other packages,
    # for example some kind of serializers with nested support
    for team in event.participants:
        pass

    # Or you can make preemptive call to fetch related objects,
    # so you can work with related objects immediately
    selected_events = await Event.filter(
        participants=participants[0].id
    ).prefetch_related('participants', 'tournament')
    for event in selected_events:
        print(event.tournament.name)
        print([t.name for t in event.participants])

    # Tortoise ORM supports variable depth of prefetching related entities
    # This will fetch all events for team and in those team tournament will be prefetched
    await Team.all().prefetch_related('events__tournament')

    # You can filter and order by related models too
    await Tournament.filter(
        events__name__in=['Test', 'Prod']
    ).order_by('-events__participants__name').distinct()

    events = await tournament.events.all()
    print(events)


async def main():
    await init()
    tournament = await Tournament.get(id=1)
    print("tournament:", tournament.name)

    for event in await tournament.events.all():
        print("event:", event.name)
        for team in await event.participants.all():
            print("team:", team.name)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(main())]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
