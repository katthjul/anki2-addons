# anki2-addons
A collection of add-ons for [Anki 2](http://http://ankisrs.net/).

## Length filter in browser
Find sentences of a given exact/maximum/minimum length in the browser.

File(s): *length.py*

### Usage
The add-on extends the available search commands in the browser. By default, it only looks at the note type 'Japanese' and its field 'Expression'. Edit the source file to add other notes.

<dl>
<dt>len:6</dt>
<dd>find notes with Expression field having a length of exactly 6 characters, like "こんにちは。", "そうですか。", etc.</dd>
<dt>max:4</dt>
<dd>find notes with Expression field having a length of at most 4 characters, like "ええ。", "いええ。", etc.</dd>
<dt>min:5</dt>
<dd>find notes with Expression field having a length of at least 5 characters, like "キムです。", "はい、そうです。", etc.</dd>
</dl>

### Status
Experimental. Requires changes to Anki 2, see [Ticket 699](https://anki.lighthouseapp.com/projects/100923-ankidesktop/tickets/699-add-hook-for-search-command).
