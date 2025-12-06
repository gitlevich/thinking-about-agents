# Thinking About Agents

This is a series about agents. I don't build them. I watch myself think and describe what I see.

I've been designing and writing software for about thirty years, mostly around domain modeling and architecture. I also
shoot a lot of photographs and read across domains: physics, cognitive science, philosophy, people like Wolfram,
Hoffman, Vervaeke, and others. Over time I kept seeing the same shapes in very different places: similar topologies,
similar preferences, similar stories about attention. Agent Language is what precipitated from that.

The series has these pieces:

**[Why Your Agent Gets Captured](1-why-your-agent-gets-captured.md)**  
Names a failure mode. Agents spiral—planning loops that won't terminate, critics that elaborate forever, tool chains
that keep firing. I call it capture. It happens when generation consumes the resources that would be needed to interrupt
generation. I describe what capture feels like from inside, and sketch what an architecture with explicit modes,
bandwidth, and a regulator might look like.

**[How Goals Precipitate](2-how-goals-precipitate.md)**  
Asks where goals come from. Most architectures I’ve seen described take goals as parameters. In my own experience,
sometimes goals precipitate from preferences. Preference pulls attention, attention collapses into pattern, pattern
crystallizes into goal. I trace that sequence and suggest what emergence might require.

**[Sigils](3-sigils.md)**  
Introduces sigils. A sigil is a label on a door—opaque from outside, containing a world inside. In this framing, memory
isn't storage and retrieval. It's attention visiting regions of a structure that also holds the present. I describe why
traversals stop at sigils, what it would mean to enter one, and what this might imply for agents handling deep context.

**[Agent Language](4-agent-language.md)**  
Introduces Agent Language (AL). AL is a minimal first-person vocabulary for talking about agents, their experience, and
their choices: contrasts, observations, observers, agents, goals, preferences, bandwidth, choices, narratives, capture,
sigils, and scale. The point isn’t to be complete, but to stop re-inventing words for the same structures.

**[Entangled Agents](5-entangled-agents.md)**  
Describes entanglement. Entanglement is present-tense mutual influence between agents at the same scale under a shared
goal. I describe what it feels like from inside when a “we” forms as a higher-scale agent, how bandwidth and capture
behave in that regime, and what this might mean for multi-agent systems that are meant to collaborate rather than just
pass messages.

**[Frames](6-frames.md)**  
Unpacks frames. A frame is the configuration of active contrasts and their current observations, held together long
enough to feel like “this moment.” I talk about contrasts as dimensions, resolution, frame rate, bounded attention, and
how word paintings (token streams) are projections of frames. Frames are where the world actually shows up for an agent;
agents and narratives are layered on top.

**[A Walk Through My Tokenizer (Annotated)](7-worked-example.md)**  
A worked example: a real-time word painting annotated in AL. I turn the tokenizer on, let the narrative run, and mark
mode switches, frame changes, gravity wells, sigils, and regulator actions inline. The earlier pieces were
reverse-engineered from sessions like this; this one shows the machinery running once, in the wild.
Each piece includes toy code. The code isn't production architecture. It's a way of checking whether the descriptions
are coherent enough to run. Theory predicts behavior; if the behavior matches, the description isn't empty.

---


I'm a late bilingual. Russian native, English acquired as an adult. This left me with unusual visibility into my own
tokenization—I can watch the conversion of experience into language. Most of what I describe comes from that
visibility, plus years of bouncing between different domains and noticing the same structures repeat. It's a sample size
of one. I don't know how far it generalizes.

If you build agents and something here is useful, use it. If it's wrong, you'll find out faster than I will.


## Running the demos

All code is plain Python 3 with no external dependencies.

Clone the repo and change into the directory:

```bash
git clone https://github.com/gitlevich/thinking-about-agents.git
cd thinking-about-agents
```

Then run any of the toy agents from the command line:

```bash
python attention_agent.py
python attention_agent_extended.py
python goal_precipitation.py
```

Each script prints a short trace of the agent’s behavior to stdout. The parameters and topologies are defined at the top
of each file and are meant to be tweaked.

---

*Vladimir Gitlevich lives in San Francisco. He designs and writes software, does photography, and spends too much time
thinking about attention and agents. This series developed over months of conversations with ChatGPT and was drafted in
one night with Claude Opus.*
---
