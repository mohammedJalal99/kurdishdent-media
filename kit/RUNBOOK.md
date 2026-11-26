# KURDISH DENT — daily runbook

Approved plan (Claude Docs doc `25112153-7e21-4686-95a6-adb27d2545cb`, approved by the owner on 2026-11-27): 1 image (13:30 Erbil) + 1 Reel (20:30 Erbil) per day, 2026-11-28 → 2026-12-27. Mode (owner's instruction, 2026-11-27): the owner approves the MONTHLY PLAN once; that approval covers every post in it. Produce posts DAILY (one day at a time, the next day's two posts), and schedule them without asking again. Never post anything that is not in the approved plan.

Per day in the batch:
1. Read that day's two plan rows (headline + key points). Write only what the plan says; no clinic names, prices, invented statistics or treatment promises. Natural, catchy Sorani.
2. Image: `kit/render_post.py` spec. Rotate styles poster → cards → bignum → poster…; use `myth` for myth/“true or false” topics.
3. Reel: voice script ≤ 230 characters (Sorani, eleven_v4 tags like [warmly] [excited]), ElevenLabs `creative_generate_speech`, voice `gMB389pj77Qe5nErWNjd`, model `eleven_v4`, generations_count 1 (check `account_get_usage` first; skip voice if credits are short). Get the mp3 with `creative_get_generations` → `full_res_url` → curl. Then `kit/render_reel.py` spec with `"voice"`, 5 scenes (hook, key fact, detail, takeaway, end card), gradient backgrounds, different `seed` each day.
4. Decrypt font: `openssl enc -d -aes-256-cbc -pbkdf2 -in kit/Rabar_021.ttf.enc -out kit/Rabar_021.ttf -pass pass:<key from the session>` (never commit the decrypted font).
5. Commit media to `media/<date>/post.jpg` and `media/<date>/reel.mp4`, push, then vidIQ: `vidiq_upload_image` / `vidiq_video_upload` with the raw.githubusercontent.com URL; `vidiq_social_post_draft_create` for Instagram account `40388390387443020` with `publishAt` `<date>T13:30:00+03:00` (image) and `<date>T20:30:00+03:00` (Reel). Caption: hook line, 1–2 lines, CTA, hashtags `#ددان #تەندروستی_ددان #kurdishdent #کوردستان`.
6. Schedule both drafts right away with `vidiq_social_post_publish` (covered by the approved monthly plan). Post a one-line note in the chat with what was scheduled.
7. Chain: `send_later` for the next day ~10:43 Erbil to prepare the following day. Near the end of the month (~12-25), write next month's plan doc and ask the owner once to approve it.

TikTok (connected 2026-11-27, account "KURDISH DENT", platformAccountId `_000qRAJIHTKORRwTrskpi9PHs2hyfxBh7bc`; never post to "پەیامی تەندروستی"): post BOTH the image (photo post, `title` ≤ 90 chars = headline, `autoAddMusic` true) and the Reel (`isAiGenerated` true, AI voice) at the same times as Instagram. Owner's fixed choices: `privacyLevel` PUBLIC_TO_EVERYONE, `allowComment` true, `musicUsageConfirmed` true. Use a separate draft per platform post.
