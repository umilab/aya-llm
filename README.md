# Aya-LLM - Large Language Models made easy 🦙

![License](https://img.shields.io/github/license/umilab/aya-llm)
[![Discord](https://img.shields.io/discord/1088427963801948201?label=Discord)](https://discord.gg/nhB8hv3Rf5)

A chat interface based on [llama.cpp](https://github.com/ggerganov/llama.cpp) for running Alpaca models. Entirely self-hosted, no API keys needed. Fits on 4GB of RAM and runs on the CPU.

- **SvelteKit** frontend
- **Redis** for storing chat history & parameters
- **FastAPI + langchain** for the API, wrapping calls to [llama.cpp](https://github.com/ggerganov/llama.cpp) using the [python bindings](https://github.com/abetlen/llama-cpp-python)

## Getting started

Setting up Aya-LLM is very easy. Starting it up can be done in a single command:

```
docker run -d -v weights:/usr/src/app/weights -v datadb:/data/db/ -p 8008:8008 ghcr.io/umilab/aya-llm:latest
```

Then just go to http://localhost:8008/ and you're good to go!

The API documentation can be found at http://localhost:8008/api/docs

#### Windows

Make sure you have docker desktop installed, WSL2 configured and enough free RAM to run models. (see below)

#### Kubernetes & docker compose

Setting up Aya-LLM on Kubernetes or docker compose can be found in the wiki

## Models

Currently the following models are supported:

- Alpaca 7B
- Alpaca 7B-native
- Alpaca 13B
- Alpaca 30B
- GPT4All
- Vicuna 7B
- Vicuna 13B
- Open Assistant 13B
- Open Assistant 30B

If you have existing weights from another project you can add them to the `aya-llm_weights` volume using `docker cp`.

### :warning: A note on _memory usage_

LLaMA will just crash if you don't have enough available memory for your model.

- 7B requires about 4.5GB of free RAM
- 13B requires about 12GB free
- 30B requires about 20GB free


## Support

Feel free to join the discord if you need help with the setup: https://discord.gg/nhB8hv3Rf5

## Contributing

Aya-LLM is always open for contributions! If you catch a bug or have a feature idea, feel free to open an issue or a PR.

If you want to run Aya-LLM in development mode (with hot-module reloading for svelte & autoreload for FastAPI) you can do so like this:

```
git clone https://github.com/umilab/aya-llm.git
DOCKER_BUILDKIT=1 docker compose -f docker-compose.dev.yml up -d --build
```

You can test the production image with

```
DOCKER_BUILDKIT=1 docker compose up -d --build
```

## What's next

- [x] Front-end to interface with the API
- [x] Pass model parameters when creating a chat
- [x] Manager for model files
- [ ] Support for other models
- [ ] LangChain integration
- [ ] User profiles & authentication

And a lot more!
