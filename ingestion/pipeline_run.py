from ingestion.pipeline import IngestionPipeline

pipeline = IngestionPipeline()

result = pipeline.run(
    # "dataset/flipkart_demo_ecommerce_2024_2025/"
    "dataset/olist/"
)

print(result)