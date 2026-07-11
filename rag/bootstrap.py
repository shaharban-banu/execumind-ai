def get_rag_pipeline():
    builder = RAGPipelineBuilder(
        rag_config=...,
        loader_configs=...,
        schema_registry=...
    )

    pipeline = builder.build()

    pipeline.initialize()

    return pipeline