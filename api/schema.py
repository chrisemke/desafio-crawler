
"""Web scraping code challenge
Copyright (C) 2023 Christian G. Semke.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from fastapi import BackgroundTasks
from strawberry import Schema, field, mutation, type
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info


@type
class Quotes:
    """Dataclass for a quote."""

    quote: str | None
    author: str | None
    limit: int | None = 10


@type
class Query:
    """Here, all GraphQL queries to get information dynamically
    like http GET on REST.
    """

    all_quotes: list[Quotes] = field()


@type
class Mutation:
    """GraphQL mutations to add/change information dynamically
    like http POST/PUT/DELETE on REST.
    """

    @mutation
    async def schedule_tasks(self, name: str, info: Info) -> bool:
        """Mutation to schedule tasks that will run every hour."""
        info.context["background_tasks"].add_task(notify_new_flavour, name)
        return True


schema = Schema(Query, Mutation)

graphql_app = GraphQLRouter(schema)
