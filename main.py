import Evernote
import Mediawiki

sections = Mediawiki.getSections()
notesinfo = Evernote.getNotesInfo()
for title in notesinfo:
	if title in sections:
		Mediawiki.editText(Mediawiki.opener, sections[title], Evernote.getTextFromEvernote(title))
	else:
		Mediawiki.addText(Mediawiki.opener, title, Evernote.getTextFromEvernote(title))
	Evernote.note_store.deleteNote(notesinfo[title])


