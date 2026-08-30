# Example: Rubber Duck Mode

**Context:** I'm building a small job queue for a side project. Workers occasionally process the same job twice under load.

**Precondition check:** Do I have a hypothesis? Yes — I think two workers are polling the same "pending" row before either marks it as claimed, so both grab it.

**Me:** "I'm debugging duplicate job processing in my queue. My hypothesis: there's a race between the SELECT that finds a pending job and the UPDATE that marks it claimed — two workers can both SELECT the same row before either UPDATEs it. Can you rubber-duck this with me?"

**Claude:** "So the shape is: worker A reads row 7 as pending, worker B reads row 7 as pending (before A's UPDATE lands), both proceed to process it. If that's right — what would you expect to see if this is the actual cause versus something else? Does the duplication rate track with the number of concurrent workers, or does it happen even with a single worker?"

**Me:** "Good question — I hadn't checked that. Let me look... it happens even with one worker sometimes, just less often."

**Claude:** "That's worth sitting with — a single worker duplicating rules out a cross-worker race on the SELECT/UPDATE gap, since there's no second reader in that window. What else touches 'pending' status for a job? Anything retry-related, a timeout requeue, a separate process?"

**Me:** "...I do have a stale-job requeue sweep that resets anything 'claimed' for more than 30s back to 'pending', in case a worker crashed. If a job just takes a bit over 30s, the sweep would requeue it while the original worker is still finishing."

**Outcome:** I found the actual bug myself — it wasn't the race I originally guessed, it was the requeue sweep's timeout being too aggressive relative to real processing time. Claude never told me this; the falsification question (does it happen with one worker?) is what pointed me at a mechanism other than the one I started with. Fix: extend the sweep timeout and have workers heartbeat instead of using a fixed window.
