# Why Your Agent Gets Captured

Agents spiral. The planning loop that won't terminate, the critic that elaborates indefinitely, the tool-use chain that keeps firing long past usefulness. Standard response: add exit conditions, tune prompts, insert reflection steps. These are patches. They don't touch the failure mode because there's no theory of what's happening.

Here's a model that comes from sustained observation of my own cognition and from thinking about how we might build agents that share these failure modes.

I'm a late bilingual—Russian native, English acquired as an adult. This accident of biography left me with something unusual: I can watch the conversion of experience into language. Most people's inner monologue is transparent to them. Mine isn't. I have a tokenizer running, and I can see it tokenize.

I haven't built large agent systems myself. This is a phenomenological and architectural sketch, aimed at people who do.

Two modes appear when I pay attention.

In observer mode, I'm present to the current frame of experience without narrating it. High bandwidth, low energy cost. The sensorium flows through without conversion to symbol.

In agent mode, attention has been captured by a narrative. I'm generating—traversing some chain of associations, producing tokens, following a trajectory through concept-space. This mode has momentum.

Here's what happens when I try to describe the room I'm in. There's a bookcase. I bought it in New York around 2008. It went to storage in San Bruno, then to an apartment at 9 Lafayette for thirteen years, then to 1550 Mission during my father's final seven months.

I wasn't trying to get to my father's death. I was describing furniture. The associative topology pulled me there. Each token conditioned the next until the chain hit a terminus too heavy to traverse past without deliberate effort.

That's capture. Generation following local gradients until it bottoms out in a gravity well.

The transition between observer and agent matters. A delta in the perceptual field—something salient, some contrast—triggers a minimal agent: investigate the disturbance. Short trajectory, should complete and return to observer. But sometimes an edge in the investigation leads somewhere. Association triggers association. Generation begins. The bookcase pulled 2008, which pulled storage, which pulled the old apartment, which pulled the new one, which pulled the death. None of those steps felt like a choice. That was the topology expressing itself through the bandwidth it had.

I use "bandwidth" as a single abstract resource standing in for attention, energy, and compute—distinct but usually moving together. Generation competes with everything else for this resource, including the meta-cognitive process that could interrupt generation. Call it the regulator. The regulator monitors whether the current trajectory is productive and can cut the narrative to return to observer.

But the regulator needs bandwidth to run.

Heavy narrative starves it. The process that should interrupt capture gets outcompeted by the capture itself. Full capture means the regulator has nothing to execute with. You ride until convergence.

The topology isn't flat. Some regions of concept-space are densely connected, high-mass—attention falls toward them without effort. Without a goal providing counter-gradient, you roll downhill into whatever basin is nearby.

Goal-directed generation differs because the goal creates a gradient you're climbing. Tangents become visible as tangents: lateral or downward relative to where you're headed. The regulator can evaluate whether current expenditure produces altitude gain.

Most agent architectures I see today lack an observer mode. They're always generating. There's no low-energy state to return to, no baseline that isn't narrative. For implementers: observer mode isn't idling between calls. It's an explicit low-cost loop that updates a world model and monitors for salient contrasts, with generation turned off. The agent is still running, just not producing tokens.

As usually built, they have no explicit bandwidth model. Generation is treated as free. There's no representation of meta-cognition requiring resources that generation might exhaust.

Their "reflection" is just more generation, with no capture detection. They can't recognize when they've fallen into a gravity well.

And where there is self-monitoring, it rarely has teeth: it can't hard-interrupt and return to observer.

An alternative architecture would have explicit modes with different resource profiles. Observer is default. Agent is entered deliberately and exited on trajectory completion or capture detection. Bandwidth is finite, depleted by generation, required for meta-cognition. Capture detection monitors for circular reasoning and goalless drift. The regulator can interrupt—not another voice in the generation, but a hard cut that clears context and forces return to observer. In code, I approximate these with cycles in the path, long goalless trajectories, and high-gravity terminal nodes.

This leaves open the question of goals. The architecture above still takes goals as injected parameters. A further direction—not implemented here—would let goals precipitate from preference gradients through sustained attention. The agent would develop goals the way minds do: by noticing what attention is already drawn toward, then rendering continuity until the pattern crystallizes. That's a separate research program, on top of the architecture here.

The code below instantiates the mode/bandwidth/capture/regulation part of the model. Toy domain, but the control structure is real. An agent that can observe, generate, get captured, detect capture, and recover. It traverses the bookcase topology. The theory predicts the behavior.
