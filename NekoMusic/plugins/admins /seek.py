# Description: Command to seek the currently playing song to a specified duration in a group chat.

# Dependencies:
# - Pyrogram
# - YouTube (Custom module)
# - Alexa (Custom module)

- from: pyrogram.filters
  import: filters
- from: pyrogram.types
  import: Message
- from: config
  import: BANNED_USERS
- from: strings
  import: get_command
- from: AlexaMusic
  import: YouTube, app
- from: AlexaMusic.core.call
  import: Alexa
- from: AlexaMusic.misc
  import: db
- from: AlexaMusic.utils
  import: AdminRightsCheck, seconds_to_min

commands:
  - SEEK_COMMAND

rules:
  - filters.command(SEEK_COMMAND) & filters.group & ~filters.edited & ~BANNED_USERS

actions:
  - command: seek_comm

functions:
  seek_comm:
    if:
      - condition: "len(message.command) == 1"
        do:
          - reply_text: _["admin_28"]
          - stop
    var:
      - query: "message.text.split(None, 1)[1].strip()"
    if:
      - condition: "not query.isnumeric()"
        do:
          - reply_text: _["admin_29"]
          - stop
    var:
      - playing: "db.get(chat_id)"
    if:
      - condition: "not playing"
        do:
          - reply_text: _["queue_2"]
          - stop
    var:
      - duration_seconds: "int(playing[0]['seconds'])"
    if:
      - condition: "duration_seconds == 0"
        do:
          - reply_text: _["admin_30"]
          - stop
    var:
      - file_path: "playing[0]['file']"
    if:
      - condition: "'index_' in file_path or 'live_' in file_path"
        do:
          - reply_text: _["admin_30"]
          - stop
    var:
      - duration_played: "int(playing[0]['played'])"
      - duration_to_skip: "int(query)"
      - duration: "playing[0]['dur']"
    if:
      - condition: "message.command[0][-2] == 'c'"
        do:
          - if:
              - condition: "(duration_played - duration_to_skip) <= 10"
                do:
                  - reply_text: _["admin_31"].format(seconds_to_min(duration_played), duration)
                  - stop
          - to_seek: "duration_played - duration_to_skip + 1"
      - else:
        do:
          - if:
              - condition: "(duration_seconds - (duration_played + duration_to_skip)) <= 10"
                do:
                  - reply_text: _["admin_31"].format(seconds_to_min(duration_played), duration)
                  - stop
          - to_seek: "duration_played + duration_to_skip + 1"
    var:
      - mystic: "await message.reply_text(_['admin_32'])"
    if:
      - condition: "'vid_' in file_path"
        do:
          - var:
              - n, file_path: "await YouTube.video(playing[0]['vidid'], True)"
          - if:
              - condition: "n == 0"
                do:
                  - reply_text: _["admin_30"]
                  - stop
    try:
      - Alexa.seek_stream(chat_id, file_path, seconds_to_min(to_seek), duration, playing[0]['streamtype'])
    catch:
      - reply_text: _["admin_34"]
      - stop
    if:
      - condition: "message.command[0][-2] == 'c'"
        do:
          - assign: db[chat_id][0]['played']
            value: "duration_played - duration_to_skip"
      - else:
        do:
          - assign: db[chat_id][0]['played']
            value: "duration_played + duration_to_skip"
    - reply_text: _["admin_33"].format(seconds_to_min(to_seek))
