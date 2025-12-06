# Sigils

A sigil is a label on a door.

In the previous pieces I described capture — narrative traversal that follows associative topology until it bottoms out
somewhere heavy. The bookcase chain ended at my father's death. That's where generation stopped. But it didn't stop
because there was nothing left. It stopped because "my father's death" is a sigil.

A sigil is opaque from the outside. Terminal node in that traversal. Nothing follows at narrative scale.

But it's not empty. It's a pointer to an entire world. If attention enters the sigil — jumps scale — there's seven
months of
structure inside. The apartment layout. Specific conversations. The light in the room. His hands. Each of those contains
its own sigils, pointing further in.

```text
Disclaimer: I don't study or build agent architectures. This is phenomenological description, aimed at people who do.
```

The key insight: at my scale, a sigil is fractally equivalent to the present moment. My father's death, properly
attended to, has the same kind of depth of available structure as my experience right now in this room. Both are
open-ended. Both can be rendered as far as attention will go. The sigil doesn't contain a compressed version of that
world. It is that world, accessed through a different entry point.

This reframes memory. I'm not storing experiences and retrieving them. I'm storing sigils — addresses, pointers, labels
on
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
marks where the current traversal's vocabulary gives out, and a different vocabulary would need to engage.

This connects to bandwidth. Staying at one scale is low cost. But entering a sigil means leaving the
current narrative and starting a new one inside the pointer. That's a context switch. The agent effectively enters a
different bounded context. It costs bandwidth. If bandwidth is depleted from the traversal that got you there, you can't
afford the jump. You experience the sigil as terminal even though it's not.

High-gravity sigils are sigils that are highly relevant at this scale. Attention keeps sliding into them, so the path in
becomes well-worn. Trauma is a region where edges got carved deep by intensity — everything nearby drains toward it, and
once you’re there, attention has visited so often that the interior is highly elaborated. You can fall in and render for
hours. The many entries are a symptom, not the cause, of the gravity: the sigil pulls because it matters here.

This suggests something like a Planck length for cognition. Not a smallest concept, but a resolution limit for the
current attentional frame. Below that grain, the tokenizer has nothing to emit. You're at the edge of what can be
expressed without a scale shift.

But the limit isn't in the territory. It's in the map-making. The sigil marks the boundary of the current map. Beyond
it, more territory exists. You'd just need to redraw at different scale to see it.

For agents: if someone wanted to build something like sigils, they’d need a structure where some nodes behave as
pointers to full worlds at a different scale, not just as states in a flat or hierarchical space. Nodes that can be
entered as worlds, not just visited as labels.

That would mean at least two kinds of edges in the model. Lateral edges: same-scale associations, cheap to traverse,
what the bookcase chain was using. Vertical edges: scale jumps, from a sigil into its interior world and back out via a
context stack. On top of that, a cost model that makes vertical moves more expensive than lateral ones, so “enter” isn’t
just another step but a bandwidth decision.

You’d also need a way to notice that you’ve hit a sigil boundary. A place where the current vocabulary starts to give
out and a different one would have to take over. In code, that’s just a tagged node and a call to push a new topology.
In lived experience, it’s the felt edge of a frame: “if I go further here, I’m not just elaborating this story, I’m
entering a different world.”

This is different from standard hierarchical planning as I understand it, where lower levels are usually refinements of
higher-level abstractions. Sigils aren’t refinements. They’re equivalents at different scale. “My father’s death” isn’t
a sub-goal of “describe the room.” It’s an entire world that happens to be reachable from the room description via a
chain of lateral edges.

If that kind of structure existed in an agent, it might be a way to handle deep context without just making the context
window bigger. You could keep lateral traversal cheap and local, and reserve the expensive scale jumps for the sigils
that actually matter. Pointers to full worlds that can be entered when needed, not summaries you drag around everywhere.

I don’t know how to build that. What I do know is that my own cognition behaves as if something like sigils is already
there. Naming them is a way to keep track of that structure. [This code](attention_agent_extended.py) is a toy version
of that idea, nothing more.
