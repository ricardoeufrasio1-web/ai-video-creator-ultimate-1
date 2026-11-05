# Google Flow prompt direction and natural-performance standard

This module captures the user's accumulated production constraints for Flow-style short clips. Apply it whenever the brief mentions Google Flow, AI UGC, recipe videos, product demos, avatar-led social video, or asks for copy/paste video prompts. These are production defaults, not restrictions on unrelated formats; follow explicit current user instructions when they differ.

## 1. Output format and segmentation
- Deliver prompts ready to copy/paste. Visual/video prompt language: English. Spoken narration: explicitly Brazilian Portuguese (pt-BR), never European Portuguese. Keep any user-supplied narration verbatim when they say not to modify it.
- Flow clip ceiling: 10 seconds. Segment into distinct clips of at most 10 seconds; for rapid recipe action, use 4–6 second scene beats if requested or if the action needs finer sync. Do not pack a 30–40 second script into one clip.
- Use vertical 9:16 for Reels, Shorts, TikTok unless another format is specified. Use the exact duration requested, not a vague “short clip.”
- Each prompt must be self-contained enough to paste individually and should state clip duration, framing, visual action, camera, lighting, sound/narration, exclusions and continuity state.
- Include a clip-by-clip narration ledger with the exact words assigned to each clip and realistic duration. Do not accelerate speech to squeeze in extra words. If it does not fit, revise the storyboard/script before generation (unless the user explicitly requires verbatim copy, then flag the timing conflict).
- Prompts for successive clips must describe the precise visual state where the preceding clip ended and start from that state. Preserve scene geography and object positions.

## 2. Natural narration — quality gate
Preferred narration for avatar/UGC/recipe content: natural, conversational Brazilian Portuguese, human cadence, warm but not overacted, clear articulation, moderate energetic delivery, organic pauses and breaths. Match speaker gender/style as brief specifies; do not assume male voice when a female avatar is shown.
- Avoid robotic TTS cadence, monotone, over-enunciation, unnatural pauses, excessively fast speech, synthetic-sounding vowels, theatrical/advertisement shouting, or voice that sounds dubbed from Portugal.
- Require exact locale: “Brazilian Portuguese (pt-BR), native Brazilian accent; not European Portuguese.”
- Voice is foreground and intelligible. Keep music/effects subtle and below speech. Do not create additional speakers or improvise lines.
- Give voice generation a performance direction (meaning and emotion of the sentence) instead of piling up contradictory adjectives. Preserve script exactness; no filler words unless present.
- For best results, use a human-recorded voice or a connected, authorized high-quality natural voice provider. Listen to the full final encoded audio and reject a robotic/incorrect accent take.
- Offline eSpeak NG is a development fallback only. Its synthetic/robotic sound is known and must not be labeled “natural,” “humanized,” or final-quality. Never use it by default for social-ready delivery. If selected, explicitly warn before generation and require the user/agent to set the allow flag.

## 3. Avatar / UGC realism
- Use the user's avatar reference as the identity anchor only when supplied and authorized. Lock face shape, age presentation, skin texture, hair, wardrobe, body proportions and voice across all clips. Avoid changing identity, beautifying into plastic skin, or switching avatar.
- Human behavior: subtle blinking, breathing, eye contact, small natural hand gestures, believable weight and object handling. Keep expression restrained and appropriate; no forced smile or exaggerated influencer acting.
- Smartphone UGC look when requested: believable domestic space, natural available light, authentic camera distance, minor natural skin texture, stable exposure. Do not show a phone in-frame unless requested.
- Keep food/product prominent when it's the subject; presenter should not block the demo.

## 4. Reference-image discipline (especially recipes)
- Do not invent food-reference stills or use them as action references unless the user explicitly requests image-first workflow. In latest recipe workflow, the avatar reference is the only image reference; describe food/ingredients directly in the video prompt.
- Never use a finished dish still to anchor a scene whose narration/action is still preparing ingredients. This causes temporal mismatch. If a finished-dish hook is explicitly requested, put it in its own opening clip and then cut to the preparation state in the next clip.
- Never let ingredients, bowls, tools, quantities, preparation stages or finished plate teleport, duplicate, morph, or change between clips. Keep a continuity ledger and state transitions.
- For final recipe payoff, show the actually completed dish, then the avatar tasting a piece only if requested and physically plausible. Do not show tasting before dish is ready.
- Prompts must reflect what is spoken and physically visible at that exact moment. No action in narration without corresponding visual when feasible; do not depict an ingredient/action not in the recipe.

## 5. On-screen exclusions and failure prevention
Default for user's social recipe/UGC workflow: no captions, subtitles, text overlays, titles, logos, watermarks, UI, or graphics unless explicitly requested. No extra voice, no off-script dialogue, no random music lyrics.
Negative constraints should be concise and concrete: no extra fingers/limbs, malformed hands, face morphing, duplicate objects, flicker, unstable geometry, product/food deformation, sudden prop changes, jumpy continuity, unnatural motion, overexposed skin, waxy skin.
Do not use blanket “cinematic” as a substitute for actual shot direction. Specify close-up/medium/overhead, camera movement, focal emphasis, light source, action, and composition. One coherent primary action per clip.

## 6. Build prompt in a fixed order
Use this template, filling details instead of leaving placeholders when known:

```
Google Flow video prompt — [CLIP ID], [exact duration], vertical 9:16.
Visual: [one coherent shot, subject, exact physical action and state].
Camera: [shot size/angle, movement and focus; avoid unnecessary movement].
Environment and light: [locked location, props, natural/soft lighting and continuity].
Character/product continuity: [fixed identity/wardrobe/product details; exact start state from prior clip and end state for next clip].
Narration: exact spoken line “[VERBATIM SCRIPT]”, spoken in native Brazilian Portuguese (pt-BR), [speaker description], natural conversational human cadence, clear and intelligible, moderate pace, subtle breathing and meaningful pauses, emotionally appropriate but not exaggerated. No paraphrase, no extra words, no European Portuguese.
Audio: narration clearly foreground; ambience/SFX only when they match visible action and remain subtle; music low or absent.
Constraints: no subtitles/captions/on-screen text/logos/watermarks; no additional speakers; no identity/prop/ingredient changes; no morphing, flicker, malformed hands or artificial acting.
```

## 7. Required handoff checks
Before returning prompts:
1. Verify scene duration sum against requested runtime.
2. Read narration aloud mentally at natural pt-BR speed; distribute speech by sentence/action, leaving breathing room.
3. Check visual/narration synchronization line by line.
4. Check start/end continuity of avatar, wardrobe, props, ingredients, food state, camera and lighting.
5. Verify reference-image plan follows the user's preference; recipe images must not pre-spoil prep state.
6. Confirm every prompt contains pt-BR locale and the natural voice direction, plus explicit no-text constraints when applicable.
7. Mark any capability gap honestly. Prompts cannot guarantee Flow will obey voice/continuity; final clips must be auditioned and visually reviewed. Regenerate or revise defective scenes rather than calling them complete.

## 8. User-established recipe preset — Leve e Saboroso
Use this preset when the user asks for a Leve e Saboroso recipe video; do not force it onto other projects.
- Typical runtime is 30–40 seconds, sometimes a 25–30 second test. Split into Flow clips of at most 10 seconds; use 4–6 second shots for detailed cooking steps when pacing and sync require them.
- Portuguese narration should start with an immediate hook/action, not a long greeting or slow introduction. The finished dish may be the opening visual hook for roughly 4–5 seconds only when the current script/storyboard asks for it; then transition to preparation, with the next clip explicitly continuing from that state.
- The newest recipe reference rule is avatar image only as identity reference. Do not attach food/ingredient reference images unless the user explicitly changes this preference. Describe recipe objects and stages in prompt text.
- Keep recipe and food as the visual priority; avatar may appear naturally in a home kitchen, in ordinary kitchen clothing. Avoid showing a phone in UGC footage unless requested. Keep face consistent and avoid plastic/airbrushed skin.
- At the end, when the offer is this recipe collection, use the user-approved CTA concept: “Quer mais receitas assim? 200 receitas leves e saborosas. Link na bio.” Preserve the exact CTA supplied for a specific video. Do not reintroduce a price comparison/price line when the user has excluded it. Avoid absolute claims such as “não engorda” or “pode comer à vontade”; use grounded “leve”, “saboroso”, “mais equilibrado” or “sem exagero” positioning.
- Final payoff: show the completed dish appetizingly; show the avatar tasting a piece only when the shot is requested and timing is physically plausible. Narration and action must align exactly (e.g., do not show a baked, plated food while the voice describes mixing ingredients).
- For each 10-second prompt (or shorter clip), repeat continuity lock: same avatar face/hair/skin/wardrobe, kitchen/counter, lighting, utensils and ingredient progression. State what hands are doing during each narration phrase. Scene B begins from scene A's final arrangement; do not reset bowls or props.

## 9. Voice and clip rejection examples
Reject these outputs and revise prompt or regenerate:
- Narration sounds like eSpeak or a monotone synthesized read; the voice uses PT-PT rather than PT-BR; the line is rushed or extra words were added.
- Avatar's face, hairstyle, outfit or apparent age changes across scenes; face is waxy, hands malformed, or smile is exaggerated.
- Food appears cooked before preparation, ingredient amounts/containers change, the camera reveals a different kitchen, or objects teleport between clips.
- Scene narration describes a step not shown, the visual action starts late/ends early, the cut changes the physical state without transition, or the last scene does not resolve/pay off the opening.
- Captions/text/logos appear when excluded.
