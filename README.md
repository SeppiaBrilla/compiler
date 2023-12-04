# Compiler Project

Welcome to the Compiler project, dedicated to enhancing the compiler experience through the integration of Language Model (LLM) capabilities. This project allows for the extension of LLM functionalities using plugins that facilitate seamless communication between themselves and the LLM.

## Architecture Overview

The architectural design is illustrated in the accompanying image:
![diagram](https://drive.google.com/uc?export=view&id=1v-S9mdO_Sf5ovS3mEcz5FHzuYOslh4d6)

## Execution Process

The execution process unfolds as follows:

1. **Frontend Interaction:**
   - The frontend initiates communication by querying the backend APIs.
   - The backend, in turn, channels the request through the service manager to the Language Model (LLM).

2. **LLM Response Handling:**
   - The LLM response is parsed to extract relevant information.

3. **Plugin Activation:**
   - The Plugin Manager orchestrates the activation of necessary plugins based on the parsed LLM response.

4. **Plugin Operations:**
   - Plugins, once activated, can interact with the backend APIs to retrieve or store data. Additionally, they have the capability to query the LLM.

5. **Finalization:**
   - Following the execution of each plugin, the responses from both the LLM and the plugins are collected.

6. **Frontend Feedback:**
   - The aggregated responses are then seamlessly passed back to the frontend for further processing and presentation to the user.

The collaboration between frontend and backend applications is facilitated through HTTP, connecting the backend with both plugins and the user interface. Notably, the plugins maintain indirect communication by interfacing exclusively with the backend. This approach ensures a well-organized and modularized structure for effective functioning.
