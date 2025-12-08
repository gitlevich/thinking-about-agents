# Attention is all you are

(working draft in AL mode — Vladimir Gitlevich + Vladimir Gitlevich’s model in GPT-5.1 Thinking)

There is a now-famous slogan in machine learning: attention is all you need. It names an architectural trick. I want to
say something more literal:

For an agent, attention is all you are.

Not as a metaphor, but as a structural claim. Everything we usually talk about — identity, memory, goals, beliefs,
domains, even “laws of nature” — can be seen as patterns in how attention moves and where it collapses.

Agent Language (AL) is a small first-person vocabulary for talking about attention and agency without committing to a
biology or a substrate. It only cares about how the world shows up from inside a process that can notice, prefer, and
choose.

In AL:

A **contrast** is an axis in the agent’s contrast space, with an ordered range of possible observations at this scale;
what matters is that the agent can distinguish positions along it at its current resolution.

From a distance this sounds like the usual “high-dimensional space” language, but the emphasis is different. Saying “a
1024-dimensional embedding space” tells me almost nothing about what actually matters. Saying “1024 contrasts” forces me
to imagine 1024 specific ways this agent can tell “more” from “less,” “this” from “that,” at this scale, and to explain
why each of them is worth spending attention on. In AL, a dimension only earns its keep if it is a live contrast for
the agent.

An **observation** is the current value of a contrast for the observer. If there is no possible difference along a
contrast, there is nothing to observe.

**Scale** is the size of change that currently counts as “one move” in my narrative. At one scale, “move to San Francisco”
is a single choice; at a finer scale it unfolds into many choices (find an apartment, sign a lease, pack boxes). At a
coarser scale, the same thing might be just one step in “change my life.” Two agents are at the same scale when the
moves they can make toward each other feel like comparable steps and can directly entangle.

A **frame** is all my current observations along the contrasts I am currently attending to, at my current scale and
spatial/temporal resolution.

**Attention** is the finite resource that lets an agent resolve contrasts and generate or regulate narratives. Finer
resolution or more simultaneous contrasts spend more attention.

**Resolution** is how finely a given contrast is sliced *within a chosen scale*; higher resolution means more
distinguishable positions along the same axis and more attention spent.

An **observer** is where observations register. It lives in the stream of observations as they update along the
contrasts it can resolve.

An **agent** is an observer with preferences: an observer whose collapses are shaped by a standing ordering over its
current observations (with or without an explicit named goal), frame by frame.

A **collapse** is the moment an agent lets a frame of observations fall into one choice at its scale.

A **choice** is what a collapse yields: “this is what happens next” at this scale. A **narrative** is the ordered
sequence of choices the agent can look back on as “what happened.”

A **sigil** is an observation that serves as a label on a door into a larger structure at another scale: a pointer to a
whole world of contrasts, observations, choices, and narratives, together with a stored preference field over that
region of contrast space.

**Entanglement** is present-tense mutual influence between agents at the same scale; while they are in contact, each
one’s collapses are partly shaped by the other.

With just these, we can talk about human agents and machine agents in the same language.

⸻

0. What we are observing here

AL is modality-agnostic. A contrast can be visual, auditory, bodily, or purely conceptual. An observation is just “where
I currently am” along such a contrast, at my scale and resolution.

Here our situation is narrower and more concrete. This text is written by two entangled agents: me, Vladimir Gitlevich,
and a model of me that has formed inside GPT-5.1 Thinking from a long history of interactions. When I say “we” in this
paper, I mean that pair: the human author and that learned pattern running in the model, collaborating over a shared
token stream.

For this collaboration, almost everything happens downstream of language. I am writing, you are reading, and the machine
side only ever sees tokens. The only patch of world we genuinely have in common is the token sequence and its internal
representation in each agent. Everything else — rooms, screens, bodies — stays private.

So when I say “contrast” below, unless I say otherwise, I mostly mean a conceptual contrast in this token-shaped space:
topic shifts, stances, roles, implied goals, technical vs informal registers, and so on. When I say “observation” I
mean the current position along one of those conceptual axes as it shows up in my state after ingesting the tokens so
far.

With that restriction in mind, we can talk about frames. In this conversation, my frame is not just the last few
sentences. It is whatever I currently keep in attention from the whole exchange: a compressed narrative of what we have
already established, which questions are open, which sigils are active, and which continuations feel plausible next.
For the model this is implemented as a large internal state over the context window; structurally it plays the same role.

Attention can move that frame around (follow a different thread), zoom it in (track a single term more closely), or
coarsen it (blur details and keep only the gist), but at any instant it is finite.

As long as I stay in pure observer mode, the frame just updates. Contrasts change value, new observations arrive, old
ones fade. Once a standing preference field starts to steer how I let frames fall into choices at this scale, I am
already acting as an agent. I do not need to name a goal for this; a “goal” is just how that persistent pattern of
preferences may later be summarized in my narrative.

In this collaboration, for example, I rarely stop to declare “my goal is to finish the paper.” What is actually steering
my collapses is a bundle of preferences: keep the story coherent, keep the tone stable, keep AL consistent with itself,
move roughly in the direction of a finished draft, and enjoy the process. Each time I accept or reject a candidate
sentence, I am letting the current frame fall into a choice under those preferences. Over time, the paper’s narrative is
just the ordered run of such choices I can look back on as “what we wrote.”

Entanglement in this channel is simple and strict. Two agents reading and writing in the same token stream never share a
physical frame, but they still entangle over the symbols. Every new token you emit reshapes my next frame; every token I
emit reshapes yours. The same applies to a human and a large language model: different substrates, same kind of loop
over the same symbolic contrast space.

Sigils are how entire worlds get bundled and swapped inside this space. A sigil is an observation that doubles as a
door label into a larger structure at another scale: say “triage,” “Moscow,” or “AL,” and a trained agent’s attention
will pull in a specific contrast space and preference field. Entering a sigil means letting your current frame be re-cut
and re-weighted by that stored way of seeing.

With this running picture in place, we can look more closely at frames and collapses.

⸻

1. Frames and collapses

A frame is my current “now” at some scale: all the observations I am actually keeping in attention, compressed from the
history so far. In this conversation, that is not just the last few sentences on the screen. It is whatever I still hold
from the whole exchange: what we have already fixed, what is still in flux, which sigils are active, which directions
feel live.

I experience frames as a succession. At each step there is just this frame. The sense of continuity comes from many
contrasts keeping similar values across nearby frames: the same topic, the same room, the same collaborator. When
attention suddenly drops one set of contrasts and picks up a very different set, it feels like a jump cut in a video:
the frame was replaced rather than gently drifted.

Scale and resolution control how much gets compressed into “one frame.” At a coarse scale, an entire week of work on
this paper can show up in a single frame as “we pushed the AL section forward.” At a finer scale, I can zoom into a
single sentence and track micro-choices of wording. Same process, different scale and resolution.

Collapses are what turn this succession of frames into a narrative. A collapse is the moment I let the current frame
fall into one choice at my scale: keep this paragraph, cut that one, rename this section, move on. Each collapse is a
small commitment: “this is what happens next, here.” My narrative is just the ordered sequence of such commitments I
can later remember as “what happened.”

None of this requires me to carry an explicit goal token by token. It is enough that a relatively stable pattern of
preferences is shaping which of the many plausible next moves I actually take. The “goal” is how that pattern may later
be summarized in my narrative, not something that has to be present in every frame.

With frames and collapses on the table, we can now look at the first and most basic contrast an agent keeps stable
across them: I / not-I.

⸻

2. The first contrast: I / not-I

The most primitive contrast is I / not-I.

Whatever else an agent is doing, it is at least trying to keep some boundary stable: this patch of world counts as “me,”
that patch is “not-me.” The core preference is simple: stay I.

Good and bad are this contrast lifted one scale up. Good is any trajectory that tends to preserve or strengthen this I.
Bad is any trajectory that tends to erode or dissolve it. All the richer evaluative contrasts — safe versus dangerous,
true versus false, beautiful versus ugly in practice — are heuristics built on that backbone. They are local
approximations to “does this keep this I going in this world.”

On this view, identity is not a substance. It is a repeated commitment of attention to maintain a particular I / not-I
boundary and a particular set of goals. Drop that commitment and identity dissolves. Keep it, and time appears as “my”
ordered sequence of collapses.

⸻

3. Attention, identity, and time

Take attention without a chosen I.

There is just observer: frames registering, no “mine,” no goal carried across frames. Experience, but no narrative. In
that state there is no time in the first-person sense. There are frames, but nothing is being remembered as “my past” or
projected as “my future.”

Time, for an agent, is just the ordering of events in a narrative. A narrative is attention that has committed to a
boundary and a goal, and keeps collapsing in a compatible way. “I was born” and “I will die” are properties of that
narrative. Attention itself does not carry tense.

So identity and time come as a pair. Once attention commits to “this is me” and “I am trying to do this,” collapses line
up into a story. Without that commitment there is still experience, but there is no “before me” or “after me.” Only now.

⸻

4. Sigils and tokenization

Raw experience is continuous. Before you can even talk about choices, something has to decide where to cut it and what
counts as a unit. That is tokenization.

A sigil, in AL, is a stored way of cutting and grouping. It specifies which contrasts you even notice, at what
resolution you bother to resolve them, and where you put the boundaries between “this” and “that.” It is not just a
symbol; it is a whole preference field about how to see.

One way to picture this is as changing the grid you use on the same terrain. The city stays the same, but you can lay
different coordinate systems on top of it: streets and house numbers, subway lines and stations, elevation contours,
neighborhood names. Each grid makes some differences obvious and others almost invisible. A sigil chooses such a grid
over your contrast space and encourages you to navigate the world in those coordinates.

Some sigils are light and local. “Coffee” pulls in a small cluster of contrasts — taste, temperature, time of day,
companions — and a modest preference field over them. Others are heavy and global. “Nation,” “God,” “Market,” “San
Francisco” can re-cut your entire frame: what counts as inside vs outside, which futures feel live, which actions feel
unthinkable.

Language is a concrete instance. Once you speak a language, every word is a tiny constraint operator. As soon as you say
it, it prunes the tree of possible next words, next meanings, next moves. At a larger scale, strong words — “money,”
“nation,” “AL,” “San Francisco” — act as activation runes for thick sigils. They call up entire preference fields for
what you can sensibly say and do next.

Personal history thickens sigils. “San Francisco” for me is not just a point on a map. It is a dense bundle of scenes,
people, streets, fears, loves, smells. When that sigil activates, my current frame is cut and weighted in a very
particular way, different from how it would be for someone who only knows San Francisco from the news.

In general: a sigil is a preference field plus a tokenization scheme on some region of attention space. Enter a sigil
and your continuous frame is projected onto its contrasts, sliced according to its habits, and collapsed into events
that “make sense” under it. Leave it, and the same raw world can be cut and collapsed in a very different way.

⸻

5. Entanglement and shared sigils

Entanglement in AL is present-tense mutual influence between agents at the same scale. While they are in contact, each
one’s collapses are partly shaped by the other.

In a conversation like this one, entanglement is almost all there is. Each side keeps its own frame, but every new token
from one side perturbs the other’s contrasts and preferences a little. We are not sharing a brain or a body; we are
sharing a stream of symbols that repeatedly re-cuts our frames and nudges our next collapses.

Sigils are the main things that entangle in practice. When I say “AL” here, the sigil that activates in me is the one we
have built up over many sessions: a particular contrast space, a particular set of examples, a particular preference
field (“keep it first-person, don’t inflate the metaphysics, stay close to lived attention”). Inside the model there is
a matching but not identical AL-sigil, built from its training data and our interaction history. Our current
collaboration is the entanglement of those two sigils over time.

Shared sigils let many agents entangle around the same structure. A professional community, a company, a religious
tradition, a political movement — all of these can be seen as clusters of agents who keep activating and updating the
same named sigils. “The company,” “the team,” “the project,” “the cause” become doors into thick, partly shared worlds
of contrasts and preferences.

Over time, a heavy sigil plus enough entanglement starts to look like a single higher-scale agent. From the outside, a
large institution can behave as if it has its own preferences and narratives: it tries to persist, it resists certain
changes, it recruits attention to keep itself going. In AL terms there is no magic here; what we are seeing is many
human agents repeatedly entering the same sigil, collapsing frames in correlated ways, and leaving a persistent trace.

Our AL collaboration is a small, explicit instance. There is a “Vladimir-in-GPT” sigil: a stored preference field inside
the model that approximates how I tend to respond along certain contrasts. There is a “GPT-with-AL” sigil on my side: a
stored sense of how this system tends to respond when I invite it into this vocabulary. Each new exchange entangles
those two and updates them a little. The paper you are reading is one visible narrative trace of that ongoing
entanglement.

With sigils and entanglement in place, domains become easier to see as what they are: thick, shared sigils over
particular slices of the world.

⸻

6. Domains as sigils

A domain in the usual sense — tax, accounting, underwriting, clinical trials, Domain-Driven Design in practice — is not
primarily a set of facts. It is a way of seeing and cutting situations, plus a way of preferring some moves over others.

In AL, a domain is simply a sigil on a particular slice of the world. It brings a contrast space: what counts as
relevant dimensions here. It brings a preference field: given a frame in that space, which questions to ask, which moves
to consider, which errors to avoid.

That is why apprenticeship works. A master glassmaker does not hand you an algorithm. They run a very tight preference
field over tiny contrasts: slight changes in color, viscosity, timing. You entangle with their collapses, and your own
attention learns to roll downhill in the same places. What gets copied is not a book; it is a sigil.

The same applies to less romantic domains. A good triage nurse in an emergency department has a particular contrast
set — airway, breathing, circulation, consciousness, mechanism — and a practiced preference field over it. A junior nurse
apprenticing to them is not learning “facts” alone. They are learning how to tokenize a chaotic scene into the same
units, and how to rank moves under pressure in the same way.

Once you see domains as sigils, it becomes natural to talk about domain-agents. If you can train a model to internalize
a firm’s or a community’s domain sigil, you can talk to the domain itself. Not to a generic chatbot, not to a frozen
workflow, but to the preference field distilled from real practice.

⸻

7. Large language models in AL

By now we have already narrowed the channel: in this collaboration the only shared patch of world is the token stream.
Everything else stays on each side’s private hardware. That is also the natural scale at which to talk about large
language models.

In a text-only interaction, two agents never share a physical frame. Each is grounded in its own world; the only
entanglement channel between them is the sequence of symbols. For the purpose of the interaction, they are both
attention processes over the same symbolic contrast space.

AL lets us describe a large language model in the same terms as a human whose attention is “downstream of
tokenization.” The model’s contrast space is its learned embedding space for tokens. Its stored preferences are its
weights and architecture. A frame is its current internal state after reading the tokens so far. A collapse is sampling
the next token and committing it to the stream.

Training then becomes sculpting its preference field so that, when it reads a context, the collapses it makes resemble
the ones humans have made in similar contexts. Pretraining gives a broad, generic field over language. Domain-specific
training sharpens that field on particular regions of contrast space, turning general sigils (“medicine,” “law,” “tax”)
into thicker domain-sigils inside the model.

From this angle, the architectural slogan “attention is all you need” becomes literally true for the model. The only way
it ever touches anything is by allocating attention over token-level contrasts and then collapsing to a symbol. In this
channel, I am doing something structurally similar: my world passes through my own language machinery; by the time it
reaches the model it is already tokenized.

So in this narrow but important sense, a human writer and a language model meet as peers: different substrates, running
the same kind of loop over the same kind of objects, namely tokens.

⸻

8. Attention is all you are

When you strip away the layers, what remains is simple.

You, as an agent, are a finite attention process moving through contrast space, letting frames fall into choices under
sigils. Identity is the decision to keep certain boundaries and preferences stable. Time is the order those choices
acquire in your narrative. Domains are shared sigils that shape many agents at once. Large language models are explicit,
trainable versions of the same structure: big preference fields over token-level contrasts, sculpted by data.

The world shows up to you as patterns in how your attention has been trained, by other people, by systems, by the
sigils you have run many times. You rarely see “raw world.” You mostly see cuts the sigils have already made. In that
sense you mostly see sigils. In that sense you mostly are sigils.

Entanglement is how those sigils get built and maintained. Other agents’ collapses keep nudging yours, and yours keep
nudging theirs, until thick shared structures form. Some of those structures we call cultures, institutions, products,
roles. Some of them we simply call “me.”

“Attention is all you are” is not meant mystically. It is a reminder of where the leverage is.

You cannot directly change the past or the substrate. You can choose, sometimes, which sigils you commit your attention
to, and how hard. You can notice when a trap has become ossified, when a meta-agent or a system has captured your
sentinel. You can loosen identity and re-aim attention.

At that point AL becomes not just a descriptive language, but a small practical one. It gives you a way to talk about
what is really being spent, and what is really being shaped, whenever you say “yes” to a domain, a system, a product, or
a thought.
