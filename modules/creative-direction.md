# Creative direction and storyboard module

## Purpose
Translate the script and brief into a shootable or generatable visual plan.

## Direction fields
For every scene specify:
- scene ID and time range;
- narration/dialogue or silent beat, exact text and spoken locale;
- subject, one primary action and emotional intention;
- shot size, angle, lens feel, focus and camera movement;
- composition, lighting, color, environment and props;
- sound design and transition;
- explicit opening state, action progression and closing continuity state.

## Continuity
Lock recurring character appearance, wardrobe, age presentation, location, prop positions, lighting, camera direction and visual style. Each following scene must begin from the actual state established by the previous scene. Record a continuity ledger: avatar identity, outfit, hands/pose, countertop, utensils, ingredient quantity/state, vessel location, food preparation stage, camera framing and light. Do not allow props, food, people, or products to teleport, duplicate, morph, or change shape between shots.

## Camera language
Choose camera moves intentionally: static for clarity, push-in for emphasis, tracking for movement, pan/tilt for reveals, orbit for spatial context, handheld for immediacy, and overhead for process demonstrations. Avoid movement that distracts or causes generation instability. In recipe/UGC demos keep food/product visually prominent and avoid presenter blocking the action.

## Prompt writing
Describe one coherent shot with explicit subject, action, environment, camera, lighting, style, duration and constraints. Spoken narration is assigned line-by-line and specified in the requested language/locale. Visuals must match what is actually said and physically shown at that moment. Do not rely on vague terms such as "cinematic" alone. For Google Flow, apply `modules/google-flow-prompting.md`: prompts in English with spoken narration explicitly in native pt-BR, clips no longer than 10 seconds, natural human performance, concise concrete negatives, and prompt-by-prompt state continuity.

For user recipe workflow, do not make or use food reference stills that show a future preparation state unless explicitly requested. If a finished-dish opening hook is requested, isolate it in a separate opener before preparation scenes. Avatar reference is the identity anchor only when the user supplies it and authorizes its use.

## Deliverables
Timed storyboard, shot list, continuity lock, generation prompts, and asset requirements.
