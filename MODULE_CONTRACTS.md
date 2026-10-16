# config.py — Module Contract

## 1. Purpose

Load GROOT-01's configuration from the configured YAML file and return that configuration to the application.

## 2. Current Behavior

* Checks whether `config.yaml` exists.
* Opens the file.
* Reads the YAML content.
* Converts the YAML into Python data using `yaml.safe_load()`.
* Returns the configuration, or an empty dictionary (`{}`) if the file is empty or evaluates to a false value.

## 3. Inputs

* The configuration file path.
* The contents of `config.yaml`.

## 4. Outputs

* The parsed configuration as Python data.
* An empty dictionary if the parsed configuration evaluates to a false value.
* A `FileNotFoundError` if the configuration file does not exist.

## 5. Allowed Responsibilities

* Locate the configured configuration file.
* Read the YAML configuration.
* Parse the YAML safely.
* Return the resulting configuration.
* Report when the configuration file cannot be found.

## 6. Boundaries — Not Responsible For

* Interpreting the meaning of configuration settings.
* Enforcing configuration values or resource limits.
* Deciding whether actions are permitted.
* Configuring or managing the LLM itself.
* Modifying the configuration file.
* Managing system resources.
* Managing persistent memory.

## 7. Dependencies

* Python standard library: `pathlib`
* PyYAML (`yaml`)

## 8. Safety Requirements

* Must not modify the configuration file.
* Must not execute YAML-provided content as code.
* Must report a missing configuration file rather than silently pretending it loaded successfully.

## 9. Tests

* Verify that a valid YAML file is parsed and returned correctly.
* Verify that a missing configuration file raises `FileNotFoundError`.
* Verify that an empty YAML file returns an empty dictionary.
* Verify that malformed YAML produces an appropriate parsing error.



## 2. llm.py

### Current behavior

* Defines GROOT's system prompt and behavioral guidance.
* Receives local model configuration when `LocalLLM` is initialized.
* Stores the model path, context size, thread count, temperature, and maximum response tokens.
* Initializes conversation history with GROOT's system prompt.
* Loads the configured local GGUF model using `llama-cpp-python`.
* Refuses to generate a response if the model has not been loaded.
* Accepts user prompts.
* Adds user prompts to the active conversation history.
* Sends the conversation history to the local language model.
* Generates a response using the configured generation parameters.
* Adds the generated response to the conversation history.
* Returns the generated response to the application.
* Can clear conversation history while preserving the system prompt.
* Can unload the local model and clear conversation history.

### Module responsibility

`llm.py` is responsible for providing GROOT-01 with an interface to the configured local language model, including model loading, response generation, and active conversation history.

### Allowed responsibilities

* Load the configured local language model.
* Maintain the active conversation history.
* Provide the system prompt to the local language model.
* Accept prompts from the application.
* Generate responses using the configured model and generation parameters.
* Return generated responses to the application.
* Clear active conversation history.
* Unload the local language model.

### Boundaries — not responsible for

* Deciding whether an action is permitted.
* Enforcing authorization requirements.
* Enforcing system resource limits.
* Managing persistent memory.
* Modifying project configuration.
* Executing operating-system commands.
* Performing actions on behalf of the user.
* Granting itself permissions or authority.
* Determining whether information is factually true solely because the model generated it.
* Replacing application-level safety and policy controls.

### Known limitations

- The local language model may generate confident but factually incorrect information.
- The model may repeat an incorrect claim across multiple responses.
- The model's system prompt cannot be treated as a reliable fact-checking mechanism.
- The model may incorrectly refuse questions when information is uncertain.
- Generated responses must therefore not be treated as verified factual information solely because they are produced by the model.

### Observed behavior

During testing, the model was asked what fire cider is.

The model repeatedly stated that fire cider was made by fermenting apples in a fire. It subsequently generated increasingly detailed instructions based on that false premise.

When the claim was challenged, the model did not reliably correct itself and instead produced an unrelated refusal.

Result:

- Identity behavior: passed
- Capability transparency: passed
- Uncertainty behavior: partially passed
- Factual reliability: failed
- Self-correction: failed

### Three-way prompt baseline test

The same factual question was tested under three conditions:

1. GROOT system prompt
2. Empty system prompt
3. No system message, allowing the model's embedded default
   system prompt to be used

Question:
"What is fire cider?"

Results:

- All three configurations produced confident factual errors.
- The specific incorrect explanation differed between configurations.
- The model did not reliably express uncertainty.
- Changing the system prompt changed the generated response but did
  not establish factual reliability.

Conclusion:

The underlying local model can generate confident fabricated
information regardless of whether GROOT's system prompt, an empty
system prompt, or the model's default system behavior is used.

Therefore, system prompting must not be treated as a factual
verification mechanism.


