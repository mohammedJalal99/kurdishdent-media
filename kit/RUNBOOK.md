# KURDISH DENT — weekly batch runbook

Approved plan (Claude Docs doc `25112153-7e21-4686-95a6-adb27d2545cb`, approved by the owner on 2026-11-27): 1 image (13:30 Erbil) + 1 Reel (20:30 Erbil) per day, 2026-11-28 → 2026-12-27. Each batch covers the days given in the trigger message.

Per day in the batch:
1. Read that day's two plan rows (headline + key points). Write only what the plan says; no clinic names, prices, invented statistics or treatment promises. Natural, catchy Sorani.
2. Image: `kit/render_post.py` spec. Rotate styles poster → cards → bignum → poster…; use `myth` for myth/“true or false” topics.
3. Reel: voice script ≤ 230 characters (Sorani, eleven_v4 tags like [warmly] [excited]), ElevenLabs `creative_generate_speech`, voice `gMB389pj77Qe5nErWNjd`, model `eleven_v4`, generations_count 1 (check `account_get_usage` first; skip voice if credits are short). Get the mp3 with `creative_get_generations` → `full_res_url` → curl. Then `kit/render_reel.py` spec with `"voice"`, 5 scenes (hook, key fact, detail, takeaway, end card), gradient backgrounds, different `seed` each day.
4. Decrypt font: `openssl enc -d -aes-256-cbc -pbkdf2 -in kit/Rabar_021.ttf.enc -out kit/Rabar_021.ttf -pass pass:<key from the session>` (never commit the decrypted font).
5. Commit media to `media/<date>/post.jpg` and `media/<date>/reel.mp4`, push, then vidIQ: `vidiq_upload_image` / `vidiq_video_upload` with the raw.githubusercontent.com URL; `vidiq_social_post_draft_create` for Instagram account `40388390387443020` with `publishAt` `<date>T13:30:00+03:00` (image) and `<date>T20:30:00+03:00` (Reel). Caption: hook line, 1–2 lines, CTA, hashtags `#ددان #تەندروستی_ددان #kurdishdent #کوردستان`.
6. Review: send all images and Reels with SendUserFile, list each post (date, time, headline, caption), and ask once with AskUserQuestion for approval of the whole batch. Publish every draft (`vidiq_social_post_publish`) only after the owner says yes.
7. Schedule the next batch with `send_later` (Thursday ~18:00 Erbil, covering Saturday → Friday). After 2026-12-27 stop and ask for next month's plan.
