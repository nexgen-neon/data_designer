import data_designer.config as dd


def load_config_builder() -> dd.DataDesignerConfigBuilder:
    config_builder = dd.DataDesignerConfigBuilder()

    config_builder.add_column(
        dd.LLMTextColumnConfig(
            name="story",
            model_alias="nvidia-text",
 prompt=(
    "Generate one original short horror story. "
    "The story must be between 100 and 150 words. "
    "Build suspense and end with an unsettling twist. "
    "Output ONLY the story itself. "
    "Do NOT explain your reasoning. "
    "Do NOT analyze the request. "
    "Do NOT include a plan, outline, word count, commentary, "
    "or phrases such as 'Let's think step by step'. "
    "Do NOT include a title. "
    "Start directly with the first sentence of the story "
    "and end with the final sentence of the story."
)
            ),
        )
  

    return config_builder
