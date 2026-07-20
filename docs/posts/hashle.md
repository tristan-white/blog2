---
title: Vibe Coding, Copilot, and Hash Length Extension Attacks
# description: Quick tips for the world's most popular password cracker.
image: https://2.bp.blogspot.com/-ErHto8FzL1g/WSLXlgmZTWI/AAAAAAAAJ0s/ELyhSq8SDsgArJ8xIFyKZH031iQFcgO7wCLcB/s1600/Hashcat.jpg
tags:
    - hacking
date: 2026-07-20
---

Everyone's talking about [fable](https://www.anthropic.com/claude/fable) so I decided the bite the bullet and get a subscription to try it out.

But before trying out fable, I wanted to see how much [Copilot](https://github.com/features/copilot/cli/) could accomplish. 

I recently spent most of a week learning more about cryptographic vulnerabilities in computers, so I decided to test out copilot by building a python library and CLI tool to perform [hash length extension attacks](https://en.wikipedia.org/wiki/Length_extension_attack). There's already a couple projects[^1] on github that perform this attack, but they all were either no longer maintained, messy, or didn't support all the hashes succeptible to this attack[^2].

After $3 of credits and an hour of prompting and coddling copilot, it pumped out [hashle](https://github.com/tristan-white/hashle):

```console exec="true" source="console" result="ansi"
$ hashle --help
```

```console exec="true" source="console"
$ hashle list-algorithms
```

```console exec="true" source="console"
$ hashle extend --help
```

!!! tip
    Also today I learned about [markdown-exec](https://pawamoy.github.io/markdown-exec/), my new favorite project that lets you use shell or python code to render docs, which is how the `hashle` output above is displayed.

For $10/month, copilot's not bad.

[^1]: See [hash_extender](https://github.com/iagox86/hash_extender) and [hlextend](https://github.com/stephenbradshaw/hlextend).
[^2]: That is, hashes that use Merkle-Damgard hash constructions.

