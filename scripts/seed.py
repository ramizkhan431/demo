import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal
from app.models.user import User
from app.models.author import Author
from app.models.location import Location
from app.models.content import Content, ContentType
from app.models.story import TravelStory
from app.models.associations import StoryAuthor, StoryLocation, StoryContent
from app.services.auth import get_password_hash

async def seed_data():
    async with SessionLocal() as db:
        # Create user
        user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_superuser=True
        )
        db.add(user)

        # Create author
        author = Author(
            name="John Doe",
            description="A traveler who loves mountains."
        )
        db.add(author)
        await db.flush()

        # Create hierarchical locations
        country = Location(
            name="Switzerland",
            description="Famous for its mountains and watches.",
            metadata_json={"currency": "CHF"}
        )
        db.add(country)
        await db.flush()

        city = Location(
            name="Zermatt",
            description="A mountain resort town at the foot of Matterhorn.",
            parent_id=country.id,
            metadata_json={"elevation": "1608m"}
        )
        db.add(city)
        await db.flush()

        # Create content
        content1 = Content(
            name="Matterhorn View",
            description="A beautiful morning view of Matterhorn peak.",
            content_type=ContentType.IMAGE,
            image_path="uploads/matterhorn.jpg"
        )
        content2 = Content(
            name="Hiking Vlog",
            description="Short vlog of hiking path near the village.",
            content_type=ContentType.VIDEO,
            video_url="https://youtube.com/example-vlog"
        )
        db.add_all([content1, content2])
        await db.flush()

        # Create Travel Story
        story = TravelStory(
            name="Mountains of Switzerland",
            description="Exploring the peak of Matterhorn and the beautiful village of Zermatt."
        )
        db.add(story)
        await db.flush()

        # Link story components
        author_link = StoryAuthor(story_id=story.id, author_id=author.id)
        location_link = StoryLocation(story_id=story.id, location_id=city.id)
        content1_link = StoryContent(story_id=story.id, content_id=content1.id, ordering_index=0)
        content2_link = StoryContent(story_id=story.id, content_id=content2.id, ordering_index=1)
        
        db.add_all([author_link, location_link, content1_link, content2_link])

        await db.commit()
        print("Initial data seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
