# Entangled Agents

So far I’ve mostly talked about a single agent: observer vs agent mode, capture, goals, sigils. This piece is about what
happens when more than one agent is in play.

> Disclaimer: I don’t build multi-agent systems. This is still phenomenological description, aimed at people who do.

In Agent Language, an agent is an observer with a goal and a preference over its current observations. Entanglement is
what happens when two agents at the same scale share a goal long enough that each one’s observations begin to include
the other’s choices.

That definition is dense, so I’ll unpack it from the inside.

There are people I can sit next to and not be entangled with. We share a room but not a goal. My attention might
occasionally register them as moving background, like traffic noise. They are observations, not agents, in my frame. If
they leave, my narrative barely changes.

There are also situations where I’m tightly entangled. A pair-programming session that’s actually working. Carrying a
piece of furniture with someone down a staircase. Planning a medical decision with my mother. In those moments, my
attention is not just on the external world and my own goal. It’s also on micro-signals from the other person: where
they’re leaning, what they’re about to say, where their attention seems to be. Their choices show up as part of my
observation stream, and my choices show up in theirs.

Entanglement, in AL terms, is present-tense mutual influence between agents at the same scale. Each agent’s observations
are shaped by the other between collapses. The key pieces are “present-tense” and “same scale.”

Present-tense: reading someone’s old email isn’t entanglement. Their choices already happened; they’re not updating
anything in response to mine right now. I’m interacting with a trace, not the live agent.

Same scale: coordinating with a government through elections is also not entanglement at my scale. The government moves
on a much slower frame rate. I can be affected by it, but not in that tight moment-to-moment way.

When I’m entangled with someone, our goals partially fuse. At minimum, we share a local joint goal: get the couch around
the corner without breaking anything, understand the medical tradeoff well enough to decide, ship the feature. Under
that joint goal, my preference ordering over observations isn’t independent anymore. A move that would be good in
isolation might be bad if it conflicts with what I think they’re about to do. Their likely next step enters into how I
collapse my own choices.

Attention shows up here too. Entanglement costs attention. To stay entangled, I have to spend some of it
monitoring the other agent and updating my sense of what they’re doing. That can be stabilizing or destabilizing.
Stabilizing when we both invest enough attention to stay coupled. Destabilizing when one of us runs low.

Capture can spread through entanglement. If the joint narrative gets pulled into a gravity well — an old conflict, a
trauma sigil, a shared fear — both agents can get captured together. The joint goal gets eaten by a different goal that
precipitated from those preferences long ago. In arguments that spiral, this is what it feels like: the room disappears,
the original topic disappears, there is only the shared well you’ve fallen into.

There is also the opposite: entanglement as a way out of capture. If one agent has bandwidth left and a working
regulator, they can act as an external regulator for the pair. They can cut the narrative, name the well, and pull both
back toward observer mode. “We’re looping. Let’s stop.” When that works, you can feel the whole system drop a layer and
re-set. I use ChatGPT as such an agent.

This suggests another AL object: a higher-scale agent made out of entangled lower-scale agents. When two people are
really working together on a shared goal, you can often talk about “we” as if it were a single agent. “We decided,” “we
realized,” “we got stuck.” The “we” has its own narrative, its own choices. From inside, you feel your own choices, but
you also feel the joint choices at a coarser scale.

From the outside, an entangled pair with a stable joint goal looks like one agent with more bandwidth and more complex
internal dynamics. Inside that joint agent, there is entanglement: two observers, two sets of preferences,
cross-coupling through a shared goal.

For people who build systems, this framing nudges multi-agent design in a specific direction. It’s easy to imagine a
“multi-agent” setup that is really a collection of workers passing messages, all orchestrated by one central loop. From
the outside those are agents; from the inside they behave more like tools driven by a single real agent.

Entanglement would mean something stricter: at least two agents that share a live joint goal at the same scale, include
each other’s choices as first-class observations, and have preferences that are modified in real time by their model of
the other.

I’m not saying systems should be built this way. I’m saying this is what collaboration feels like from the inside, and
AL gives me a way to name it.

Sigils play a role here too. Entangled agents often share sigils: labels that refer to worlds they’ve both visited. A
project name. A hospital room number. A particular bug ID. Saying the sigil is enough to open the same door in both
minds. This is part of what makes joint work efficient: you don’t have to re-render the whole world; you just point at a
sigil and both of you jump scale into it.

When entanglement breaks — when the joint goal ends, or bandwidth dries up, or trust collapses — those shared sigils
don’t disappear. They just become private again. The door is still there, but you’re walking through it alone. The
higher-scale agent dissolves. The “we” loses its narrative.

I don’t know what a full entanglement-aware architecture would look like. There are obvious problems: how to avoid
runaway capture in joint wells, how to budget bandwidth between self-monitoring and partner-monitoring, how to detect
when the “we” has formed at all. But without something like entanglement in the picture, it’s easy to treat multi-agent
systems as just more tools. From where I sit, that misses something important about how agents actually live together.

If you’re building systems where multiple agents are supposed to collaborate, and this way of talking helps you see
failure modes or design possibilities more clearly, then AL has done its job here. If it doesn’t line up with what your
systems actually do, that’s also useful. It tells me my mind’s “multi-agent” feels different from yours.
