# Degrees of Lewdity: player-facing systems handover

This is a source-grounded orientation to what the game feels like from the human player’s side, what the major systems expect the player to do, and how those systems fit together underneath.

It is not a passage-by-passage walkthrough. It is the conceptual model a fresh agent needs before touching the consensual combat, haggle, or NPC desire systems.

---

## 1. What the player is doing

At the highest level, the player is managing a vulnerable young character through a hostile, sexualised town and surrounding wilderness.

The player repeatedly:

```text
choose a destination or activity
    ↓
spend time and resources
    ↓
encounter people, places, jobs, or threats
    ↓
make choices inside the event
    ↓
gain money, skills, relationships, trauma, corruption, clothing, pregnancy, fame, or other state
    ↓
manage the resulting condition and continue
```

The game is not built around one clean victory condition. It is closer to a survival/sandbox life simulator with:

- exploration
- school and work
- money management
- clothing and appearance
- social relationships
- sexual encounters
- combat and escape
- body transformation
- pregnancy
- corruption and psychological change
- exhibitionism and public reputation
- named-character storylines
- recurring random events

The player is expected to create a personal story rather than follow one universal optimal route.

The game’s underlying tone, however, is heavily biased toward danger, loss of control, sexual coercion, and recovery from bad events. Many systems are designed around the assumption that the player will be exposed, overpowered, embarrassed, exploited, traumatised, or forced to manage consequences.

That is the part this project is trying to rebalance: not removing the game’s danger, but giving consensual decisions enough mechanical weight and variety that they are a genuine alternative playstyle.

---

## 2. Erotic intent and direction for mods

Degrees of Lewdity is fundamentally an erotic game. Its dominant fantasy is not generic sexual freedom. It is erotic vulnerability, particularly being on the receiving end of molestation, coercion, rape, exposure, restraint, involuntary arousal, humiliation, corruption, and loss of control.

The life-simulation systems give that fantasy persistence and context. Clothing, travel, work, school, money, weather, reputation, relationships, body state, trauma, and transformation make sexual danger happen to a continuing character whose circumstances and history matter. These systems are substantial, but they should not obscure the game’s erotic centre.

This creates an important distinction between character agency and player agency:

- The character is often vulnerable, constrained, overpowered, or unable to determine what happens.
- The player should still be able to make choices that causally shape the form, direction, meaning, and consequences of what happens.
- The player controls engagement with the fantasy, even when the fantasy concerns the character losing control.

Increasing player agency does not inherently compromise the game. It compromises the game when new mechanics provide universal safety, guaranteed compliance, frictionless outcome selection, or reliable control over other characters. Those outcomes remove the uncertainty and opposing pressure that give the game its identity.

The preferred uplift is **responsive uncertainty**. Player actions should provide leverage rather than sovereignty. An attempt may succeed, fail, partially succeed, provoke resistance, reveal information, invite a counterproposal, worsen the situation, or produce an interpretation the player did not expect. Clean success must remain possible, or agency becomes a false choice that the game merely punishes.

Uncertainty should remain legible rather than arbitrary. The player should be able to observe behaviour, form a theory, act on it, and understand the result in retrospect. The desired reaction is usually “I misread them” or “I took a risk and it changed the encounter,” not “the game ignored my choice” or “a hidden roll selected a random outcome.”

When discussing a mod with the user, treat the following as the default design direction:

- preserve the character’s vulnerability while increasing the player’s authorship;
- make choices causally meaningful without making outcomes obedient;
- give NPCs, situations, and existing systems enough independent pressure to resist or reinterpret player intent;
- prefer dynamic reactions, trade-offs, partial success, counterplay, and consequences over guaranteed selection;
- preserve meaningful differences between hostile, consensual, transactional, and ambiguous encounters;
- do not assume that conventional empowerment, greater safety, universal consent, or removal of erotic danger is the intended improvement;
- do not assume that every exercise of agency must backfire or carry a negative consequence;
- evaluate proposed mechanics by the fantasy and player behaviour they produce, not by the number of new options they add.

The directional goal is:

> Preserve the protagonist’s vulnerability while giving the player richer authorship over how encounters develop.

This is a design nudge, not a requirement that every feature become an agency system. Mods should remain compatible with the game’s sandbox structure, named storylines, hostile content, and native restrictions unless the user explicitly chooses a different direction.

---

## 3. The world loop

The overworld is organised around locations, time, weather, schedules, and event availability.

The player normally interacts with:

- a location/map system
- time and date
- weather and temperature
- location-specific activities
- shops and services
- school/work routines
- random ambient events
- story events and named NPC encounters
- movement restrictions and route hazards

Moving, working, studying, sleeping, eating, shopping, and participating in events all consume or advance time.

The world is therefore not just a menu of scenes. The player is constantly balancing:

- where they are
- what time it is
- how much money they have
- their physical condition
- their stress and trauma
- exposure and clothing
- whether they have enough energy, food, warmth, or supplies
- which NPCs or events are currently available

Weather, clothing, body temperature, exhaustion, hunger, and other environmental factors can turn ordinary travel into a resource-management problem.

The player generally does not receive a clean “quest objective” for every meaningful action. They learn the game by reading descriptions, observing state changes, checking the map, and remembering what places and characters do.

---

## 4. The player character

The player character is represented by a large persistent state object, `$player`, plus many global variables.

The character has several overlapping identities:

```text
physical body
social presentation
psychological condition
sexual history
relationships and reputation
mechanical progression
```

The player can customise or alter:

- sex and gender presentation
- pronouns
- body shape
- breast, penis, and bottom size
- clothing and exposure
- hair, skin, and appearance
- chastity and virginity
- body transformations
- traits and background
- attitudes toward sex, control, submission, and exhibitionism

The player is not only choosing actions. They are also shaping what kind of person the character becomes.

---

## 5. Core resources and conditions

The game has many persistent and semi-persistent resources. The exact balance varies by game mode and event, but the player is broadly managing:

### Money

Money pays for:

- food
- clothing
- medicine
- transport or services
- sex work and brothel-related activity
- supplies
- certain story outcomes

The player can earn money through work, business, prostitution, events, rewards, and exploitation of various opportunities.

Money is one of the clearest areas where the player can pursue a more controlled, transactional playstyle. The current haggle system is an early attempt at this.

### Health

Health represents physical survivability. It is affected by:

- attacks
- injuries
- combat
- environmental danger
- some sexual outcomes
- illness and other events

Health reaching zero generally ends or resolves combat in the opponent’s favour.

### Arousal

Arousal drives sexual escalation.

In combat, NPC arousal is tracked separately and usually determines whether they are stimulated, nearing orgasm, ejaculating, or losing interest.

The player’s own arousal affects actions, orgasm, control, and some psychological consequences.

Arousal is often treated as a tactical resource: increasing it can make sexual situations more rewarding or more dangerous, depending on who controls the encounter.

### Anger

NPC anger is one of the main behavioural variables in native combat.

It affects:

- willingness to cooperate
- likelihood of hostile actions
- combat escalation
- reactions to the player’s speech and behaviour
- some acceptance checks

The current haggle implementation uses anger crudely: below a threshold means acceptance, above it means refusal. This is one of the major areas the overhaul should improve.

### Trust

Trust is another broad NPC reaction variable.

It affects:

- how receptive the NPC is
- whether requests succeed
- social and sexual interactions
- whether the NPC becomes guarded or confident
- the chances of player-led transitions

The combat UI communicates trust using descriptive text such as cautious, wary, relaxed, suspicious, or confident.

### Stress

Stress represents short-to-medium-term psychological pressure.

It can rise through:

- public exposure
- sexual danger
- humiliation
- failure
- threats
- violence
- unwanted events

The player manages stress through rest, pleasure, drugs, comfort, activities, and certain story choices.

### Trauma

Trauma is a deeper psychological resource.

It is connected to:

- violent sexual experiences
- loss of control
- abuse
- frightening events
- dissociation
- some transformations and story effects

Trauma can affect the player’s behaviour and available responses. The game sometimes allows the player to cope, resist, embrace, or become desensitised to certain experiences.

### Control

Control represents how much agency the player feels they retain over the character’s behaviour and identity.

It is affected by:

- sexual acts
- prostitution
- submission
- exhibitionism
- trauma
- attitudes
- story events
- certain psychological effects

The game often treats “loss of control” as both a mechanical danger and a thematic progression.

---

## 6. Skills and progression

The player has skills that influence the likelihood and quality of actions.

Common categories include:

- seduction
- English/language
- athletics
- security
- various sexual skills
- combat-related abilities
- school and work skills

Many checks use a native formula based on some combination of:

```text
skill
+ arousal
+ trust
+ random factor
- difficulty
- anger or opposition
```

The player is expected to improve skills over time through school, work, repetition, and story events.

Progression is not just “level up and become stronger.” It often means:

- unlocking more actions
- becoming better at avoiding danger
- gaining access to new jobs or locations
- tolerating more exposure
- becoming more sexually capable
- changing which choices feel psychologically available
- building relationships
- becoming more able to survive bad events

---

## 7. Clothing and exposure

Clothing is one of the game’s most important cross-system mechanics.

The clothing system controls:

- what body parts are visible
- what actions are possible
- how much protection the player has
- public modesty
- weather protection
- social reactions
- sexual availability
- whether NPCs can target certain body parts
- whether the player is recognised or judged

Clothing is layered across many slots:

- face
- head
- neck
- upper body
- lower body
- underwear
- over-clothing
- genitals
- hands
- feet
- accessories and handheld objects

The player can deliberately dress for:

- modesty
- warmth
- work
- fashion
- seduction
- exposure
- combat
- sexual accessibility
- public humiliation

Exposure is not a single boolean. Individual body parts have separate exposure states, and combat actions inspect those states before generating available options.

This is why clothing edits can have effects far beyond appearance. A clothing change may alter:

- map movement
- weather survival
- NPC reactions
- combat actions
- social events
- public reputation
- pregnancy or sexual availability
- whether a player-led request is physically possible

---

## 8. Sexual history and behaviour systems

The game tracks sexual history through several progression systems.

### Virginity

Different virginity states are tracked independently, including:

- oral
- vaginal
- penile
- anal
- kissing
- handholding
- some specialised forms

Virginity affects descriptions, character reactions, consequences, and sometimes event availability.

### Promiscuity

Promiscuity measures the player’s increasing willingness or experience with ordinary sexual activity.

It often gates consensual combat actions. Some actions require a certain promiscuity threshold before the game allows the player to request or initiate them.

The system is meant to represent growing sexual confidence and willingness, but mechanically it often functions as an unlock ladder.

### Deviancy

Deviancy gates more unusual, extreme, or socially taboo activities.

It may determine whether the player can access actions involving:

- unusual body parts
- stronger sexual behaviour
- more extreme encounters
- certain non-human or unconventional acts

### Exhibitionism

Exhibitionism tracks comfort with being seen, exposed, or sexually displayed.

It can unlock:

- public exposure
- nude behaviour
- exhibitionist events
- public sexual opportunities
- reduced discomfort with nudity

It also interacts with clothing and public reactions.

### Fame and reputation

The player can gain different kinds of fame, including:

- sexual fame
- prostitution fame
- exhibitionism fame
- business fame
- performance fame
- social fame
- rape-related fame
- other activity-specific reputation

Fame affects how the world recognises or categorises the player.

This is important for the planned consensual overhaul: a player who becomes known as someone who sells sexual services, dominates willing partners, performs publicly, or negotiates aggressively should ideally develop a different social trajectory from a player who is mostly victimised.

---

## 9. Attitudes and player agency

The player can configure certain attitudes that shape how the game interprets consensual activity.

The current attitude system includes choices such as:

- enjoying making people feel good
- enjoying being in control
- treating sex as naughty or fun
- speaking neutrally, meekly, or brattily
- changing comfort with underwear exposure
- changing comfort with nudity
- changing comfort with prostitution
- changing how the player psychologically processes lewd actions

The important idea is that the player’s chosen attitude can modify consequences after consensual sex.

For example, assertive behaviour may increase defiance, while submissive behaviour may increase submissiveness. Some attitudes also change how the player gains or loses stress and trauma.

This is a useful foundation for the planned system because the player already has an identity and preferred interaction style. The NPC desire system should eventually be able to respond to that style rather than treating every consensual action as an isolated skill check.

---

## 10. Named NPCs

Named NPCs are the game’s persistent relationship characters.

They have:

- persistent identity
- names and descriptions
- individual storylines
- relationship values
- love, lust, trust, rage, purity, corruption, or similar state
- special dialogue
- special reactions
- unique events
- custom sexual scenes
- personal progression and route changes

Named NPC data exists separately from ordinary generated NPC data.

The player’s relationship with a named NPC can evolve through:

- conversation
- gifts
- sex
- shared events
- betrayal
- violence
- submission or dominance
- corruption
- story-specific choices
- repeated encounters

Named NPCs can therefore support continuity. A player can intentionally build a relationship, manipulate someone, become dependent on someone, or create a long-term conflict.

For the haggle/desire overhaul, named NPCs should probably use their persistent state as a source of bias, not as a complete replacement for temporary encounter behaviour.

---

## 11. Unnamed NPCs

Unnamed NPCs are generated into `$NPCList` slots when a passage needs them.

They are generally:

- physically generated for the event
- given random names and descriptions
- assigned anatomy and clothing
- given a role or generic description
- used in the event or combat
- cleared or replaced afterward

They normally do not have a persistent identity or long-term relationship.

There are exceptions:

- some generic NPCs are deliberately saved under `per_npc`
- some “persistent archetypes” can be loaded again
- some event NPCs are copied for use later
- some NPC values technically remain in `$NPCList` until the slot is reused

The right player-facing interpretation is still:

> Most strangers are one-encounter characters whose personality is created by the current situation.

That is a strength for the proposed system. A temporary, encounter-specific social profile is more appropriate than trying to invent a full biography for every stranger.

---

## 12. Combat from the player’s perspective

Combat is the most important reusable interaction system in the game.

It is not a conventional attack/defend combat loop. It is a body-part-based sexual and physical interaction engine.

The player usually sees action groups for:

- left hand
- right hand
- feet
- mouth
- penis
- vagina
- anus
- chest
- thighs
- speech

Actions are generated dynamically based on:

- the player’s anatomy
- the NPC’s anatomy
- clothing and exposure
- current body-part occupancy
- positions
- restraints
- available targets
- promiscuity and deviancy
- consensual versus non-consensual state
- NPC state
- player skills
- story-specific restrictions

Relevant generation code:

- [actionsGeneration.twee](<H:\Other\Degrees of Lewdity\game\base-combat\actionsGeneration.twee:1>)
- [actions-speech.twee](<H:\Other\Degrees of Lewdity\game\base-combat\actions-speech.twee:1>)
- [actions-hands.twee](<H:\Other\Degrees of Lewdity\game\base-combat\actions-hands.twee:1>)
- [actions-mouth.twee](<H:\Other\Degrees of Lewdity\game\base-combat\actions-mouth.twee:65>)
- [actions-penis.twee](<H:\Other\Degrees of Lewdity\game\base-combat\actions-penis.twee:1>)
- [actions-vagina.twee](<H:\Other\Degrees of Lewdity\game\base-combat\actions-vagina.twee:1>)
- [actions-anus.twee](<H:\Other\Degrees of Lewdity\game\base-combat\actions-anus.twee:1>)

The player’s actual task is:

```text
inspect the current physical state
    ↓
identify available actions
    ↓
choose what to do with each body part
    ↓
submit the turn
    ↓
read the NPC’s response and state changes
    ↓
adapt
```

The action menu is therefore a live representation of what the player can currently do.

The menu changes when:

- a body part becomes occupied
- clothing is removed
- a body part is restrained
- the player changes position
- the NPC changes position
- an NPC begins or releases an interaction
- the player reaches orgasm
- a condom or sex toy appears
- a new target becomes available
- the player’s social or sexual stats change

---

## 13. Native consensual combat

Consensual combat is not a completely separate engine from assaultive combat. It uses much of the same physical state infrastructure, but changes:

- available actions
- default action sets
- dialogue
- resistance rules
- social checks
- player control
- NPC behaviour
- consequences

The combat menu selects a defaults category:

```text
consensual
or
rape
```

For named characters, default actions can be specific to that character. For ordinary strangers, defaults fall back to generic categories such as “Strangers.”

This is one of the places where the current game’s architecture becomes visible: consensual and non-consensual play are different behavioural modes layered over the same body-part state machine.

The current consensual system expects the player to:

- select sexual actions manually
- build arousal
- manage NPC trust and anger
- use speech to alter the encounter
- request or initiate transitions
- meet promiscuity/deviancy requirements
- respond to NPC actions
- escape or end the encounter when needed

However, much of the NPC response logic was designed around generic cooperation or resistance rather than rich negotiation. The player has action control, but not always meaningful social control.

That is the gap the desire/haggle work is addressing.

---

## 14. NPC combat behaviour

NPCs choose actions based on their current state, type, available body parts, combat position, and encounter mode.

NPCs may:

- expose the player
- undress the player
- kiss
- use hands
- use mouth
- penetrate
- grope
- restrain
- remove clothing
- use sex toys
- attempt orgasm
- submit
- switch positions
- react to the player’s actions
- attack or escalate

Native NPC behaviour is often organised around body-part state transitions:

```text
NPC penis state
NPC vagina state
NPC mouth state
NPC hand state
NPC position
NPC target
```

An action usually:

1. checks whether the interaction is available;
2. changes a state variable;
3. prints descriptive text;
4. applies arousal, pleasure, pain, trauma, trust, anger, or other effects;
5. leaves the body-part state ready for future actions.

This makes the combat system robust and reusable, but it also means any new social system must eventually translate back into these existing state transitions.

The desire system currently does this by suggesting an intended interaction while allowing native combat to execute it.

---

## 15. The player’s visible feedback

The game communicates state through:

- prose
- colour-coded text
- status descriptions
- action availability
- sidebar effects
- combat animations
- image or canvas rendering
- explicit difficulty labels
- body-part state changes
- NPC facial/emotional descriptions

Combat state is described in broad bands.

For example, NPC arousal is shown as:

```text
unstimulated
stimulated
aroused
horny
lustful
approaching orgasm
orgasm imminent
```

Anger is shown as:

```text
calm
tense
irritated
frustrated
angry
furious
incredibly pissed off
```

Trust is shown as:

```text
suspicious
guarded
wary
cautious
alert
relaxed
confident
```

This feedback is important because the player is expected to infer what is happening from reactions rather than seeing every numeric value.

The planned haggle system should follow this design. It should expose enough emotional information for the player to make informed experiments without revealing the entire hidden profile.

---

## 16. Player-led agency actions

The current workspace contains a newer player-agency layer in `ingame.js`.

It defines explicit relations such as:

- NPC penis to player mouth
- NPC penis to player vagina
- NPC penis to player anus
- NPC vagina to player mouth
- NPC mouth to player vagina
- NPC mouth to player penis
- NPC mouth to player anus
- NPC hand to player vagina
- NPC hand to player penis
- NPC hand to player anus
- asking the NPC to release control

These actions are checked for:

- consensual combat
- NPC type
- anatomy
- body-part availability
- clothing and exposure
- position
- promiscuity
- current state
- NPC desire
- trust
- arousal
- anger
- seduction skill

The desire score is already used in `combatAgencySuccessChance()` to influence whether an NPC accepts a player request.

This layer is more explicit than the native controls: instead of merely selecting an action for the player character, the player can ask the NPC to change what the NPC is doing.

That makes it an obvious bridge for haggle.

---

## 17. The existing extended desire system

The current desire model is encounter-local and dynamically generated.

At combat start:

```text
NPC anatomy
+ available player targets
+ native combat state
→ candidate interaction list
```

Candidates begin with mostly uniform scores. During combat:

```text
player/NPC interaction
    ↓
arousal and pleasure result
    ↓
satisfaction band
    ↓
candidate score changes
    ↓
next preferred intent changes
```

The system also uses weighted intent switching. Even if another desire becomes stronger, the NPC does not always switch immediately. Their previous action, satisfaction band, and cooldown influence whether they change direction.

This is a useful emergent foundation because it creates behavioural inertia:

- an NPC may continue enjoying an action
- an NPC may become dissatisfied and seek something else
- a very strong new desire may override the current activity
- a poor interaction may reduce that candidate’s future priority
- an accepted player transition may create a short-term preference cooldown

The system is not yet a full personality model. It is closer to:

> an encounter-specific satisfaction and intent simulator layered over native combat.

That is probably the correct scope for this project.

---

## 18. Haggle from the player’s perspective

The current haggle feature is accessed through speech in a consensual single-NPC encounter.

The player selects “Sell yourself,” passes a qualification check, and enters the haggle interface.

The current UI lets the player choose:

- what sexual service to offer
- how much money to request

Existing offers include:

- oral
- oral virginity
- penile sex
- penile virginity
- vaginal sex
- vaginal virginity
- anal sex
- anal virginity

The current version behaves like a transaction form:

```text
choose act
choose amount
submit proposal
NPC accepts or declines
```

The intended overhaul is much more interesting:

```text
choose act or role
choose framing
choose compensation
submit a social proposition
NPC interprets it through temporary state
NPC accepts, refuses, counters, becomes offended, or escalates
```

The player should be able to use haggle to:

- earn money on their own terms
- test what an NPC wants
- control the direction of sex
- offer dominance
- offer submission
- offer unusual or non-standard acts
- exploit an NPC’s attraction
- discover hidden preferences
- make a socially risky proposition
- create a unique story outcome

Haggle should not guarantee that money can buy anything.

---

## 19. What the game currently expects the player to optimise

The native game often expects the player to optimise survival and damage control.

The practical player mindset is usually:

```text
avoid dangerous situations
keep health and stress manageable
maintain enough money and supplies
improve relevant skills
use clothing and exposure intelligently
understand which actions are safe
escape before the situation becomes unrecoverable
```

In sexual combat, the player often optimises:

- arousal without losing control
- pleasure against trauma
- submission versus defiance
- exposure against social consequences
- available body parts
- NPC anger and trust
- escape opportunities
- virginity and pregnancy risks
- whether to cooperate or resist
- whether an action unlocks future options

The player is expected to learn the rules through repetition and failure.

That produces a lot of depth, but it also creates the central problem behind this overhaul: a player can become very skilled at navigating a system without feeling that they are authoring the encounter.

---

## 20. Why the current game can feel low-agency

The game has many choices, but choice count is not the same as agency.

The current experience can feel low-agency because:

- many encounters begin with the NPC already controlling the situation
- native NPC behaviour often advances through predetermined physical states
- social checks are broad and opaque
- the same action can have radically different consequences without enough explanation
- the player’s sexual choices often modify how they endure an event rather than whether the event happens
- consent and non-consent share much of the same underlying action infrastructure
- NPC motivations are usually implied through prose rather than modelled explicitly
- generic NPCs have little continuity
- haggle currently reduces a complicated social proposition to anger plus price
- the game rewards surviving or adapting to coercion more consistently than deliberately shaping consensual interactions

The desire/haggle project is not merely adding more options. It is trying to make the player’s choices causally meaningful.

The desired feeling is:

> “I made a proposition, the NPC understood it in their own way, and the encounter became something because of that choice.”

---

## 21. How persistent state works

SugarCube stores most `$variables` in story state, which means they are saveable unless deliberately cleared.

There are several persistence levels:

### Persistent global/player state

Examples:

- money
- skills
- clothing
- stress
- trauma
- fame
- corruption
- promiscuity
- exhibitionism
- named NPC relationships
- pregnancy
- transformations

### Encounter state

Examples:

- `$enemyarousal`
- `$enemyanger`
- `$enemytrust`
- `$NPCList`
- combat body-part states
- `$consensualNpcDynamics`
- current combat targets
- current action state

These are meant to last through the encounter and be cleared at combat/event end.

### Temporary rendering/local state

Examples:

- `_target`
- `_sound`
- `_n`
- `_mouthFree`
- temporary action dictionaries
- local text variables

These exist only during passage rendering or widget execution.

The system’s cleanup is explicit. `endcombat`, `endevent`, and related widgets reset large portions of combat and event state.

Relevant file:

- [end.twee](<H:\Other\Degrees of Lewdity\game\base-combat\end.twee:1>)

The desire/haggle overhaul should respect this lifecycle. Encounter personalities should live in encounter state, not leak into permanent NPC or player data unless a deliberate consequence is chosen.

---

## 22. Code architecture from the player’s point of view

The game is a SugarCube/Twee project.

The player experiences a continuous story, but underneath it is divided into:

```text
passages
    ↓
widgets
    ↓
JavaScript helpers and state
    ↓
global story variables
    ↓
native combat and rendering systems
```

Passages are responsible for:

- scenes
- dialogue
- choices
- event progression
- location transitions

Widgets are responsible for:

- reusable actions
- combat effects
- NPC generation
- clothing operations
- stat changes
- event cleanup
- text generation

JavaScript modules are responsible for:

- calculations
- state management
- NPC agency
- dynamic action generation
- rendering
- save handling
- weather
- clothing
- UI behaviour
- larger subsystems

The important engineering reality is that many systems share broad global variables. A seemingly local change can affect:

- combat generation
- action availability
- passage transitions
- save/load
- NPC cleanup
- text macros
- named-character events
- rendering

That is why the haggle/desire work should remain an adapter layer rather than rewriting native combat assumptions.

---

## 23. What a fresh agent must not assume

A new agent should not assume:

- every NPC has a persistent personality
- `$NPCList` means persistent NPC identity
- desire scores are innate preferences
- anger is the same as refusal
- arousal is the same as consent
- a successful skill check means the NPC wants the action
- the action menu is static
- consent and assault use separate combat engines
- all NPCs are generated in the same way
- every temporary variable is actually unsaved
- the player’s available options are independent of clothing and body state
- a UI change is safe if the underlying state model is unchanged
- the haggle UI is the main problem
- named NPC logic can be applied directly to generic strangers

The core distinction is:

```text
native systems tell the game what is physically possible
desire tells the game what this encounter currently gravitates toward
haggle should tell the game what the player is proposing socially
```

Those layers should interact, but they should not become indistinguishable.

---

## 24. The intended future model

The target experience is a consensual encounter that behaves more like a volatile social simulation:

```text
NPC generated
    ↓
temporary encounter profile created
    ↓
player observes, teases, talks, touches, negotiates, or offers
    ↓
NPC interprets those actions
    ↓
desire, trust, anger, arousal, and control shift
    ↓
NPC accepts, refuses, counters, submits, dominates, disengages, or escalates
    ↓
native combat executes the resulting physical interaction
    ↓
the encounter feeds back into the temporary profile
```

The temporary profile should not be a full biography.

It should be enough to answer:

- What does this NPC seem interested in right now?
- What do they find presumptuous or offensive?
- How open are they to being propositioned?
- Do they prefer control, submission, or switching?
- Does money matter to them?
- What kind of offer would they counter with?
- How much trust or arousal is needed before they accept?
- What actions have improved or worsened the encounter?

That is enough to make a generated stranger feel like a person for the duration of the encounter without pretending the game has a persistent social database underneath it.

---

## 25. One-sentence summary

Degrees of Lewdity is an erotic life-and-survival sandbox centred on persistent vulnerability and sexual loss of control, where the character is often overpowered but the player should retain meaningful authorship over how encounters develop; its combat engine is a shared body-part state machine, its NPCs are usually temporary generated objects, and mods should favour legible, responsive uncertainty over either arbitrary powerlessness or guaranteed player-selected outcomes.
