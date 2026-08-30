# Example: Knowledge Checker Mode

**Context:** I just read the docs on how React's `useEffect` cleanup function works and want to verify I actually understood it before moving on.

**Precondition check:** Have I attempted an explanation myself first? Yes — I wrote one out below before asking.

**Me:** "I just read about `useEffect` cleanup functions. My understanding: the function you return from inside `useEffect` runs right before the effect runs again on the next re-render, and also runs once when the component unmounts. It's mainly for cleaning up subscriptions, timers, or event listeners so they don't pile up. Can you check my understanding?"

**Claude:** "Take this scenario: a component has `useEffect(() => { const id = setInterval(tick, 1000); return () => clearInterval(id); }, [count])` where `count` is state that changes on every tick. Walk through what happens across three consecutive re-renders as `count` updates — when exactly does the cleanup run relative to the effect re-running, and does the interval ever end up leaking or duplicating?"

**Me:** "So... on each render where `count` changed, React runs the cleanup from the previous effect first — clearing the old interval — then runs the new effect, setting up a fresh interval. So it should stay at one interval at a time, no leak. But wait, is the cleanup from render N running before render N+1's effect, or is there some batching where multiple renders' effects queue up?"

**Claude:** "You've got the core order right — cleanup-then-effect, paired per dependency change, not batched across multiple changes. Since you're now asking about batching specifically: what does your model predict if `count` changes twice in the same synchronous event handler, before React re-renders at all?"

**Me:** "If it's genuinely synchronous state updates batched into one render, then the effect only sees the final `count` value — no cleanup/effect pair runs for the intermediate value at all, since there's no render for it."

**Outcome:** My original explanation held up on the core mechanism (cleanup runs before the next effect and on unmount). The scenario surfaced a real gap I hadn't considered — batching — and I reasoned it through myself rather than being told the answer. Confirmed correct after the fact, not before.
