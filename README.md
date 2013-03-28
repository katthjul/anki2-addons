# anki2-addons
A collection of add-ons for [Anki 2](http://http://ankisrs.net/).

## Generate clozes from frame numbers
Generate clozes from frame numbers listed in field Extras.

Status: **Alpha**

File(s): *cloze_creator.py*, *clozecreator/frame-list.txt*, *clozecreator/gui.py*, *closecreator/utils.py*

### Usage
The add-on creates a new menu Cloze in the browser. The menu contains several operations that can be done to cards with the note type Cloze.

<dl>
<dt>Bulk-add clozes</dt>
<dd>The action executes the following in order: *Format frame number*, *Create clozes*, and *Reposition cards*.</dd>
<dt>Format frame numbers</dt>
<dd>If the field Extra contains a list of numbers or kanji, each number or kanji will be used to look up the corresponding frame from the <a href="http://www.coscom.co.jp/ebook/item_2001kanji.html">2001.Kanji.Odyssey series</a>, like "32 二 19" will be formatted as "今32 二2 日19".</dd>
<dt>Create clozes</dt>
<dd>Will create a cloze for every kanji that is listed in the field Extra. Notes that already has at least one cloze will be ignored.</dd>
<dt>Reposition cards</dt>
<dd>Every card of a note will be repositioned based on the frame number of the kanji. If a cloze is not a kanji or a kanji without a frame number, its position will not change. A note with field Text like "{{c1::今}}日は{{c2::水::すい}}{{c3::曜}}日です。" and field Extra "今32 水22" will have its first and second card repositioned to 32 respective 22 (the third is unchanged).</dd>
<dt>Regenerate frame numbers</dt>
<dd>Fill in frame numbers in the field Extra based on the kanji present in the field Cloze. Overwrites any content in the field Extra.</dd>
</dl>

## Search by length in browser
Find sentences of a given exact/maximum/minimum length in the browser.

Status: **Experimental**. Requires changes to Anki 2, see [Ticket 699](https://anki.lighthouseapp.com/projects/100923-ankidesktop/tickets/699-add-hook-for-search-command).

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
