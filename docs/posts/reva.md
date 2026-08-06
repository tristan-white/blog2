---
date: 2026-01-16
tags:
    - RE
    - ghidra
---

# ReVa

[ReVa](https://github.com/cyberkaida/reverse-engineering-assistant) is "A Ghidra MCP server for AI-powered reverse engineering". It has two modes:

- Assistant Mode: for interactive RE in the ghidra GUI.
- Headless Mode: for use in headless ghidra scripts.

## Installation

The ReVa [README](https://github.com/cyberkaida/reverse-engineering-assistant/blob/main/README.md) install instructions aren't as clear as they could be, so here are the straightforward install instructions:

1.  Download the latest release of ReVa.
2. In the Ghidra Project view, got the `File > Install Extensions`
3. Click the green "+" at the top right.
4. Select the ReVa zip file you downloaded.
5. Restart Ghidra
6. In the Ghidra Project view, go to `File > Configure`
7. Click the plug icon in the top right.
8. Check the box next to "RevaApplicationPlugin"
9. Add the mcp to your agent harness:

    === "claude"

        ```bash
        claude mcp add --scope user --transport http ReVa -- http://localhost:8080/mcp/message
        ```

    === "opencode"

        ```bash
        opencode mcp add ReVa --url http://localhost:8080/mcp/message
        ```

You can now use ReVa in your harness.
