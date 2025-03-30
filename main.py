from telethon.sync import TelegramClient, events
import asyncio
from fuzzywuzzy import fuzz
import os
from telethon.errors import ChatWriteForbiddenError, ChatAdminRequiredError

# Configuration
API_ID = 23449732
API_HASH = '155f957734947d7d39c6300f9679d2c9'
PHONE_NUMBER = '+251918365217'  
HYMN_GROUP = 'Faaruu_Search'

# Initialize client as bot instead of user
client = TelegramClient('user_session', API_ID, API_HASH)
async def search_hymns(query):
    """Search MP3 files with fuzzy matching"""
    try:
        group = await client.get_entity(HYMN_GROUP)
        hymns = []
        
        async for msg in client.iter_messages(group, limit=200):
            if msg.document and msg.document.mime_type == 'audio/mpeg':
                filename = msg.file.name.lower() if msg.file.name else ""
                similarity = fuzz.partial_ratio(query.lower(), filename)
                
                if similarity > 50:
                    hymns.append(msg)
        
        return hymns
        
    except Exception as e:
        print(f"Search error: {str(e)}")
        return []

async def main():
    try:
        await client.start(phone=PHONE_NUMBER)
        print("Bot is running...")
        
        @client.on(events.NewMessage)
        async def handler(event):
            try:
                if event.is_private:  # Only respond in private chats
                    query = event.raw_text.strip()
                    if not query:
                        return
                        
                    reply = await event.reply("🔎 Searching...")
                    hymns = await search_hymns(query)
                    
                    if hymns:
                        await reply.edit(f"Found {len(hymns)} matches")
                        for hymn in hymns[:3]:
                            await event.reply(file=hymn)
                            await asyncio.sleep(0.2)
                        
                        invite_message = (
                            "🌟 Faaruu Haaraa Argachuu Barbaadduu? 🌟\n\n"
                            "📱 Grop keenya itt daabalamuu barbaadan:\n"
                            "➡️ t.me/kutaa_faaruu_jimma_jit\n\n"
                            "🎵 Faaruu Haaraa Argadhaa! 🎶"
                        )
                        await event.reply(invite_message)
                    else:
                        await reply.edit("❌ No matches found")
            
            except (ChatWriteForbiddenError, ChatAdminRequiredError):
                print("Bot doesn't have permission to write in this chat")
            except Exception as e:
                print(f"Handler error: {str(e)}")
        
        await client.run_until_disconnected()
        
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main())
