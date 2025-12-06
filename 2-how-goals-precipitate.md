# How Goals Precipitate

The previous piece left goals as injected parameters. The agent receives a target, climbs toward it, uses the
goal-gradient to distinguish productive traversal from capture. That's useful but incomplete. It doesn't explain where
goals come from.

Here's the continuation: goals aren't prior to attention. They precipitate from it.

I haven't built large agent systems. This is phenomenological observation and architectural thinking, aimed at people
who do build them.

Start with preference. Preference isn't a list of things I want. It's a property of the topology—the shape of how
concepts connect for me, where the gradients are steep, what pulls attention without effort. I don't decide to prefer. I
notice that attention went somewhere.

In observer mode, the visual field isn't uniform. Some regions have higher contrast—light falling a certain way, a color
relation, an edge. Attention gets pulled there. Not a choice. A property of the field meeting a property of the system.

By attending, I collapse. Each observation constrains subsequent observations to cohere with what I'm already rendering.
If I attend to the light on the bookshelf, the next moment of attention is shaped by that. I'm not scanning neutrally
anymore. I'm rendering a pattern.

The pattern isn't found. It's constituted by attentional continuity. I provide the substrate for it to persist.

After enough collapses, the pattern has momentum. It starts to look like something I'm pursuing. A goal. But that's
retrospective framing. The picture I'm offering is: preference pulls attention, attention collapses possibilities,
collapse accumulates into continuity, continuity crystallizes into goal.

They're mutually derivable. Preference is goal before crystallization. Goal is preference after sufficient collapse. The
same structure at different moments of its evolution.

There's a gap here. If goals are always injected, there's no mechanism to notice what the system is already attending
to, sustain that attention, and let the goal emerge from the sustained pattern.

What would emergence require? I can think through the components, though I'm not the one who would build them.

A preference landscape. The agent needs something analogous to topology—not just a flat state space but weighted
connections, regions of varying density, gradients that exist prior to any task. This could be learned from prior
trajectories, encoded by the designer, or inherited from a foundation model's latent structure.

Undirected attention. Before goal-injection, the agent would need to observe without generating toward a target. Let
attention move according to preference gradients. This is observer mode from the previous piece, but now with a purpose:
sensing where attention naturally falls.

Collapse tracking. As attention visits regions, the agent records the trajectory. Repeated visits, lingering,
high-contrast responses—these are evidence of preference expressing itself. The agent isn't deciding what to want. It's
detecting what it's already drawn toward.

A crystallization threshold. At some point, the accumulated pattern becomes stable enough to function as a goal. The
agent shifts from observer to directed agent, but now the goal wasn't injected—it emerged from the agent's own
attentional history.

This is not goal selection from a menu. It's goal formation from within.

But the flow goes both ways. A goal can precipitate from preferences—or an imposed goal can reshape preferences. When
circumstances force a goal on you (deadline, crisis, someone else's demand), that goal doesn't just sit on top of your
existing topology. It changes where attention falls. The imposed goal becomes an attractor, and preferences reorganize
around it. Precipitation and imposition are symmetrical: preferences crystallize into goals, and goals dissolve into
preferences.

This reframes what it means to build a domain expert. Expertise isn't a list of goals. It's a shaped topology. A senior
architect looks at a system and attention falls toward coupling problems, not because anyone specified that goal, but
because years of practice carved those gradients. You don't tell the expert what to find. The expert's preferences
surface what matters.

Building a domain expert agent, then, isn't about injecting the right goals. It's about shaping the preference
landscape. Goals emerge when shaped attention meets specific material.

The objection: isn't this just exploration with extra steps? No. In typical exploration, the reward function is fixed
and external. Here the "reward" is implicit in the attention field, then later made explicit as a goal. Exploration
searches state space to maximize some externally defined objective. Goal precipitation lets the objective itself emerge
from the shape of attention over time. The agent ends up wanting something because it kept attending to it, and it kept
attending because the topology made that region salient.

Another objection: doesn't this just push the problem back to the preference landscape? Partially. But the preference
landscape can be simpler than a fully specified goal. Preferences are local gradients: this region is more salient than
that one. Goals are global targets: go there. You can have rich preference structure without having named goals. Goals
are what preferences become when the system runs long enough.

In my own case, this is how most goals actually work. I didn't start with "become a photographer" and pursue it.
Attention kept getting captured by light. Patterns accumulated. At some point the word "photographer" became a useful
label for a goal that had already crystallized from years of preferential attention. The goal was downstream of the
attention, not prior to it.

The toy implementation from the previous post doesn't do this. It takes goals as parameters. A next version would add: a
preference-weighted topology (already implicit in the gravity values), an observation phase before goal-injection,
collapse tracking across multiple traversals (could be as simple as a counter and dwell-time per node), and a threshold
that promotes accumulated preference into active goal.
