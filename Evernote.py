import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.edam.notestore.ttypes import NoteFilter

from bs4 import BeautifulSoup
from functools import reduce

from evernote.api.client import EvernoteClient

auth_token = "TOKEN"
updatorGUID = "GET YOUR GUID"

if auth_token == "your developer token":
    print("Please fill in your developer token")
    print("To get a developer token, visit " \
          "https://sandbox.evernote.com/api/DeveloperToken.action")
    exit(1)

client = EvernoteClient(token=auth_token, sandbox=True)

user_store = client.get_user_store()

version_ok = user_store.checkVersion(
    UserStoreConstants.EDAM_VERSION_MAJOR,
    UserStoreConstants.EDAM_VERSION_MINOR
)
print("Is my Evernote API version up to date? ", str(version_ok))
print("")
if not version_ok:
    exit(1)

note_store = client.get_note_store()

def getNotesInfo():
    updatorNotes = note_store.findNotes(NoteFilter(notebookGuid = updatorGUID), 0, 10).notes
    updatorNotesInfo = {note.title:note.guid for note in updatorNotes}
    return updatorNotesInfo


def getTextFromEvernote(title):
    rawtext = BeautifulSoup(note_store.getNoteContent(getNotesInfo()[title]))
    return reduce(lambda acc, s : acc + s.string + '\n', rawtext.find_all('div'),'')

