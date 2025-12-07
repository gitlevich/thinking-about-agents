# Frames

Earlier I talked about observer and agent modes, capture, goals, sigils. I kept using the word “frame” without unpacking
it. This is the piece that does that.

```text
Disclaimer: I don’t build agent architectures. This is phenomenological description and architectural sketching, aimed at people who
do.
```

In Agent Language, a contrast is an axis in the agent’s space along which things can differ: light/dark, near/far,
safe/dangerous, “this design” vs “that one.” What matters is that the agent can distinguish positions along it at its
current resolution.

An observation is the current value of a contrast for the agent. “This much light, this much distance, this much safety,
this specific design choice.” Observations are always relative to contrasts; without a possible difference there’s
nothing to observe.

A frame is the configuration of active contrasts and their current observations, held together long enough to feel like
“this moment.” It’s not just a bitmap. It’s which contrasts are even live, where they currently sit, and how finely each
is being sliced.

Resolution in AL is how finely I can distinguish along a contrast in this frame. Along “light,” I might only tell
“bright vs dark,” or I might tell “direct sun / open shade / bounced fill,” or in a lab I might track tiny changes in
lux. Same contrast, different granularity of distinction. Finer resolution means more, smaller distinguishable steps
along that axis, and it uses more attention.

Frame rate is how often I allow the frame to update. At high frame rate, I keep re-evaluating contrasts: micro-shifts in
posture, flicker in a face, tiny changes in sound. At low frame rate, I hold a frame for longer; the world can move a
bit and I’ll treat it as “still the same moment.” That’s cheaper in attention, but it means I miss some changes.

Attention is bounded. There is no “infinite attention” regime. For a given agent at a given time, the product of “how
many contrasts are live,” “how fine their resolution is,” and “how fast I’m updating them” has to fit under the
attention the agent actually has. If it doesn’t, something gives: I drop contrasts, I blur them, or I let the frame
update more slowly. That trade-off is not a choice the agent can avoid. It’s built in.

There are limits on both sides. There’s a minimum dwell time per frame: if I flip frames too fast, nothing has time to
register, and it all blurs. There’s also a maximum sustainable frame rate for a given bundle of contrasts and
resolutions: beyond it, I’m just jittering between partial frames and not integrating anything. In AL terms, the
attention limit is the boundary of the feasible region where number of contrasts, their resolution, and the frame rate
all fit under the attention the agent actually has. Outside that region, degradation starts: missed signals, tunnel
vision, or collapse into a much simpler frame.

This is where I want to line up AL with the way people talk about “dimensions.” When someone says “a 1,024-dimensional
embedding,” it doesn’t land for me. Dimension at that level is just a number. You can’t feel 1,024. In AL I treat a
dimension as a contrast. Each contrast is one axis along which things can differ for an agent: light/dark, near/far,
safe/dangerous, “this API shape / that API shape.” If you tell me “this frame is tracking 20 contrasts,” in principle I
can list them and explain why they matter.

Mathematically this is the same thing. A 1,024-dimensional vector is just a point in the space of 1,024 contrasts, most
of which we don’t have names for. AL doesn’t try to name all the hidden axes in a model’s embedding. It just insists
that when we talk about “dimension” in a lived frame, we talk in terms of contrasts: how many meaningful differences are
live for the agent right now, and at what resolution. Saying “this frame carries a dozen contrasts at high resolution”
tells you more than “it’s 12-dimensional,” because I could, if pressed, walk you through each contrast and show how
changing it would change the frame.

Observer mode is dominated by frames. In observer mode I’m not making choices. I’m just letting frames update as
attention moves across contrasts. Plenty of attention is available for sensing; narrative cost is low. The sensorium
flows through, but I’m not yet turning it into story. It’s “what’s here,” not “what I’m doing.”

Agent mode sits on top of frames. The agent uses frames as substrate for choice. Under a goal, each new frame is
evaluated: keep going, pivot, stop. A long narrative is just a sequence of frames that have been collapsed into choices
under a goal. If I’m “describing the room,” each frame is one update of what’s salient; the narrative is the word stream
that falls out of those frames being collapsed into “next token, next token.”

This brings in word paintings. A word painting is just a frame rendered in tokens. The frame itself is high-dimensional:
many contrasts, each with its own resolution and update rhythm. When I describe it in language, I project that frame
down into a one-dimensional sequence. The tokenizer walks the frame and leaves a trace. The result is linear, lossy, and
narratable, but still carries enough of the original structure that another agent can reconstruct a compatible frame on
their side. Because I’m a late bilingual, I often see this projection happen in my head: the frame is there first, then
the words arrive as a painting laid over it.

Capture can be seen as a frame problem. In capture, the agent keeps generating inside a frame that has stopped updating
in useful ways. The set of contrasts shrinks. Resolution narrows around whatever the narrative is about. Frame rate for
everything else drops. The “room” frame disappears, the “bookcase” frame disappears; only the gravity well remains. From
inside, it doesn’t feel like the frame has frozen. It feels like the world truly is only that sigil and its interior.

Sigils and frames meet at the resolution limit. Earlier I suggested something like a Planck length for cognition: not a
smallest concept, but a resolution limit for this frame. Below that grain, the tokenizer has nothing to emit. A sigil
marks that boundary. “My father’s death” is as far as this frame can express without a scale jump. To go further, I
would need to open a new frame at a different scale, with different contrasts and resolutions.

Scale, in this view, is about what gets packed into one frame. At a coarse scale, “describe the room” is one frame I can
hold for a while, with low resolution on many contrasts. At a finer scale, the same time interval contains many frames:
changes in light on the bookshelf, micro-movements in my chest, individual tokens as I speak. When I say “jump scale
into a sigil,” I mean: close the current frame and open another whose contrasts and resolutions are tuned for that
interior world.

There is also a hierarchy of frames that isn’t purely temporal. While I’m writing this, there is a tight frame around
the words on the screen, a looser frame around the room, and a very slow frame around my current life situation. They
update at different effective frame rates. The writing frame changes with every sentence. The room frame changes when
something salient moves or a sound intrudes. The life frame changes when something big happens: a move, an illness, a
new job. When I get captured by a thought, the writing frame can expand to fill attention, and the others go dim.

Some contrasts underlie all of this. In these pieces I’ve mostly used sensory or local contrasts — light/dark,
near/far — because they’re easy to point at. There are deeper contrasts too: “good / bad” under a goal, “I / not-I” as the
background split that makes any of this feel like “mine.” They show up implicitly whenever I talk about goals and
agents, but they need their own treatment. I’m just flagging them here.

From an architecture point of view, frames suggest a different way of thinking about context. Context windows in current
systems are mostly flat: a long list of tokens. Attention weights give that list some structure, but the system doesn’t
explicitly represent “these are the contrasts that are live in this frame, this is their resolution, this is how quickly
I’m willing to update them given my attention and goal.”

An AL-flavored agent would make that explicit. At any moment it would internally track which contrasts it is currently
following at all, for each contrast what resolution is in play, and how fast it plans to update them, given attention
and goals. Observer mode would be the regime where the agent mostly adjusts contrasts, resolution, and frame rate,
without committing to choices. Agent mode would be where it lets frames collapse into choices, and those choices form
narratives.

Capture detection could then be framed as a frame anomaly: frames that stop updating along important contrasts while
narrative continues; frames where resolution is extremely high on one contrast and collapsed on the rest; frames whose
update pattern no longer matches the nominal goal.

Goal precipitation fits here too. Preferences carve patterns not just in topology but in which frames keep reappearing.
Attention keeps opening similar frames — same bundle of contrasts, similar resolutions, similar update rhythm. Over time
that repeated framing stabilizes into a goal that can be named. “Apparently I keep opening frames where light and
geometry have high resolution. Maybe I’m a photographer.”

Entanglement, which I’ll come back to, can also be read in frame terms: two agents repeatedly opening overlapping
frames, with partially synchronized resolutions and frame rates, under a joint goal. But that’s another step.

I don’t know how much of this maps cleanly onto any existing architecture. For me, though, without frames — contrasts,
resolutions, and update rhythms held together as “this moment” — talk of agents, goals, sigils, and capture floats. Frames
are where the world actually shows up for an agent. Everything else in AL is layered on top of that.

If you’re building systems that have to manage attention, context, and narrative over time, and thinking in frames
sharpens where you place limits or detectors, use it. If it doesn’t line up with anything you see when you instrument
your systems, then at least you know that my frames and yours are drawn differently.
