import os
from dotenv import load_dotenv
import logging
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.trace import config_integration

from datetime import datetime
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

# opencensus trace shows as a dependency in azure
def create_dependency(name,message):
    tracer = Tracer(exporter=AzureExporter(connection_string='InstrumentationKey=%s'%(instrument_key)), sampler=ProbabilitySampler(1.0))
    with tracer.span(name=name):
        print(message)

# opencensus log exporter will create a trace in azure
def create_trace(message):
    logger = logging.getLogger(__name__)

    logger.addHandler(AzureLogHandler(
        connection_string='InstrumentationKey=%s'% (instrument_key))
    )
    
    logger.warning(message)


def create_trace_dependency(name,message,message_before,message_after):
    config_integration.trace_integrations(['logging'])

    logger = logging.getLogger(__name__)

    handler = AzureLogHandler(connection_string='InstrumentationKey=%s'% (instrument_key))
    #handler.setFormatter(logging.Formatter('%(traceId)s %(spanId)s %(message)s'))
    logger.addHandler(handler)

    tracer = Tracer(
        exporter=AzureExporter(connection_string='InstrumentationKey=%s'% (instrument_key)),
        sampler=ProbabilitySampler(1.0)
    )

    logger.warning(message_before)
    with tracer.span(name=name):
        logger.warning(message)
    logger.warning(message_after)


if __name__ == '__main__':
    # load en vars
    load_dotenv()

    # get instrumentation key 
    instrument_key = os.environ["APPINSIGHTS_INSTRUMENTATIONKEY"]
 
    name = "Kiki opencensus trace 12Aug"
    message = "Hello, kiki <3 12Aug"
    message_before="before message..."
    message_after="after message..."

    create_dependency(name,message)
    create_trace(message)
    create_trace_dependency(name,message,message_before,message_after)

    print("done!")

  