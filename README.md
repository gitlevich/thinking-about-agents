# Thinking About Agents

This is a series about agents. I don't build them. I watch myself think and describe what I see.

I'm a software architect with thirty years of practice. I've spent time on domain modeling—finding the right
abstractions before committing to code. That's the mode I'm in here. Not implementation, not empirical research. Just
careful description of one mind's operation, aimed at people who might find it useful for building minds that aren't
theirs.

The series has three pieces:

[The first](1-why-your-agent-gets-captured.md) names a failure mode. Agents spiral—planning loops that won't
terminate, critics that elaborate forever, tool chains that keep firing. I call it capture. It happens when generation
consumes the resources that would be needed to interrupt generation. I describe what capture feels like from inside, and
sketch what an architecture with explicit modes, bandwidth, and a regulator might look like.

[The second](2-how-goals-precipitate.md) asks where goals come from. Most architectures I’ve seen described take goals
as parameters. But in my own experience, sometimes goals precipitate from preferences. Preference pulls attention,
attention collapses into pattern, pattern crystallizes into goal. I trace that sequence and suggest what emergence might
require.

[The third](3-sigils.md) introduces sigils. A sigil is a label on a door—opaque from outside, containing a world
inside. In this framing, memory isn't storage and retrieval. It's attention visiting regions of a structure that also
holds the present. I describe why traversals stop at sigils, what it would mean to enter one, and what this might imply
for agents handling deep context.

Each piece includes toy code. The code isn't production architecture. It's a way of checking whether the descriptions
are coherent enough to run. Theory predicts behavior; if the behavior matches, the description isn't empty.

I'm a late bilingual. Russian native, English acquired as an adult. This left me with visibility into my own
tokenization—I can watch the conversion of experience into language as it happens. Most of what I describe comes from
that visibility. It's a sample size of one. I don't know how far it generalizes.

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

*Vladimir Gitlevich is a software architect and founder of DDD-NYC. He lives in San Francisco. This series developed
over months of conversations with ChatGPT and was drafted in one night with Claude Opus.*
