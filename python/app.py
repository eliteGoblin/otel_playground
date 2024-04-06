from fastapi import FastAPI
from time import sleep
import asyncio
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

app = FastAPI()

def init_tracer(service_name: str):
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: service_name})
        )
    )
    tracer_provider = trace.get_tracer_provider()
    span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4318"))
    tracer_provider.add_span_processor(span_processor)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)
    return trace.get_tracer(__name__)

tracer = init_tracer("example-server")

async def process_order():
    with tracer.start_as_current_span("process_order"):
        sleep(0.1)  # Simulate processing order
        await asyncio.gather(check_inventory(), charge_payment())

async def check_inventory():
    with tracer.start_as_current_span("check_inventory"):
        sleep(0.2)  # Simulate inventory check
        await asyncio.gather(check_stock_level(), reserve_stock())

async def charge_payment():
    with tracer.start_as_current_span("charge_payment"):
        sleep(0.15)  # Simulate payment charging
        await asyncio.gather(validate_payment_method(), process_payment())

async def check_stock_level():
    with tracer.start_as_current_span("check_stock_level"):
        sleep(0.05)  # Simulate stock level checking

async def reserve_stock():
    with tracer.start_as_current_span("reserve_stock"):
        sleep(0.1)  # Simulate stock reservation

async def validate_payment_method():
    with tracer.start_as_current_span("validate_payment_method"):
        sleep(0.05)  # Simulate payment method validation

async def process_payment():
    with tracer.start_as_current_span("process_payment"):
        sleep(0.2)  # Simulate payment processing

@app.get("/hello")
async def read_root():
    with tracer.start_as_current_span("handle_request"):
        # Simulate a delay in response
        await process_order()
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
