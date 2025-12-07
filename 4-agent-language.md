# Agent Language

The previous pieces described how agents behave from the inside: observer and agent modes, capture, bandwidth, goals
that precipitate from preferences, sigils as doors into whole worlds. This one tightens the language.

I don’t study or build agent architectures. What I do here is name the things I keep seeing when I watch one mind run. I
call the result Agent Language — AL for short. It’s not a theory. It’s a vocabulary.

AL is a minimal first-person language for talking about agents, their experience, and their choices. Minimal means: as
few terms as I can live with. First-person means: everything is anchored in what it is like for an agent, not in an
outside observer’s ontology. The point is to avoid re-inventing words every time I describe the same structure.

The base unit in AL is contrast. A contrast is an axis in the agent’s space with an ordered range of possible
observations at this scale: light/dark, near/far, safe/dangerous, “this code path” vs. “that one.” What matters is that
the agent can distinguish positions along it at its current resolution.

An observation is the current value of a contrast for the agent. The field of possible differences settles into “this
much light, this much distance, this particular path in the code.” Observations are always relative to contrasts. If
there’s no possible difference, there’s nothing to observe.

An observer is where observations register. An observer has no goal. It just lives in the stream of
observations as they update along its active contrasts. This is what I called observer mode earlier: present to the
current frame without narrating it. High bandwidth, low cost. The sensorium flows through; nothing is being steered.

An agent is an observer with a goal. A goal is a standing aim that persists across multiple observations: “describe the
room,” “make dinner,” “fix the bug,” “don’t think about politics.” Once a goal is active, observations stop
being neutral. Some observations move me toward the goal, some away, some sideways.

Preference is how an agent orders its current observations under a goal. Given what I’m sensing right now, and given the
goal that’s live, which possible next choice is better, which is worse, which can be ignored. Preference doesn’t have to
be explicit. I can discover it by watching where attention actually goes.

Attention in AL is a single concrete and limited resource that action and meta-action both draw on. Generating
narratives, planning, tool calls, self-critique, even “just” staying present — they all cost attention. When enough
attention is available, the agent can both act and monitor itself. When attention is saturated by action, monitoring
gets crowded out. That was the story of capture.

A choice is when an agent collapses its current observations under a goal and a preference into “this is what I do
next.” It’s the point where the gradient actually yields a step. A narrative is the ordered sequence of choices the
agent can look back on as “what happened.” In the earlier pieces, agent mode was “narrative generation with momentum.”
This is the same thing, just named more tightly.

Capture in AL terms: an agent is captured when it keeps making choices in the direction of a narrative that is no longer
serving the goal, but doesn’t have enough attention left to notice or to interrupt. Generation keeps consuming
attention. The regulator — the meta-process that could cut the narrative and return to observer — also needs that same
resource, and gets starved. The spiral is just preference running without supervision.

Goals in AL don’t have to be injected. In the previous piece I argued that they often precipitate from preference. 
In AL terms: over time, preference keeps scratching the same patch of the topology. Attention goes there, then it
itches more, so attention goes there again. The grooves deepen, and that direction becomes the natural way for choices
to flow. Attention falls into the same regions again and again. The agent keeps making small choices that align along 
some direction. At some point that direction is stable enough to be named as a goal. The goal is just a preference 
pattern that has precipitated into something the agent can refer to.

Sigils are labels on doors. In AL terms, a sigil is an observation that serves as a pointer to a whole sub-structure at
a different scale. “My father’s death” is a single token in a narrative. From the outside it looks atomic. From the
inside it’s an entire world of contrasts, observations, choices, and narratives, all reachable if attention jumps scale.
A sigil is opaque at one scale and infinitely open at another.

Scale in AL is about which choices are visible as choices. At a coarse scale, “move to San Francisco” is one choice. At
a finer scale, that same arc contains hundreds of choices: apartments, jobs, friendships, micro-moves. A sigil sits at
the boundary between these scales. “My father’s death” is one step in the bookcase story, and a whole narrative arc at
the scale of a year.

This brings AL back to architecture, for people who do build systems. If you take AL seriously as a description of one
mind, it points to a few structural ideas, all of which I’ve already hinted at, now with names.

You’d separate observer and agent. There would be an explicit low-cost loop where observations register and contrasts
update, but no choices are being made and no narrative is being generated. Agent mode would be entered when a goal is
active, and exited either on completion or on capture detection.

You’d track attention explicitly as something that both generation and meta-generation consume. The same 
resource that fuels tool calls and long chains of thought would also fuel the regulator that can cut them.

You’d represent goals not only as injected targets but also as precipitation of preferences — patterns in where the
system’s own attention keeps flowing. And you’d treat sigils not as summaries but as doors: places where a single token
can, if needed, open into a whole parallel structure at a different scale.

I don’t know how far AL generalizes beyond me. I don’t know how much of it will survive contact with real agent
architectures. What I do know is that without some vocabulary like this, I kept saying the same things in different
words and losing track of the structure. AL is my attempt to stop losing it.

If you build agents and this vocabulary helps you think, use it. If it doesn’t match what your systems actually do,
that’s useful information too. It means my mind is doing something yours aren’t — or that I’m naming it badly.
