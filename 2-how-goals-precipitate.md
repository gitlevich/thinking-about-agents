# How Goals Precipitate

The previous piece left goals as injected parameters. The agent receives a target, climbs toward it, uses the
goal-gradient to distinguish productive traversal from capture. That’s useful but incomplete. It doesn’t explain where
goals come from.

In my experience, goals aren’t always prior. Often they precipitate from preferences. Sometimes it goes the other way:
goals are imposed and preferences re-shape around them. It’s the same structure seen at different moments.

> Disclaimer: I haven’t built large agent systems. This is phenomenological observation and architectural sketching,
> aimed at people who do.

Start with preference. Preference isn’t a list of things I want. It’s a property of the topology: the shape of how
concepts connect for me, where gradients are steep, what pulls attention without effort. I don’t decide to prefer. I
notice that attention went somewhere.

In observer mode, the frame isn’t uniform. Some regions have higher contrast: light falling a certain way, a color
relation, a sharp edge in a concept. Attention gets pulled there. That’s the field meeting the wiring of the agent.

By attending, I stabilize a frame. Each observation narrows what I’m likely to notice next so it coheres with what I’m
already rendering. If I attend to the light on the bookshelf, the next moment of attention is shaped by that. I’m not
scanning neutrally anymore. I’m continuing a pattern.

The pattern isn’t found. It’s constituted by attentional continuity. Attention provides the substrate for it to
stabilize. After enough repetitions, the pattern has momentum. It starts to look like something I’m pursuing—a goal.
That’s retrospective framing.

The picture I’m offering is: preference pulls attention, attention narrows possibilities, choices accumulate into
continuity, continuity crystallizes into goal. They’re mutually derivable. Preference is goal before crystallization.
Goal is preference after enough continuity has built up. Same structure at different moments of its evolution.

Sometimes this runs from below. Attention shimmers over a topographically interesting region, keeps revisiting the same
contrasts, and a direction stabilizes. That direction is what later gets named as a goal. Sometimes it runs from above.
A goal is imposed from outside, and the preference field is re-oriented to serve it. In practice, it is usually both.

Injected goals feel imperative to me. They arrive from nowhere relative to this agent’s own history. The agent doesn’t
get to bring its local preferences to bear; it is just told “optimize this.” It’s like asking an object-oriented
developer to write everything in flat procedural code. They can do it, but you are not using the structures their mind
already prefers.

If goals are always injected, there’s no mechanism to notice what the system is already attending to, sustain that
attention, and let a goal precipitate from the sustained pattern.

Designing for emergent goals needs at least a preference landscape: something like topology, not just a flat state
space, but weighted connections, regions of different density, gradients that exist before any task. That structure can
be learned from prior trajectories, encoded by the designer, or inherited from a foundation model’s latent space.

Undirected attention is next. Before goal injection, the agent has to observe without generating toward a target. Let
attention move along preference gradients. This is the observer mode from the previous piece, now with a purpose:
sensing high-contrast regions where attention naturally falls.

Then tracking. As attention visits regions, the agent records its choices as a trajectory. Repeated visits, lingering,
and strong salience along particular contrasts are evidence of preference expressing itself. The agent isn’t deciding
what to want. It’s detecting what it is already drawn toward.

A crystallization threshold closes the loop. At some point the accumulated pattern is stable enough to function as a
goal. The same observer now has a goal riding on top of its frames and starts acting as an agent, but this time the goal
wasn’t injected. It precipitated from the agent’s own attentional history. This isn’t goal selection from a menu. It’s
goal formation from within.

The flow also goes the other way. A goal can precipitate from preferences, or an imposed goal can reshape preferences.
When circumstances force a goal on you—deadline, crisis, someone else’s demand—that goal doesn’t just sit on top of the
existing topology. It changes where attention falls. The imposed goal becomes an attractor, and preferences reorganize
around it. Precipitation and imposition are symmetrical: preferences crystallize into goals, and goals dissolve back
into preferences.

This reframes what it means to build a domain expert. Expertise isn’t a list of goals. It’s a shaped topology. A senior
architect looks at a system and attention falls toward coupling problems, not because anyone specified that goal, but
because years of practice carved those gradients. You don’t tell the expert what to find. The expert’s preferences
surface what matters. Building a domain-expert agent, then, isn’t mainly about injecting the right goals. It’s about
shaping the preference landscape. Goals precipitate when shaped preferences meet specific material.

This is not exploration in RL. There the reward function is fixed and external, and exploration searches state space to
maximize that objective. Here the “reward” is implicit in the preference landscape and only later becomes explicit as a
goal. The agent ends up wanting something because it kept attending to it, and it kept attending because the topology
made that region salient.

The preference landscape is simpler than a full list of goals. Preferences are local gradients; goals are the stable
directions those gradients trace over time. You can have rich preference structure without ever naming goals. Goals are
what preferences become when the system runs long enough.

In my own case, most goals precipitate. I didn’t start with “become a photographer” and pursue it. Attention kept
getting captured by light. Patterns accumulated. At some point the word “photographer” became a useful label for a goal
that had already crystallized from years of preferential attention. The goal was downstream of preference, not prior to
it.

The toy implementation from the previous post doesn’t do this. It still takes goals as parameters. The extended version
adds a preference-weighted topology (already implicit in the gravity values), an observation phase before goal
injection, tracking across multiple traversals (a simple visit and dwell-time counter), and a threshold that promotes
accumulated preference into an active goal.
