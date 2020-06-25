import asyncio

from opsdroid.matchers import match_regex, match_event
from opsdroid.skill import Skill
from opsdroid.events import *


class DemoSkill(Skill):

    # Send events

    @match_regex(r'[hH]i')
    async def send_text(self, message):
        await message.respond("hey")

    @match_regex(r'[sS]end a file')
    async def send_file(self, message):
        with open("path/to/file", "rb") as send_file:
            send_file = send_file.read()
            send_event = File(name="file", file_bytes=send_file, mimetype="text/plain")
        #send_event = File(name="pic", url="https://docs.opsdroid.dev/en/stable/_static/logo.png", mimetype="image/png")
        await message.respond(send_event)

    @match_regex(r'[sS]end a pic')
    async def send_image(self, message):
        with open("path/to/pic", "rb") as pic:
            pic = pic.read()
            send_event = Image(name="pic", file_bytes=pic, mimetype="image/png")
        #send_event = Image(name="pic", url="https://docs.opsdroid.dev/en/stable/_static/logo.png", mimetype="image/png")
        await message.respond(send_event)

    @match_regex(r'[eE]dit')
    async def send_edit(self, message):
        old_event = await message.respond("unedited")
        await asyncio.sleep(2)
        send_event = EditedMessage(text="edited", linked_event=old_event)
        await message.respond(send_event)

    @match_regex(r'[rR]eact')
    async def send_reaction(self, message):
        send_event = Reaction(emoji="😃", linked_event=message)
        await message.respond(send_event)

    @match_regex(r'[rR]eply')
    async def send_reply(self, message):
        send_event = Reply(text="sup")
        await message.respond(send_event)

    @match_regex(r'[cC]hange( the)? room name')
    async def send_room_name(self, message):
        send_event = RoomName(name="Demo Room Encrypted")
        await message.respond(send_event)

    @match_regex(r'[cC]hange( the)? room desc(ription)?')
    async def send_room_description(self, message):
        send_event = RoomDescription(description="This room is encrypted")
        await message.respond(send_event)

    # Receive events

    @match_regex(r'^(?![hH]i$|[sS]end a (file|pic)$|[eE]dit$|[rR]e(act|ply)$|[cC]hange( the)? room (name|desc(ription)?)$).*')
    async def get_text(self, message):
        await message.respond("Received encrypted text")

    # Events that aren't Message type don't have a respond method that converts strings to Message events so we have to do it

    @match_event(File)
    @match_event(Image)
    @match_event(EditedMessage)
    @match_event(Reaction)
    @match_event(Reply)
    @match_event(RoomName)
    @match_event(RoomDescription)
    async def get_event(self, message):
        await message.respond(Message(f"Received encrypted {message.__class__.__name__} event"))

