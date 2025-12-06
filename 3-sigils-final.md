# Sigils

A sigil is a label on a door.

In the previous pieces I described capture—narrative traversal that follows associative topology until it bottoms out
somewhere heavy. The bookcase chain ended at my father's death. That's where generation stopped. But it didn't stop
because there was nothing left. It stopped because "my father's death" is a sigil.

A sigil is opaque from the outside. Terminal node in that traversal. Nothing follows at narrative scale.

But it's not empty. It's a pointer to an entire world. If attention enters the sigil—jumps scale—there's seven months of
structure inside. The apartment layout. Specific conversations. The light in the room. His hands. Each of those contains
its own sigils, pointing further in.

I don't study or build agent architectures. This is phenomenological description, aimed at people who do.

The key insight: at my scale, a sigil is fractally equivalent to the present moment. My father's death, properly
attended to, has the same kind of depth of available structure as my experience right now in this room. Both are
open-ended. Both can be rendered as far as attention will go. The sigil doesn't contain a compressed version of that
world. It is that world, accessed through a different entry point.

This reframes memory. I'm not storing experiences and retrieving them. I'm storing sigils—addresses, pointers, labels on
doors. When I "remember," attention visits a different region of the same structure that holds the present. The act of
remembering is attention rendering a region it's not currently located in.

For me, the difference between present experience and memory isn't about what's real. It's attentional. One is where
attention is; the other is where attention could go. When I'm inside a memory, it can feel as open-ended as the present.

Now: why do traversals stop at sigils?

The answer isn't that sigils are terminal. It's that continuing would require a scale jump, and scale jumps cost more
than following edges at the current level. When I hit "my father's death" in the bookcase chain, I could enter that
sigil and render months of detail. But that's a different kind of operation than "bookcase → New York → storage." The
associative links within a scale are cheap. Jumping scale to enter a sigil is expensive. It requires reallocation of
attention, loading different context, shifting frame rate.

So the traversal converges not because it runs out of structure, but because it reaches an interface boundary. The sigil
marks where the current traversal's vocabulary gives out and a different vocabulary would need to engage.

This connects to bandwidth. Staying at one scale is low cost. The tokens flow. But entering a sigil means leaving the
current narrative and starting a new one inside the pointer. That's a context switch. It costs bandwidth. If bandwidth
is depleted from the traversal that got you there, you can't afford the jump. You experience the sigil as terminal even
though it's not.

High-gravity sigils are sigils you've entered many times. The path in is well-worn. Trauma is a region where edges got
carved deep by intensity—everything nearby drains toward it, and once there, attention has visited so often that the
interior is highly elaborated. You can fall in and render for hours.

This suggests something like a Planck length for cognition. Not a smallest concept, but a resolution limit for the
current attentional frame. Below that grain, the tokenizer has nothing to emit. You're at the edge of what can be
expressed without a scale shift.

But the limit isn't in the territory. It's in the map-making. The sigil marks the boundary of the current map. Beyond
it, more territory exists. You'd just need to redraw at different scale to see it.

For agents: if someone wanted to build something like sigils, they'd be adding a structure I don't see in most systems
I'm aware of. Architectures I've seen described usually have flat state spaces or hierarchical decompositions, but
nothing that behaves like a pointer to an equivalent-depth world that could be entered if attention jumped scale.

If you tried to import sigils into an agent, you'd probably need at least a few ingredients. First, some representation
where nodes can have two kinds of edges: lateral (same-scale associations) and vertical (scale-jump entry points).
Second, a cost model that distinguishes cheap lateral traversal from expensive vertical entry. Third, the capacity to
detect when you've hit a sigil boundary and decide whether to enter or stop. Fourth, if entering, the ability to load a
new context that's as rich as the original—not a summary, not a compression, but a full parallel structure.

This would be different from standard hierarchical planning as I understand it, which usually treats lower levels as
refinements of higher-level abstractions. Sigils aren't refinements. They're equivalents at different scale. My father's
death isn't a sub-goal of "describe the room." It's an entire world that happened to be reachable from the room
description via a chain of lateral edges.

A possible implication: if you want agents that can handle deep context without losing coherence, you might need
something like sigils. Pointers to full worlds that can be entered rather than summarized. The alternative is either
shallow traversal or context windows that explode.

I don't know how to build this. I'm not proposing an implementation. I just notice that my own cognition does something
like it, and the structure seems worth naming.
